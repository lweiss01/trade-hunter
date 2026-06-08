import re

with open('app/detector.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add whale_history to MarketWindow
window_pattern = re.compile(r'    event_history: deque\[MarketEvent\] \| None = None  # For M002 enriched context')
content = window_pattern.sub(r'    event_history: deque[MarketEvent] | None = None  # For M002 enriched context\n    whale_history: deque[MarketEvent] | None = None', content)

init_pattern = re.compile(r'        if self.event_history is None:\n            self.event_history = deque\(maxlen=100\)  # Keep last 100 events')
content = init_pattern.sub(r'        if self.event_history is None:\n            self.event_history = deque(maxlen=100)  # Keep last 100 events\n        if self.whale_history is None:\n            self.whale_history = deque()', content)

# Modify process signature
process_pattern = re.compile(r'    def process\(self, event: MarketEvent\) -> SpikeSignal \| None:')
content = process_pattern.sub(r'    def process(self, event: MarketEvent, baselines: dict[str, float] | None = None) -> SpikeSignal | None:', content)

# Insert whale logic inside process
whale_logic = """        is_whale_cluster = False
        p_value = 1.0
        eff_lam = 0.0
        if baselines and event.event_kind == "trade" and event.trade_size is not None:
            p99 = baselines.get("percentile_99", 200.0)
            lam = baselines.get("lambda_120s", 0.0)
            
            pr = event.yes_price if event.yes_price is not None else 1.0
            notional = float(event.trade_size) * pr
            
            if notional >= p99:
                window.whale_history.append(event)
                
                cutoff = event.timestamp - timedelta(seconds=120)
                while window.whale_history and window.whale_history[0].timestamp < cutoff:
                    window.whale_history.popleft()
                
                k = len(window.whale_history)
                if k >= 3:
                    import math
                    eff_lam = max(lam, 0.001)
                    prob_less_than_k = 0.0
                    for i in range(k):
                        prob_less_than_k += math.exp(-eff_lam) * (eff_lam**i) / math.factorial(i)
                    p_value = 1.0 - prob_less_than_k
                    
                    if p_value < 0.01:
                        is_whale_cluster = True
"""

search_str = """        should_alert = self._should_alert(
            window=window,
            event=event,
            volume_delta=volume_delta,
            price_move=price_move,
            baseline=baseline,
        )"""

content = content.replace(search_str, search_str + '\n\n' + whale_logic)

# Modify the exit condition
exit_pattern = re.compile(r'        if not should_alert:\n            return None')
content = exit_pattern.sub(r'        if not should_alert and not is_whale_cluster:\n            return None', content)

# Modify score, tier, topic
score_logic = """        if is_whale_cluster:
            score = max(self._score(volume_delta, price_move, baseline), 8.0)
            tier = "whale-cluster"
            topic = self._topic(event)
            reason = f"whale-cluster: {len(window.whale_history)} whales in 120s (p={p_value:.4f}, λ={eff_lam:.3f})"
        else:
            score = self._score(volume_delta, price_move, baseline)
            tier = self._tier(event, score, volume_delta, price_move, baseline)
            topic = self._topic(event)
            reason = (
                f"{tier}: volume +{volume_delta:.0f} vs baseline {baseline:.0f}, "
                f"price move {price_move:.1%}, score {score:.2f}"
            )"""

old_score_logic = """        score = self._score(volume_delta, price_move, baseline)
        tier = self._tier(event, score, volume_delta, price_move, baseline)
        topic = self._topic(event)
        reason = (
            f"{tier}: volume +{volume_delta:.0f} vs baseline {baseline:.0f}, "
            f"price move {price_move:.1%}, score {score:.2f}"
        )"""

content = content.replace(old_score_logic, score_logic)

with open('app/detector.py', 'w', encoding='utf-8') as f:
    f.write(content)

