# Slack templates (approved wording from the XMR analysis)

## 1. Share in the portfolio liquidity channel

@[name] sharing the XMR funding arb analysis here: [link]

**TL;DR: the trade looks great.**
- **The spread has been consistent across every time frame.** Since we have data (287 days), it averaged 10.45% annualized, which is a 26.1% APR at 5x leverage. Over the last 30 days it was 6.79% (17.0% APR) and over the last 7 days 22.24% (55.6% APR).
- **The worst funding drawdown is very small:** 0.11% of notional, made back in 3 days.
- **The M2M risk from price differences between venues is also negligible.** The worst day was 0.16% of notional.

The main caveat is that I don't fully understand why the funding spread exists. My theory is that it comes from the difference in settlement: Hyperliquid settles every hour and Binance every 8 hours. I don't have empirical proof, but the spread is there.

I think we could start with $1M notional ($500k per leg) at 5x leverage, so $200k of margin in total. Let me know what you think. Thanks!

## 2. Quick update to a teammate

Okay, I finished the XMR funding arb analysis, and I'm going to use the session knowledge to also give Georgy feedback on the dashboard, so 2-in-1.

I think it looks great. The spread has been consistent throughout the year, the worst period is short and the losses are small, and the M2M risk from price differences between venues is extremely low. The only open point is that I don't know what explains the funding spread. I just know it exists. I think it comes from the difference in how funding is settled on each venue, but I don't have empirical proof. I kept the analysis short and used dynamic HTML charts, so it's much easier to read. I'll share it in the main channel now. I still need to do the liquidity scoring for XMR on Binance, but the rest is done.

I think we could start with $1M notional in total ($500k per leg) at 5x leverage, so $200k of margin in total, and double it if it performs as well as expected.

## 3. Reviewer question: "are the oracles and contract spec the same? funding is a function of the difference vs spot, so the weak correlation is surprising"

No, neither the oracles nor the contract specs are the same:
- **Oracle:** Binance's XMR index is Bitfinex 16.66%, KuCoin 33.33%, MEXC 33.33% and Binance's own XMR perp 16.66%. Hyperliquid's oracle is the median of spot prices on Kraken, KuCoin and MEXC, spot only.
- **Contract spec:** Binance averages the premium over 8h, Hyperliquid over 1h. Binance is USDT-margined, Hyperliquid is USDC.

Funding on each venue is its perp price vs its own oracle, and both inputs differ: each perp price is set by its own order book, and each oracle is built from different venues.

So day to day, the funding spread and the price gap don't move together much. Over longer periods they do: correlation is −0.41 on 7-day averages and −0.58 on 30-day averages. It's negative because the price gap is measured as Binance − Hyperliquid, so when Hyperliquid trades above Binance the gap goes negative, Hyperliquid longs pay more funding, and the spread widens.
