# Trade Hunter - Deployment Checklist

**Milestone:** M001 - Live Data Integration & Persistence  
**Version:** 1.0.0  
**Status:** Production Ready  
**Last Updated:** 2026-04-03

## Pre-Deployment Checklist

### Environment Setup
- [ ] Python 3.11+ installed on production server
- [ ] Git repository cloned to production environment
- [ ] Virtual environment created: `python -m venv venv`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Production server meets minimum requirements:
  - 2GB RAM minimum
  - 10GB disk space for database growth
  - Port 8765 available (or configure APP_PORT)

### Configuration

#### Required Environment Variables
- [ ] Create `.env` file from `.env.example`
- [ ] Set `APP_HOST` (default: 127.0.0.1, use 0.0.0.0 for external access)
- [ ] Set `APP_PORT` (default: 8765)
- [ ] Set `ENABLE_SIMULATION=false` (disable simulation in production)
- [ ] Set `ENABLE_KALSHI=true` (enable live Kalshi feed)

#### Kalshi API Credentials
- [ ] Obtain Kalshi API key from https://kalshi.com/account/api-keys
- [ ] Set `KALSHI_API_KEY_ID` in `.env`
- [ ] Set `KALSHI_PRIVATE_KEY_PATH` to path of downloaded private key file
- [ ] Configure `KALSHI_MARKETS` with comma-separated market tickers
  - Example: `KALSHI_MARKETS=KXBTC-26DEC31-B110000,KELECT-28NOV04-TX-D`
  - Find tickers at https://kalshi.com/markets

#### PolyAlertHub Integration (Optional)
- [ ] Create PolyAlertHub account at https://polyalerthub.com (if using)
- [ ] Generate webhook token for Trade Hunter
- [ ] Set `POLYALERTHUB_TOKEN` in `.env`
- [ ] Configure webhook URL in PolyAlertHub dashboard:
  - URL: `https://your-domain.com/api/alerts/polyalerthub`
  - Method: POST
  - Auth: Bearer token (POLYALERTHUB_TOKEN)

#### Discord Notifications (Optional)
- [ ] Create Discord webhook URL (Server Settings → Integrations → Webhooks)
- [ ] Set `DISCORD_WEBHOOK_URL` in `.env`
- [ ] (Optional) Configure `DISCORD_WEBHOOK_ROUTES` for topic-specific channels
  - Format: `crypto=https://...,macro=https://...,elections=https://...`

#### Spike Detector Tuning
- [ ] Review default detector settings in `.env`:
  - `SPIKE_MIN_VOLUME_DELTA=120` (minimum volume change to trigger alert)
  - `SPIKE_MIN_PRICE_MOVE=0.03` (minimum price move: 3%)
  - `SPIKE_SCORE_THRESHOLD=3.0` (minimum composite score)
  - `SPIKE_BASELINE_POINTS=24` (number of events for baseline calculation)
  - `SPIKE_COOLDOWN_SECONDS=300` (5 minutes between duplicate alerts)
- [ ] Adjust based on market activity after initial deployment

#### Data Retention
- [ ] Set `RETENTION_DAYS=7` (or adjust based on storage capacity)
- [ ] Ensure sufficient disk space for retention period:
  - Formula: `(events_per_day × 1.5KB) × retention_days`
  - Example: 1000 events/day × 7 days = ~10MB

### Database Setup
- [ ] Verify `trade_hunter.db` will be created in project root
- [ ] Ensure database directory has write permissions
- [ ] Plan backup location for database file
- [ ] Database will auto-initialize on first run (schema.sql applied automatically)

### Security Checklist
- [ ] All API tokens stored in `.env` file (not in version control)
- [ ] `.env` file has restricted permissions: `chmod 600 .env`
- [ ] `INGEST_API_TOKEN` set if exposing `/api/events` endpoint publicly
- [ ] `POLYALERTHUB_TOKEN` set if exposing webhook endpoint publicly
- [ ] Firewall configured to restrict access to APP_PORT if needed
- [ ] Consider HTTPS reverse proxy (nginx/Caddy) for production

### Testing Pre-Deployment

#### Smoke Test
- [ ] Run smoke test: `python -m app --smoke-test`
- [ ] Verify output shows: "Smoke test complete: markets=X signals=Y triggered=Z"
- [ ] Verify `trade_hunter.db` created (~76KB initial size)

#### Unit Tests
- [ ] Run all tests: `pytest tests/ -v`
- [ ] Verify: "58 passed" (or more if new tests added)
- [ ] All S01, S02, S03 test suites passing

#### Kalshi Connection Test
- [ ] Test Kalshi credentials: `python test_kalshi_connection.py`
- [ ] Verify successful connection and market subscription
- [ ] Check for authentication errors

#### Database Persistence
- [ ] Start app: `python -m app`
- [ ] Let run for 30 seconds with Kalshi feed enabled
- [ ] Stop app (Ctrl+C)
- [ ] Query database: `python -c "import sqlite3; conn = sqlite3.connect('trade_hunter.db'); print('Events:', conn.execute('SELECT COUNT(*) FROM events').fetchone()[0])"`
- [ ] Verify events > 0

#### Feed Health Monitoring
- [ ] Start app, wait 10 seconds
- [ ] Query health: `curl http://127.0.0.1:8765/api/health`
- [ ] Verify all feeds show running=true
- [ ] Verify last_event_at timestamps are recent

## Deployment Steps

### 1. Initial Deployment
```bash
# Clone repository
git clone <repository-url> trade-hunter
cd trade-hunter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with production values

# Run smoke test
python -m app --smoke-test

# Start application
python -m app
```

### 2. Verify Deployment
- [ ] Dashboard accessible at `http://<APP_HOST>:<APP_PORT>`
- [ ] Live feed showing Kalshi markets
- [ ] Feed health panel shows "running: true" for all feeds
- [ ] Check browser console for JavaScript errors (should be none)
- [ ] Test PolyAlertHub webhook (if configured):
  ```bash
  curl -X POST http://<APP_HOST>:<APP_PORT>/api/alerts/polyalerthub \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer <POLYALERTHUB_TOKEN>' \
    -d @tests/fixtures/sample_polyalerthub_payload.json
  ```
- [ ] Verify Discord notifications (if configured) - trigger test spike

### 3. Process Management (Production)

Choose one process manager:

#### Option A: systemd (Linux)
Create `/etc/systemd/system/trade-hunter.service`:
```ini
[Unit]
Description=Trade Hunter Market Monitor
After=network.target

[Service]
Type=simple
User=<your-user>
WorkingDirectory=/path/to/trade-hunter
Environment="PATH=/path/to/trade-hunter/venv/bin"
ExecStart=/path/to/trade-hunter/venv/bin/python -m app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable trade-hunter
sudo systemctl start trade-hunter
sudo systemctl status trade-hunter
```

#### Option B: supervisor
Create `/etc/supervisor/conf.d/trade-hunter.conf`:
```ini
[program:trade-hunter]
command=/path/to/trade-hunter/venv/bin/python -m app
directory=/path/to/trade-hunter
user=<your-user>
autostart=true
autorestart=true
stderr_logfile=/var/log/trade-hunter/err.log
stdout_logfile=/var/log/trade-hunter/out.log
```

#### Option C: screen/tmux (Development)
```bash
screen -S trade-hunter
python -m app
# Detach with Ctrl+A, D
# Reattach with: screen -r trade-hunter
```

### 4. Monitoring Setup

#### Log Monitoring
- [ ] Set up log rotation for application logs
- [ ] Monitor for error patterns:
  - Kalshi connection failures
  - Database write errors
  - Retention cleanup failures

#### Health Endpoint Monitoring
- [ ] Add health check to monitoring system:
  ```bash
  */5 * * * * curl -f http://127.0.0.1:8765/api/health || alert
  ```
- [ ] Alert conditions:
  - Any feed running=false
  - error_count > 0
  - last_event_at older than 5 minutes (for active feeds)

#### Database Monitoring
- [ ] Monitor database file size:
  ```bash
  watch -n 3600 ls -lh trade_hunter.db
  ```
- [ ] Alert if size exceeds expected (retention_days × events_per_day × 1.5KB)
- [ ] Set up daily backup cron:
  ```bash
  0 2 * * * cp /path/to/trade_hunter.db /backup/location/trade_hunter_$(date +\%Y\%m\%d).db
  ```

#### Retention Cleanup Monitoring
- [ ] Check retention cleanup logs after 24 hours
- [ ] Verify rows deleted matches expectations
- [ ] Alert if cleanup fails

## Post-Deployment Verification

### Day 1 Checklist
- [ ] Verify Kalshi feed connected and receiving events
- [ ] Check database size is growing reasonably (~1-2KB per event)
- [ ] Verify spike detector triggering signals (check `/api/state` signals array)
- [ ] Test Discord notifications if configured
- [ ] Review logs for any errors or warnings
- [ ] Verify retention cleanup will run (24h after start)

### Week 1 Checklist
- [ ] Review database size growth rate
- [ ] Tune detector settings based on actual market activity:
  - Too many false positives? Increase SPIKE_SCORE_THRESHOLD
  - Missing important moves? Decrease SPIKE_MIN_VOLUME_DELTA
- [ ] Verify retention cleanup executed successfully
- [ ] Check feed reconnection behavior (review reconnect count in /api/health)
- [ ] Evaluate Discord notification volume

### Month 1 Checklist
- [ ] Review detector performance over longer baseline
- [ ] Adjust retention_days if needed based on storage
- [ ] Consider tuning baseline_points based on market cadence
- [ ] Document any operational issues or edge cases discovered

## Backup and Recovery

### Database Backup Strategy
**Recommended approach:**
```bash
# Stop application
sudo systemctl stop trade-hunter  # or supervisor/screen

# Backup database
cp trade_hunter.db backup/trade_hunter_$(date +%Y%m%d_%H%M%S).db

# Restart application
sudo systemctl start trade-hunter
```

**Automated daily backup:**
```bash
#!/bin/bash
# backup-trade-hunter.sh
systemctl stop trade-hunter
cp /path/to/trade_hunter.db /backup/trade_hunter_$(date +%Y%m%d).db
systemctl start trade-hunter
# Keep last 30 days
find /backup -name "trade_hunter_*.db" -mtime +30 -delete
```

Add to crontab: `0 3 * * * /path/to/backup-trade-hunter.sh`

### Restore from Backup
```bash
sudo systemctl stop trade-hunter
cp backup/trade_hunter_<timestamp>.db trade_hunter.db
sudo systemctl start trade-hunter
```

### Disaster Recovery
If database is corrupted:
```bash
# Stop app
sudo systemctl stop trade-hunter

# Remove corrupted database
mv trade_hunter.db trade_hunter.db.corrupted

# Restart app (new database will be created)
sudo systemctl start trade-hunter

# App will start with empty database - schema auto-initialized
# Optionally restore from last good backup
```

## Rollback Plan

If deployment fails:
```bash
# Stop application
sudo systemctl stop trade-hunter

# Restore previous version
git checkout <previous-commit>
pip install -r requirements.txt

# Restore database backup if needed
cp backup/trade_hunter_<timestamp>.db trade_hunter.db

# Restart
sudo systemctl start trade-hunter
```

## Known Limitations (M001)

1. **Detector state resets on restart:** Baseline calculations start fresh after app restart. Normal behavior will resume as new events arrive.

2. **Single-threaded event ingestion:** Adequate for <1000 events/day. For higher volume, consider transaction batching (future enhancement).

3. **24-hour cleanup interval:** First retention cleanup runs 24 hours after app start. Manual cleanup possible with:
   ```bash
   python -c "from app.retention import cleanup_old_events; print(cleanup_old_events(None, 7))"
   ```

4. **No payload validation for PolyAlertHub:** Empty payloads accepted with defaults. Monitor for unexpected data patterns.

## Support and Troubleshooting

### Common Issues

**Issue: Kalshi connection fails**
- Verify API credentials in .env
- Check KALSHI_PRIVATE_KEY_PATH points to correct file
- Test credentials: `python test_kalshi_connection.py`
- Check Kalshi API status: https://kalshi.com/status

**Issue: Database locked errors**
- Another process has database open
- Check for multiple app instances: `ps aux | grep "python -m app"`
- Kill duplicates and restart

**Issue: No events appearing in dashboard**
- Check ENABLE_KALSHI=true in .env
- Check KALSHI_MARKETS configured with valid tickers
- Verify network connectivity to Kalshi API
- Check /api/health for feed status

**Issue: Retention cleanup not running**
- Wait 24 hours after initial start
- Check logs for cleanup execution messages
- Manually trigger: `python -c "from app.retention import cleanup_old_events; print(cleanup_old_events(None, 7))"`

**Issue: Discord notifications not sending**
- Verify DISCORD_WEBHOOK_URL is correct
- Test webhook directly:
  ```bash
  curl -X POST <DISCORD_WEBHOOK_URL> \
    -H 'Content-Type: application/json' \
    -d '{"content": "Test from Trade Hunter"}'
  ```
- Check /api/health shows discord running=true

### Debug Mode
Enable verbose logging:
```bash
# Add to .env
DEBUG=true

# Restart app
sudo systemctl restart trade-hunter

# Watch logs
tail -f /var/log/trade-hunter/out.log
```

### Health Check Script
```bash
#!/bin/bash
# health-check.sh
curl -f http://127.0.0.1:8765/api/health | jq '
  .feeds | to_entries[] | 
  select(.value.running == false or .value.error_count > 0) |
  "ALERT: \(.key) feed unhealthy: \(.value)"
'
```

## Contact and Documentation

- **Code Repository:** <repository-url>
- **Documentation:** `.gsd/milestones/M001/M001-SUMMARY.md`
- **UAT Plans:** `.gsd/milestones/M001/slices/S0*/S0*-UAT.md`
- **Integration Tests:** `integration_test_results*.md`

## Sign-off

**Deployed by:** _______________  
**Date:** _______________  
**Version:** 1.0.0 (M001)  
**Environment:** ☐ Development  ☐ Staging  ☐ Production  

**Verification:**
- [ ] All pre-deployment checklist items complete
- [ ] Smoke test passed
- [ ] All 58 tests passing
- [ ] Database persistence verified
- [ ] Feed health monitoring confirmed
- [ ] Process manager configured
- [ ] Backup strategy in place
- [ ] Monitoring alerts configured
