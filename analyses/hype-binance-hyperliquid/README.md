# HYPE funding arb: long Binance, short Hyperliquid (Nov 2026)

- `report.md`: write-up (Notion format), $1M notional, $500k per leg, 5×.
- `hype_daily.csv`: input from the server session (funding from Grafana's matview, perp closes from the venue APIs).
- `charts/`. Live: growth https://claude.ai/artifact/BHM9AfozCK9RLhatgEKVyS · funding https://claude.ai/artifact/4XC4rVQmRC675tjuGh1Nic · prices https://claude.ai/artifact/WJfVjFVfbMfLZVUdWKo77i

```bash
python3 .claude/skills/funding-arb-analysis/analyze.py --csv analyses/hype-binance-hyperliquid/hype_daily.csv --asset HYPE \
  --long Binance --short Hyperliquid --long-interval 4h --bear 2025-11-07:2026-01-20 --bull 2026-04-02:2026-05-31 \
  --regime-price-ref start --funding-source "Grafana (bishop_daily_funding_rate_history_materialized), deduplicated" --out out/
```
