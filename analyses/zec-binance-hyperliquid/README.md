# ZEC funding arb: long Binance, short Hyperliquid (Nov 2026)

- `report.md`: write-up (Notion format), $1M notional, $500k per leg, 5×.
- `zec_daily.csv`: input from the server session (funding from Grafana's matview, perp closes from the venue APIs).
- `charts/`. Live: growth https://claude.ai/artifact/1xrxU3F3qBsKjjo873vZpJ · funding https://claude.ai/artifact/YJ7fHXdc1psJjh3CfeXkd4 · prices https://claude.ai/artifact/7wbfTwaXPYBRQNVjpZ7nbk

```bash
python3 .claude/skills/funding-arb-analysis/analyze.py --csv analyses/zec-binance-hyperliquid/zec_daily.csv --asset ZEC \
  --long Binance --short Hyperliquid --long-interval 8h --bear 2026-01-06:2026-02-04 --bull 2026-08-05:2026-09-04 \
  --regime-price-ref start --funding-source "Grafana (bishop_daily_funding_rate_history_materialized), deduplicated" --out out/
```
