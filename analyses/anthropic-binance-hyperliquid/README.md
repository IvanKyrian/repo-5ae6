# Anthropic pre-IPO perps: short Binance, long Hyperliquid xyz (Nov 2026)

Per-share price gap between Binance `ANTHROPICUSDT` and trade.xyz `xyz:ANT` on Hyperliquid, from Mon 2 Nov 2026 00:00 UTC.
Trade opened 8 Nov 2026 01:26:44 (read as UTC).

- Chart (Notion embed): https://claude.ai/artifact/5mtjwJ1LS2dGFLG9zBf6pK, source `charts/anthropic-spread.html`, PNG fallback `charts/anthropic-spread.png`.
- `anthropic_prices.csv`: every close behind the chart (5-minute closes, the 1-minute entry candle, live Binance quotes), with the source of each.
- `spread.py`: rebuilds the CSV and prints the summary.

## Conversion

From the Cross-venue tab of the model (`Anthropic_1.xlsx`):

- Binance quotes valuation ÷ 1B. Binance per share = price × 1,000,000,000 ÷ 12,700,000,000 exchange post-offering shares.
- xyz:ANT quotes one share.
- Spread = Binance per share ÷ xyz price − 1, the model's "Short Binance / long xyz" column. The trade gains as it narrows. Funding and fees are not included.

## Snapshot, 9 Nov 2026 17:30 UTC

| | Spread |
|---|---|
| Entry, 8 Nov 01:26 UTC (1m closes: Binance 1,374.63, xyz 97.458) | 11.06% |
| If the entry time was Madrid time (00:26 UTC) | 11.58% |
| Last Binance 5m close, 9 Nov 10:25 UTC | 9.57% |
| Live, 9 Nov 17:30 UTC (Binance 1,391.49 via CoinGecko, xyz 100.91) | 8.58% |
| Range of 5m closes since 2 Nov | 4.01% (4 Nov 10:45) to 22.23% (3 Nov 01:35) |

## Sources

- Binance 5m and 1m closes, 2–8 Nov: Binance's public data portal, `data.binance.vision` (daily files, published the next morning UTC).
- Binance 9 Nov 00:00–10:25 UTC: the model's `5m candles` tab. Since 1 Nov it matches the portal on every candle except 6 Nov 13:20, where the portal value is used.
- Binance after 10:25 UTC on 9 Nov: CoinGecko `/derivatives` last price, paired with the xyz 1-minute close of the same minute. `fapi.binance.com` refuses requests from this cloud environment's region, so there are no Binance 5m candles between 10:30 and 17:15 UTC. Rerun `spread.py` after the 9 Nov portal file is out to fill the gap.
- xyz:ANT: Hyperliquid info API, `candleSnapshot`.

```bash
python3 analyses/anthropic-binance-hyperliquid/spread.py --xlsx Anthropic_1.xlsx --start 2026-11-02 \
  --entry "2026-11-08 01:26" --out analyses/anthropic-binance-hyperliquid/anthropic_prices.csv
```
