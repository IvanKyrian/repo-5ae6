---
name: funding-arb-analysis
description: Due-diligence write-up for a cross-venue funding rate arbitrage (long a perp on one venue, short the same perp on another). Use when the user asks to analyze a funding arb / funding spread trade between two exchanges, or to reuse "the XMR analysis" method on another asset or venue pair. Produces the Notion report, three interactive charts and a Slack TL;DR in the user's approved format.
---

# Funding rate arb analysis

Reference case: `analyses/xmr-binance-hyperliquid/` (long XMR on Binance, short on Hyperliquid, Oct 2026). Its `report.md` is the approved format and tone. Match it. Later runs with the same method: `analyses/hype-binance-hyperliquid/`, `analyses/zec-binance-hyperliquid/` (Nov 2026).

## What to ask the user for (if not given)

1. **Trade:** asset, long venue, short venue, symbols on each.
2. **Data:** a daily CSV (format below) or access to build it. If this session can't reach their DB or the exchange APIs, ask for the CSV.
3. **Sizing:** total notional and leverage. Default: $1M total ($500k per leg), 5×, so $200k margin.
4. **Regimes:** bear and bull date ranges, non-overlapping (e.g. bear `2026-01-15:2026-02-06`, bull `2026-02-07:2026-10-22`).
5. **Knowledge Layer averages** (7d / 30d / 90d / 1y) for both venues, to validate.
6. **Open interest** on each venue, with date.
7. **Index / oracle constituents** of each venue for the asset (e.g. screenshot of Binance's "References" tab; Hyperliquid's oracle venues).
8. Header fields they own: expected yield range, size.

## Input CSV

One row per UTC day:

| column | meaning |
|---|---|
| `date` | YYYY-MM-DD |
| `long_funding`, `short_funding` | daily funding = **sum of every settlement that UTC day**, decimal (0.0003 = 0.03%). Positive = longs pay shorts. |
| `long_close`, `short_close` | daily close of **each venue's own perp** |
| `long_n`, `short_n` | optional: settlements that day (sanity check) |

Building it from fmtdb (`psql -h 172.31.29.28 -p 5432 -U research -d fmtdb`), deduplicating first (the raw table has duplicate rows per timestamp):

```sql
WITH deduped AS (
  SELECT DISTINCT ON (venue, symbol, timestamp)
         venue, (to_timestamp(timestamp) AT TIME ZONE 'UTC')::date AS date_utc, funding_rate
  FROM public.funding_rate_history
  WHERE (venue = 'Binance' AND symbol = 'XMRUSDT') OR (venue = 'HyperLiquid' AND symbol = 'XMR/USD')
  ORDER BY venue, symbol, timestamp)
SELECT venue, date_utc AS date, SUM(funding_rate) AS daily_rate, COUNT(*) AS n
FROM deduped GROUP BY venue, date_utc;
```

Prices: Binance `fapi.binance.com/fapi/v1/klines?symbol=XMRUSDT&interval=1d`, Hyperliquid `POST api.hyperliquid.xyz/info {"type":"candleSnapshot","req":{"coin":"XMR","interval":"1d",...}}`. Mark prices in the DB are unreliable (Hyperliquid's are 0).

## Run

```bash
python3 .claude/skills/funding-arb-analysis/analyze.py --csv data.csv --asset XMR --long Binance --short Hyperliquid \
  --long-interval 8h --short-interval 1h --notional 1000000 --leverage 5 \
  --bear 2026-01-15:2026-02-06 --bull 2026-02-07:2026-10-22 --oi-long 58967094 --oi-short 123618604 --out out/
```

Writes `report.md` (Notion-ready, with `[...]` placeholders to fill), `slack.md`, `numbers.json`, and three charts: `<asset>-growth.html`, `<asset>-funding.html`, `<asset>-prices.html`. It prints checks (settlement counts, gaps, per-venue margin, pinned days). On the XMR data it reproduces the final report exactly.

Use `--regime-price-ref start` when the user gives periods as start-date close → end-date close (default `prior` measures from the day before the start, as in XMR). Always use the perp closes from the CSV for the price row; period tables the user pastes may come from spot or another source (HYPE's did).

Then:
1. Validate the period averages against Grafana / the Knowledge Layer. Grafana's backing table is `public.bishop_daily_funding_rate_history_materialized`; its rolling averages use `RANGE BETWEEN 'N days' PRECEDING AND CURRENT ROW`, i.e. N+1 calendar days including today's partial day. So 30d/90d/1y should match a last-N-full-days average within ~0.2pp, while 7d can be 1–2pp off. That's expected; anything else is a data problem.
2. Fill the placeholders: data start reason, theory, oracle constituents, contract specs, review tags.
3. Publish each chart as an Artifact (they embed in Notion via link; the user sets link sharing). Send PNG fallbacks too.

Data traps seen so far:
- Bishop (the server session) reports a "Net" column as long − short (Binance − Hyperliquid), which is negative when the trade earns. What the trade earns is short − long.
- Grafana can be missing days the exchange API has (HYPE: Binance 28 Jan – 2 Feb 2026). Report the gap in the overview; offer to fill it from the API.
- Grafana's history can start later than the exchanges' (ZEC from 1 Jan 2026, API from Oct 2025). Say why the series starts where it does.
- Binance settlement intervals differ by contract (XMR 8h, HYPE 4h, ZEC 8h); the base rate is still 0.03%/day. Pass `--long-interval`.

## Method (what each number is)

- **Spread** = short-venue daily funding − long-venue daily funding. Annualized = daily × 365.
- **Implied APR** = spread × (leg notional ÷ total margin) = spread × leverage / 2 (×2.5 at 5×).
- **Funding P&L** = daily spread × leg notional. **% of notional** = $ ÷ total notional.
- **Periods:** last 7, 30, 90, 180 days and max track record, all ending on the last data day. Call them "periods", not "windows".
- **Daily behavior:** positive / zero / negative days. Round the spread to 1e-12 first: days where both venues sit at the base rate come out as −5e-20 and must count as zero, not negative.
- **Worst cases:** worst single-day spread (date, annualized, APR, $, %), and worst funding drawdown = biggest peak-to-trough drop in cumulative funding P&L (dates from the day after the peak to the trough, avg spread, APR, $, %, date made back). No separate "negative streak" rows: the drawdown replaces them.
- **M2M** = coin quantity per leg × change in the $ price gap (long close − short close), same quantity on both legs, sized to the leg notional at the previous close. Report only the worst adverse daily M2M, and whether the gap closed the next day. Never use cumulative M2M recovery (it's just today's gap vs the entry gap and misleads). Never use spot (CoinGecko) as a proxy for either perp.
- **Gap stats:** average gap in bps, share of days within ±10 bps, widest gap.
- **Volatility note** (end of section 2, added after the PM team asked on XMR): days with close-to-close moves above 15% and 20%, the largest up and down move, and that each leg is margined on its own venue (20% margin at 5×). The script's checks print these.
- **Correlation** of daily spread vs daily gap, plus on 7-day and 30-day averages. Gap is long − short, so the expected sign is negative.
- **Bear vs bull:** price change from the prior day's close, avg spread, APR, negative days (+ zero days), cumulative funding P&L in the period, worst adverse daily M2M. No M2M P&L or total P&L rows.
- **$100 growth chart:** $100 × (1 + cumulative funding ÷ total margin). Say it earns the same return as the full margin.
- **Oracles and contract specs** (asked by reviewers): funding is each perp vs its own index/oracle, so list the constituents and weights of each, the premium averaging window, and the margin currency. Binance: Futures → Index Price → References, or `GET /fapi/v1/constituents`. Hyperliquid: weighted median of spot mids on Binance 3, OKX 2, Bybit 2, Kraken, KuCoin, Gate, MEXC, Hyperliquid 1, limited to venues that list the asset. For XMR, Binance's index included its own perp (16.66%), which damps its measured premium.

## Writing style

- Short, plain, natural. One line of method and one short interpretation per section. Explain anything that isn't obvious in one sentence.
- Tables over prose for numbers. No median, no stats the user didn't ask for.
- Use `$1M / $500k / $200k` for sizing, exact dollars for P&L, `−` for negatives.
- Header block: Date, Strategy category, Expected Yield Range, Protocol exposure, Size.
- Section order: Strategy overview (sizing, open interest, assumptions, "do we know what causes the spread?", growth chart) → 1. Historical funding spread → 2. Mark-to-market risk → 3. Oracles, contract specs and correlation → 4. Bear vs bull → Conclusion (first person).
- "Do we know what causes the spread?" is always answered "No", followed by the theory, labeled as a theory, not empirical evidence.

## Before sending

- Recompute every number from the CSV; check that tables, text and charts agree.
- Flag, in chat, anything that undercuts the conclusion: per-venue liquidation risk (the script lists days with moves above 75% of margin), partial days, data gaps, unconfirmed oracle venues.
- Leave the recommendation as `[Recommendation]` for the user; give your view in chat.
- Never state a fact you haven't verified (e.g. an oracle venue list); say what is unconfirmed and how to check it (`reference/oracle_check.py` rebuilds Hyperliquid's oracle from live spot prices).

Slack templates (share, TL;DR, reviewer Q&A) are in `reference/slack.md`.
