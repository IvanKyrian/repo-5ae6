# Funding arb screening (25 Nov 2026)

One table comparing every live funding arb (long Binance, short Hyperliquid): Brent, WTI, XMR and ZEC.
`screening.html` is the deliverable: the methodology plus the table. `screening.csv` and `numbers.json` hold the same numbers.

Rebuild:

```
python3 -I fetch_api.py data                # optional: refresh Hyperliquid API + Binance archive (ZEC, XMR)
python3 -I screen.py --data "<folder with the exported funding CSVs>" --positions Other_Relevant_Data.xlsx --end 2026-11-24 --out .
python3 -I build_page.py                    # puts numbers.json into screening.html
```

ZEC starts on 3 Oct 2025 using `data/` (Hyperliquid API from its 2 Oct 2025 listing, Binance's public archive to 31 Oct 2026, our export after that).
XMR's Hyperliquid leg comes from the API because the export tool gets the first 24h of every file wrong; export times are London time and are converted to UTC.

Inputs, not committed: the settlement-level funding CSVs (annualized `funding_rate` per settlement) and the positions sheet (AuM, notional, OI per venue).
Oil starts on 1 May 2026 (April excluded, as asked). Leverage is 5×, so implied APR = spread × 2.5.
