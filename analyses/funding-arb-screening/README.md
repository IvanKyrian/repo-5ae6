# Funding arb screening (25 Nov 2026)

One table comparing every live funding arb (long Binance, short Hyperliquid): Brent, WTI, XMR and ZEC.
`screening.html` is the deliverable: the methodology plus the table. `screening.csv` and `numbers.json` hold the same numbers.

Rebuild the numbers:

```
python3 -I screen.py --data "<folder with the funding CSVs>" --positions Other_Relevant_Data.xlsx --end 2026-11-24 --out .
```

Inputs, not committed: the settlement-level funding CSVs (annualized `funding_rate` per settlement) and the positions sheet (AuM, notional, OI per venue).
Oil starts on 1 May 2026 (April excluded, as asked). Leverage is 5×, so implied APR = spread × 2.5.
