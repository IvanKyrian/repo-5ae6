# USDE mNAV trade: long StablecoinX (USDE) on IBKR, short ENA perp on Hyperliquid (Nov 2026)

- `report.md`: write-up (Notion format), $500k per leg.
- `usde_mnav_model.xlsx`: scenario model (inputs, balance sheet at market, mNAV history, scenarios, exit mNAV × ENA move grid). All formulas.
- `usde_mnav_daily.csv`: daily USDE close, ENA price at the Nasdaq close, mNAV, Hyperliquid ENA funding.
- `numbers.json`: every number used in the report.
- `data/`: raw inputs (Yahoo USDE daily chart, Hyperliquid ENA 1h candles and hourly funding).
- `charts/`. Live: mNAV https://claude.ai/artifact/TvrRwmc498eUC7AJtKyzK6 · price vs ENA https://claude.ai/artifact/KNKrDu8vZW7EBXBqrbpi67 · ENA funding https://claude.ai/artifact/VySKiH2hPx1NoqeKokwVGF · scenarios https://claude.ai/artifact/MB3LEJaY5SejBdYXixkg2x

Company facts (shares, ENA held, cash, liabilities) are set at the top of `build.py` from the Q3 2026 results (8-K, 16 Nov 2026).

```bash
python3 analyses/usde-mnav/build.py        # csv, numbers.json, charts
python3 analyses/usde-mnav/make_model.py   # xlsx (then recalc with LibreOffice to cache values)
```
