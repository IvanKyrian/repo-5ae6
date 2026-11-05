# XMR funding arb: long Binance, short Hyperliquid (Oct 2026)

- `report.md`: final write-up (Notion format), $1M notional, $500k per leg, 5×.
- `xmr_daily.csv`: input in the standard format for `.claude/skills/funding-arb-analysis/analyze.py`.
- `xmr_funding_arb_dataset_500k.csv`: full dataset with P&L at $500k per leg.
- `charts/`: the three chart pages. Live versions:
  - Growth: https://claude.ai/artifact/6vovg3j2LzmEnesA6q5irX
  - Funding: https://claude.ai/artifact/FgMiRy3BPQ261RdENzXF1v
  - Prices: https://claude.ai/artifact/M9wck9LMWAfhBCXTf3TgvP

Reproduce:

```bash
python3 .claude/skills/funding-arb-analysis/analyze.py --csv analyses/xmr-binance-hyperliquid/xmr_daily.csv \
  --asset XMR --long Binance --short Hyperliquid --bear 2026-01-15:2026-02-06 --bull 2026-02-07:2026-10-22 \
  --oi-long 58967094 --oi-short 123618604 --out out/
```
