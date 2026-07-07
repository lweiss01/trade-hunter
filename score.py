"""
score.py -- evaluation scorer for Trade Hunter.

Reads eval_log.jsonl (written by signal_log.py), verifies the hash chain,
joins signals to resolutions, and prints the full rubric:

  PROBABILITY (is the agent's number better than the market's?)
    - Brier score, agent vs market
    - Brier Skill Score vs market      <- HEADLINE
    - Log loss, agent vs market
    - Beat-market rate                 <- HEADLINE (most intuitive)
    - Directional hit rate, agent vs market
    - Calibration table + ECE
    - AUC (discrimination)

  ECONOMIC (would a bankroll actually grow, net of costs?)
    - Flat-stake P&L and ROI, net of Kalshi taker fees  <- HEADLINE
    - Fractional-Kelly log-growth and max drawdown (gross, directional)

  SIGNIFICANCE
    - Bootstrap 95% CIs on Brier skill score, beat-market rate, flat ROI

  BASELINES (Step 3)
    - market@T, always-favorite, coin-flip

Stdlib only. Run:  python score.py eval_log.jsonl

Refuses to score if the hash chain is broken, because a tampered log means
the inputs cannot be trusted and neither can any number computed from them.
"""

from __future__ import annotations

import argparse
import math
import random
from collections import defaultdict

from signal_log import SignalLog

EPS = 1e-15  # log-loss clip so a confident-and-wrong call never hits log(0)

# Below this many prob-scorable pairs, treat every headline as preliminary:
# bootstrap CIs are degenerate and a lucky streak looks like an edge. This is
# a display guard only; set your real publish threshold in pre-registration.
MIN_TRUST_N = 30


# ----------------------------------------------------------------------------
# probability metrics
# ----------------------------------------------------------------------------

def brier(probs, outcomes):
    if not probs:
        return None
    return sum((p - o) ** 2 for p, o in zip(probs, outcomes)) / len(probs)


def log_loss(probs, outcomes):
    if not probs:
        return None
    total = 0.0
    for p, o in zip(probs, outcomes):
        p = min(max(p, EPS), 1 - EPS)
        total += -(o * math.log(p) + (1 - o) * math.log(1 - p))
    return total / len(probs)


def brier_skill_score(agent_probs, market_probs, outcomes):
    """1 - Brier_agent / Brier_market. > 0 means the agent beats the crowd.
    This is the single number that decides whether there's an edge."""
    b_agent = brier(agent_probs, outcomes)
    b_market = brier(market_probs, outcomes)
    if b_agent is None or b_market is None or b_market == 0:
        return None
    return 1 - (b_agent / b_market)


def beat_market_rate(agent_probs, market_probs, outcomes):
    """Fraction of markets where the agent's probability landed strictly
    closer to the truth than the market's did. Ties (equal distance) count
    as not-beat, so this is a conservative read."""
    if not agent_probs:
        return None
    wins = 0
    for pa, pm, o in zip(agent_probs, market_probs, outcomes):
        if abs(pa - o) < abs(pm - o):
            wins += 1
    return wins / len(agent_probs)


def hit_rate(probs, outcomes):
    """Directional accuracy: lean YES if prob > 0.5. Support metric only."""
    if not probs:
        return None
    correct = 0
    for p, o in zip(probs, outcomes):
        pred = 1 if p > 0.5 else 0
        if pred == o:
            correct += 1
    return correct / len(probs)


def auc(probs, outcomes):
    """Rank-based AUC (Mann-Whitney), average ranks for ties. Probability
    the agent scores a random winner above a random loser."""
    data = sorted(zip(probs, outcomes), key=lambda x: x[0])
    n = len(data)
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j < n and data[j][0] == data[i][0]:
            j += 1
        avg_rank = (i + j - 1) / 2.0 + 1.0  # 1-based average rank
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j
    n_pos = sum(1 for _, o in data if o == 1)
    n_neg = n - n_pos
    if n_pos == 0 or n_neg == 0:
        return None
    sum_pos = sum(r for r, (_, o) in zip(ranks, data) if o == 1)
    return (sum_pos - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


def calibration(probs, outcomes, n_bins=10):
    """Return (rows, ece). Each row: (lo, hi, count, mean_pred, obs_freq).
    ECE is the count-weighted average gap between predicted and observed."""
    bins = [[] for _ in range(n_bins)]
    for p, o in zip(probs, outcomes):
        idx = min(int(p * n_bins), n_bins - 1)
        bins[idx].append((p, o))
    rows, ece, n = [], 0.0, len(probs)
    for b in range(n_bins):
        lo, hi = b / n_bins, (b + 1) / n_bins
        if not bins[b]:
            rows.append((lo, hi, 0, None, None))
            continue
        mean_pred = sum(p for p, _ in bins[b]) / len(bins[b])
        obs_freq = sum(o for _, o in bins[b]) / len(bins[b])
        ece += (len(bins[b]) / n) * abs(mean_pred - obs_freq)
        rows.append((lo, hi, len(bins[b]), mean_pred, obs_freq))
    return rows, ece


# ----------------------------------------------------------------------------
# economic metrics
# ----------------------------------------------------------------------------

def kalshi_taker_fee_cents(price_cents, multiplier=0.07):
    """Kalshi taker fee per contract: ceil(mult * P * (1-P) * 100) / 100,
    P in dollars, returned in cents. Default multiplier 0.07 is the standard
    taker rate; sports and index markets use different multipliers, so pass
    your own if you're scoring those. Settlement is free, so this is charged
    on entry only. Verify against the live schedule before publishing."""
    p = price_cents / 100.0
    fee_dollars = math.ceil(multiplier * p * (1 - p) * 100) / 100.0
    return fee_dollars * 100.0  # cents


def _trade_leg(pair):
    """Resolve a pair into (entry_cost_cents, won: bool) for the agent's
    chosen side, or None if there's no actionable trade / missing prices.

    buy_yes: pay the YES ask, win if outcome == 1
    buy_no : pay the NO ask (= 100 - YES bid), win if outcome == 0
             YES bid reconstructed as ask - spread when the book is known,
             else approximated from the last price.
    """
    action = pair.get("agent_action")
    ask = pair.get("entry_ask_cents")
    spread = pair.get("spread_cents")
    outcome = pair.get("outcome")
    if action not in ("buy_yes", "buy_no") or ask is None or outcome == "void":
        return None

    if action == "buy_yes":
        return float(ask), (outcome == 1)
    # buy_no
    yes_bid = (ask - spread) if spread is not None else ask
    no_cost = 100.0 - yes_bid
    return no_cost, (outcome == 0)


def pnl_flat(pairs, multiplier=0.07):
    """One contract per signal, net of taker fees. Returns dict with total
    profit (cents), total cost basis (cents), ROI, trade count, win rate."""
    profit = cost_basis = 0.0
    trades = wins = 0
    for pair in pairs:
        leg = _trade_leg(pair)
        if leg is None:
            continue
        cost, won = leg
        fee = kalshi_taker_fee_cents(cost, multiplier)
        payoff = 100.0 if won else 0.0
        profit += payoff - cost - fee
        cost_basis += cost + fee
        trades += 1
        wins += 1 if won else 0
    roi = (profit / cost_basis) if cost_basis > 0 else None
    return {
        "profit_cents": profit,
        "cost_basis_cents": cost_basis,
        "roi": roi,
        "trades": trades,
        "win_rate": (wins / trades) if trades else None,
    }


def pnl_kelly(pairs, fraction=0.25, cap=0.25):
    """Fractional-Kelly log-growth, gross of fees, directional view only.
    Bets are ordered by signal time. Kelly for buying at cost c (dollars)
    with belief q: f* = (q - c) / (1 - c), clamped to [0, cap], scaled by
    `fraction`. Returns final bankroll, log-growth, and max drawdown."""
    ordered = sorted(pairs, key=lambda p: p.get("ts_signal") or "")
    bankroll = 1.0
    peak = 1.0
    max_dd = 0.0
    bets = 0
    for pair in ordered:
        leg = _trade_leg(pair)
        q = pair.get("agent_prob")
        if leg is None or q is None:
            continue
        cost, won = leg
        c = cost / 100.0
        if pair.get("agent_action") == "buy_no":
            q = 1 - q  # belief in the NO side
        if c <= 0 or c >= 1:
            continue
        edge = (q - c) / (1 - c)
        f = max(0.0, min(cap, fraction * edge))
        if f == 0:
            continue
        r = (1.0 / c - 1.0) if won else -1.0  # net return per unit staked
        bankroll *= (1 + f * r)
        bets += 1
        peak = max(peak, bankroll)
        if peak > 0:
            max_dd = max(max_dd, (peak - bankroll) / peak)
        if bankroll <= 0:
            bankroll = 0.0
            break
    log_growth = math.log(bankroll) if bankroll > 0 else float("-inf")
    return {
        "final_bankroll": bankroll,
        "log_growth": log_growth,
        "max_drawdown": max_dd,
        "bets": bets,
    }


# ----------------------------------------------------------------------------
# significance
# ----------------------------------------------------------------------------

def bootstrap_ci(pairs, stat_fn, B=5000, seed=42, lo=2.5, hi=97.5):
    """Resample pairs with replacement B times; return (lo, hi) percentile CI
    for stat_fn(sample). stat_fn returns a scalar or None (None samples are
    skipped). Binary outcomes are noisy; the CI is what tells you if the
    point estimate means anything."""
    rng = random.Random(seed)
    n = len(pairs)
    if n == 0:
        return (None, None)
    stats = []
    for _ in range(B):
        sample = [pairs[rng.randrange(n)] for _ in range(n)]
        s = stat_fn(sample)
        if s is not None and not math.isinf(s):
            stats.append(s)
    if not stats:
        return (None, None)
    stats.sort()
    return (stats[int(lo / 100 * len(stats))], stats[int(hi / 100 * len(stats)) - 1])


# ----------------------------------------------------------------------------
# assembly + baselines
# ----------------------------------------------------------------------------

def _prob_scorable(pairs):
    """Pairs usable for probability metrics: real agent_prob, real market_prob,
    binary outcome. Directional-ticker pairs (no market prob) are excluded and
    counted separately."""
    good = []
    for p in pairs:
        if (
            p.get("agent_prob") is not None
            and p.get("market_prob") is not None
            and p.get("outcome") in (0, 1)
        ):
            good.append(p)
    return good


def _vecs(pairs):
    a = [p["agent_prob"] for p in pairs]
    m = [p["market_prob"] for p in pairs]
    o = [float(p["outcome"]) for p in pairs]
    return a, m, o


def score(pairs, fee_multiplier=0.07, kelly_fraction=0.25):
    ps = _prob_scorable(pairs)
    report = {
        "n_total_pairs": len(pairs),
        "n_prob_scorable": len(ps),
        "n_excluded": len(pairs) - len(ps),
    }
    if ps:
        a, m, o = _vecs(ps)
        report["brier_agent"] = brier(a, o)
        report["brier_market"] = brier(m, o)
        report["brier_skill_score"] = brier_skill_score(a, m, o)
        report["logloss_agent"] = log_loss(a, o)
        report["logloss_market"] = log_loss(m, o)
        report["beat_market_rate"] = beat_market_rate(a, m, o)
        report["hit_rate_agent"] = hit_rate(a, o)
        report["hit_rate_market"] = hit_rate(m, o)
        report["auc_agent"] = auc(a, o)
        report["calibration"], report["ece"] = calibration(a, o)

        # Step 3 baselines
        fav = [1.0 if mm >= 0.5 else 0.0 for mm in m]  # always-favorite as prob
        report["hit_rate_favorite"] = hit_rate(fav, o)
        report["base_rate_yes"] = sum(o) / len(o)

        # significance
        report["ci_brier_skill"] = bootstrap_ci(
            ps, lambda s: brier_skill_score(*_vecs(s))
        )
        report["ci_beat_market"] = bootstrap_ci(
            ps, lambda s: beat_market_rate(*_vecs(s))
        )

    # economics (uses all pairs with an actionable trade)
    report["pnl_flat"] = pnl_flat(pairs, fee_multiplier)
    report["pnl_kelly"] = pnl_kelly(pairs, kelly_fraction)
    report["ci_flat_roi"] = bootstrap_ci(
        pairs, lambda s: pnl_flat(s, fee_multiplier)["roi"]
    )

    # per-category headline (only where volume >= 10)
    by_cat = defaultdict(list)
    for p in ps:
        by_cat[p.get("category") or "uncategorized"].append(p)
    cats = {}
    for cat, group in by_cat.items():
        if len(group) < 10:
            continue
        a, m, o = _vecs(group)
        cats[cat] = {
            "n": len(group),
            "brier_skill_score": brier_skill_score(a, m, o),
            "beat_market_rate": beat_market_rate(a, m, o),
        }
    report["by_category"] = cats
    return report


# ----------------------------------------------------------------------------
# formatting
# ----------------------------------------------------------------------------

def _fmt(x, nd=4):
    return "n/a" if x is None else f"{x:.{nd}f}"


def _ci(t, nd=4):
    lo, hi = t
    if lo is None:
        return "n/a"
    if lo == hi:
        return f"[{lo:.{nd}f}, {hi:.{nd}f}] (degenerate: n too small to bootstrap)"
    return f"[{lo:.{nd}f}, {hi:.{nd}f}]"


def format_report(r):
    L = []
    L.append("=" * 66)
    L.append("TRADE HUNTER -- AGENT EVALUATION")
    L.append("=" * 66)
    L.append(
        f"pairs: {r['n_total_pairs']} total | "
        f"{r['n_prob_scorable']} prob-scorable | "
        f"{r['n_excluded']} excluded (no market prob / unresolved)"
    )

    n = r.get("n_prob_scorable", 0)
    if n < MIN_TRUST_N:
        L.append("")
        L.append("!" * 66)
        L.append(f"  PRELIMINARY: only {n} resolved pair(s). Nothing below is a")
        L.append(f"  result yet. CIs are degenerate under ~20 and a lucky streak")
        L.append(f"  reads as an edge. Keep logging to at least {MIN_TRUST_N}+ before")
        L.append(f"  reading any headline, and to your pre-registered minimum")
        L.append(f"  before publishing anything.")
        L.append("!" * 66)

    if r.get("n_prob_scorable"):
        L.append("")
        L.append("-- PROBABILITY -------------------------------------------------")
        L.append(f"  base rate YES               {_fmt(r['base_rate_yes'])}")
        L.append(f"  Brier   agent / market      {_fmt(r['brier_agent'])} / {_fmt(r['brier_market'])}")
        L.append(f"  LogLoss agent / market      {_fmt(r['logloss_agent'])} / {_fmt(r['logloss_market'])}")
        L.append(f"  HitRate agent / market      {_fmt(r['hit_rate_agent'])} / {_fmt(r['hit_rate_market'])}")
        L.append(f"  AUC (agent)                 {_fmt(r['auc_agent'])}")
        L.append(f"  ECE (calibration error)     {_fmt(r['ece'])}")
        L.append("")
        L.append("  >> HEADLINES")
        bss = r["brier_skill_score"]
        verdict = "beats market" if (bss or 0) > 0 else "no edge vs market"
        L.append(f"  Brier Skill Score vs market {_fmt(bss)}  CI {_ci(r['ci_brier_skill'])}  ({verdict})")
        L.append(f"  Beat-market rate            {_fmt(r['beat_market_rate'])}  CI {_ci(r['ci_beat_market'])}")

        L.append("")
        L.append("  -- calibration (agent) --")
        L.append("   bin        n   pred    obs")
        for lo, hi, n, mp, of in r["calibration"]:
            if n == 0:
                continue
            L.append(f"   {lo:.1f}-{hi:.1f}  {n:4d}  {_fmt(mp, 3)}  {_fmt(of, 3)}")

        L.append("")
        L.append("  -- Step 3 baselines --")
        L.append(f"   always-favorite hit rate   {_fmt(r['hit_rate_favorite'])}")
        L.append(f"   (market Brier is the bar the agent must beat: {_fmt(r['brier_market'])})")

    L.append("")
    L.append("-- ECONOMIC ----------------------------------------------------")
    pf = r["pnl_flat"]
    L.append("  flat stake, 1 contract per signal, net of taker fees:")
    L.append(f"    trades {pf['trades']} | win rate {_fmt(pf['win_rate'], 3)}")
    L.append(f"    profit {_fmt(pf['profit_cents'], 1)}c on basis {_fmt(pf['cost_basis_cents'], 1)}c")
    L.append(f"    ROI    {_fmt(pf['roi'])}  CI {_ci(r['ci_flat_roi'])}")
    pk = r["pnl_kelly"]
    L.append("  fractional Kelly (gross, directional):")
    L.append(f"    bets {pk['bets']} | final bankroll {_fmt(pk['final_bankroll'], 3)}x "
             f"| log-growth {_fmt(pk['log_growth'])} | max DD {_fmt(pk['max_drawdown'], 3)}")

    if r.get("by_category"):
        L.append("")
        L.append("-- BY CATEGORY (n >= 10) ---------------------------------------")
        L.append("   category            n   BSS      beat-mkt")
        for cat, c in sorted(r["by_category"].items()):
            L.append(f"   {cat:<18} {c['n']:4d}  {_fmt(c['brier_skill_score'])}  {_fmt(c['beat_market_rate'])}")

    L.append("")
    L.append("-- READING IT --------------------------------------------------")
    L.append("  Edge exists only if Brier Skill Score > 0 AND its CI excludes 0.")
    L.append("  Beat-market rate > 0.50 (CI too) is the intuitive confirmation.")
    L.append("  Positive flat ROI net of fees is the economic proof.")
    L.append("  If any CI straddles the line, you need more resolved markets.")
    L.append("=" * 66)
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Score Trade Hunter agent signals.")
    ap.add_argument("log", help="path to eval_log.jsonl")
    ap.add_argument("--fee-multiplier", type=float, default=0.07,
                    help="Kalshi taker multiplier (0.07 default; sports/index differ)")
    ap.add_argument("--kelly-fraction", type=float, default=0.25,
                    help="fractional Kelly multiplier for the growth sim")
    ap.add_argument("--allow-broken-chain", action="store_true",
                    help="score even if hash-chain verification fails (NOT recommended)")
    args = ap.parse_args()

    log = SignalLog(args.log)
    if not log.verify_chain():
        msg = ("HASH CHAIN VERIFICATION FAILED. The log was edited, reordered, "
               "or truncated after writing. Scores from it are NOT trustworthy.")
        if not args.allow_broken_chain:
            raise SystemExit("ERROR: " + msg + "\nRe-run with --allow-broken-chain to override.")
        print("WARNING: " + msg + "\n")

    pairs = log.load_scored_pairs()
    if not pairs:
        raise SystemExit("No resolved signal/resolution pairs yet. Nothing to score.")
    print(format_report(score(pairs, args.fee_multiplier, args.kelly_fraction)))


if __name__ == "__main__":
    main()