# <img src="Trade Hunter Icon.png" width="200" align="right"> Trade Hunter 🎯
    
    *The institutional edge for prediction market flow.*
    
    In prediction markets, alpha isn't just about knowing the news first—it's about seeing the money move before the news breaks. By the time a headline hits social media, the orderbook has already repriced.
    
    **Trade Hunter** is a real-time, locally-hosted intelligence dashboard built to catch coordinated institutional flow, aggressive hedging, and mathematically improbable volume spikes across prediction markets (like Kalshi) the exact second they happen.
    
    ---
    
    ## 🛰️ Trade Hunter vs. Traditional SaaS
    While cloud-based prediction trackers are convenient, **Trade Hunter** is built for traders who prioritize privacy, speed, and deep technical control.
    
    | Feature | Trade Hunter (Local-First) | Standard SaaS Tools |
    | :--- | :--- | :--- |
    | **Data Privacy** | **100% Private.** Your watchlists and SQLite database stay on your hardware. | Your activity and interests are stored on third-party servers. |
    | **Execution Latency** | **Direct.** Connects your machine directly to Kalshi WebSockets. | **Delayed.** Data often passes through a middle-man server first. |
    | **Intelligence** | **Dual-AI.** Use your own API keys for transparent, un-metered analysis. | Opaque, "black box" logic that you cannot audit or tune. |
    | **Customization** | **Open Logic.** Modify the Poisson thresholds or AI prompts yourself. | "One size fits all" alerts and fixed configurations. |
    | **Cost** | **Free & Open Source.** No monthly subscriptions to maintain access. | Recurring monthly fees. |
    
    ---
    
    ## 🔬 Detection Logic: The Math Behind the Signal
    Trade Hunter doesn't just alert on high volume; it identifies **statistically improbable** events using high-frequency anomaly detection.
    
    ### Whale Cluster Probability
    To separate coordinated institutional "sweeps" from organic retail flow, we model trade frequency using a **Poisson Distribution**. When $\ge 3$ trades from the 99th percentile of historical volume occur within a rolling 120-second window, we calculate the probability $P$ of that cluster occurring by chance:
    
    $$P(k; \lambda) = \frac{\lambda^k e^{-\lambda}}{k!}$$
    
    * **$\lambda$ (Lambda):** The expected arrival rate of "Whale" trades based on the 24-hour baseline.
    * **$k$:** The number of observed large trades in the current window.
    
    If the resulting probability is **$p < 0.01$**, the system triggers a **Purple Neon Edge** alert. This signals high-conviction institutional movement with less than a 1% chance of being random market noise.
    
    ---
    
    ## ⚡ Key Features
    - **🐋 Whale Cluster Detection:** Real-time Poisson probability modeling to catch the biggest players.
    - **🧠 Dual AI Analysts (Claude + Perplexity):** Integrated agents analyze order flow context to label moves as `signal`, `noise`, or `uncertain`.
    - **⚙️ Autonomous Tuning System:** An *Advisor* suggests threshold corrections based on false positives, while a *Governor* ensures logic stays within safe baseline rules.
    - **📈 Dynamic Baseline Detector:** Flags flow based on volume delta multiples rather than static numbers.
    - **🔔 Smart Discord Integration:** Routes specific topics (Crypto, Elections, etc.) to dedicated channels with AI-filtered signal verification.
    - **💾 Zero-Friction Local Runtime:** Lightweight SQLite backbone with self-cleaning retention, running on `localhost:8765`.
    
    ---
    
    ## 🚀 Quick Start
    Ensure you have Python 3.11+ installed.
    
    1. **Clone and Install:**
       ```bash
       git clone https://github.com/lweiss01/trade-hunter.git
       cd trade-hunter
       pip install -r requirements.txt
       ```
    
    2. **Launch:**
       * **Windows:** `.\trade-hunter.cmd` (Self-healing launcher)
       * **macOS / Linux:** `python -m app`
    
    3. **Access:** Open `http://127.0.0.1:8765` in your browser.
    
    *Note: Starts in SIMULATION mode by default so you can see the dashboard immediately.*
    
    ---
    
    ## 📊 Alert Tiers
    | Tier | Meaning | Visual |
    | :--- | :--- | :--- |
    | **watch** | Noticeable activity, worth monitoring. | Standard |
    | **notable** | Significant move, worth investigating. | Yellow Edge |
    | **high conviction** | Massive volume multiple + price shift. | Red Neon Edge |
    | **whale-cluster** | $\ge 3$ 99th-percentile trades in 120s ($p < 0.01$). | Purple Neon Edge |
    
    *Built to separate the signal from the noise.*
    
