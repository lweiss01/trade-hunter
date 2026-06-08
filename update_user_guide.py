import sys

with open('USER_GUIDE.md', 'r', encoding='utf-8') as f:
    guide = f.read()

# 1. Update date
guide = guide.replace('**Last updated:** 2026-04-03', '**Last updated:** 2026-04-06')

# 2. Add Settings Page section under "Discovering markets with Category Search" or before it
settings_section = """
## Settings Page

Trade Hunter includes a built-in **Settings** panel accessible via the gear icon in the top right of the dashboard. This allows you to configure the app on the fly without manually editing your `.env` file. 

The Settings Page allows you to configure:
*   **Data Sources:** Toggle the Live Kalshi feed or Simulation feed, and securely input your Kalshi API credentials.
*   **Spike Thresholds:** Adjust `SPIKE_MIN_VOLUME_DELTA`, `SPIKE_SCORE_THRESHOLD`, and other detector variables in real-time. Changes to thresholds apply immediately without requiring a restart.
*   **Webhook Alerts:** Configure your default Discord webhook URL, set the Alert Mode (`all`, `detector-only`, or `analyst-signals-only`), and route specific topics (e.g., Crypto, Elections) to different channels.
*   **Storage & Server:** Modify database retention days, toggle quiet mode, or change the bind host/port.

*Note: Changes to data sources, webhooks, or server ports may require a server restart, which can be initiated directly from the Settings page.*

---"""

guide = guide.replace('## Discovering markets with Category Search', settings_section + '\n\n## Discovering markets with Category Search')

# 3. Update "Multiple server instances" section
old_instances = """## Multiple server instances

Trade Hunter now treats the configured host/port as a single-instance local startup target. On Windows, use `trade-hunter.cmd` as the supported launcher. Starting it again will ask the already-running local Trade Hunter instance on that port to shut down cleanly before the new one starts.

If you still see alternating status strings in the feed detail (different ws_msgs counts on successive refreshes), there may be an older pre-guard instance or a manually started stray process outside the supported path. Kill all and start one clean:

```powershell
# Windows
Get-CimInstance Win32_Process |
  Where-Object { $_.CommandLine -match "-m app" } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
.\trade-hunter.cmd
```

```bash
# macOS / Linux
pkill -f "python -m app"
python -m app
```"""

new_instances = """## Multiple server instances

Trade Hunter treats your configured host/port as a strictly enforced single-instance local startup target. 

On Windows, use `trade-hunter.cmd` as the supported launcher. On macOS/Linux, use `python -m app`. 

Starting the app again will automatically ask the already-running local Trade Hunter instance on that port to shut down cleanly. **If the old instance is hung, unresponsive, or fails to shut down, the new launcher will automatically identify the exact process holding your configured port (default 8765) and forcefully terminate it.**

You no longer need to manually track down and kill zombie `py -m app` processes or worry about stale instances causing alternating status strings. A fresh start guarantees a pristine, single server instance."""

guide = guide.replace(old_instances, new_instances)

# 4. Make sure Whale Detection math thresholds are called out as currently hardcoded but future tunable
whale_math_old = """The math:
1. **The Baseline:** The app caches the 99th percentile trade size (minimum $200 notional) and the average rate of whales (λ) over the last 24 hours.
2. **The Cluster:** It tracks a rolling 120-second window per market.
3. **The Alert:** If 3 or more 99th-percentile trades occur in that 120s window, and the Poisson probability of that happening is less than 1% (p < 0.01), it overrides normal scoring and fires a `whale-cluster` alert."""

whale_math_new = """The math (currently hardcoded, but planned for Settings UI integration in M011):
1. **The Baseline:** The app caches the 99th percentile trade size (minimum $200 notional) and the average rate of whales (λ) over the last 24 hours.
2. **The Cluster:** It tracks a rolling 120-second window per market.
3. **The Alert:** If 3 or more 99th-percentile trades occur in that 120s window, and the Poisson probability of that happening is less than 1% (p < 0.01), it overrides normal scoring and fires a `whale-cluster` alert."""

guide = guide.replace(whale_math_old, whale_math_new)

with open('USER_GUIDE.md', 'w', encoding='utf-8') as f:
    f.write(guide)
