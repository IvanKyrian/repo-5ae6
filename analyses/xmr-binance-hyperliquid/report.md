# XMR Funding Rate Arb (Long Binance - Short Hyperliquid)

**Date: 28 Oct 2026**

**Strategy category: Funding Rate Arbitrage**

**Expected Yield Range: 20-25%**

**Protocol exposure: Binance, Hyperliquid**

**Size: TBD**

---

#### **Strategy overview**

Long XMR perp on Binance, short XMR perp on Hyperliquid, and capture the funding spread. The price exposure cancels out, so what's left is the difference in funding between the two venues.

Over the full data series, 15 Jan – 28 Oct 2026 (287 days, since our Hyperliquid funding data starts on 15 Jan), the spread averaged **10.45% annualized**.

At 5× leverage per leg we multiply the spread by 2.5, because $500k of notional per leg earns the spread on $200k of total margin. That gives a **26.1% APR**.

**Sizing**

- $1M total notional: $500k per leg
- 5× leverage on each leg: $100k margin on Binance and $100k on Hyperliquid, $200k in total

**Markets Open Interest**

Binance OI: $58,967,094 (our leg is 0.85%)

Hyperliquid OI: $123,618,604 (our leg is 0.40%)

**Assumptions**

- All $ figures use the sizing above.
- % of notional = $ figure ÷ $1M total notional.
- Daily funding P&L = daily spread × $500k.
- Implied APR = annualized spread × 2.5 ($500k notional per leg ÷ $200k margin).
- Daily M2M = XMR held per leg × change in the $ price gap between Binance and Hyperliquid. Both legs hold the same amount of XMR, sized to $500k at the previous close.
- Days are UTC. Annualized = daily × 365. No compounding, before trading fees.

**Do we know what causes the spread, or have reason to believe it will persist?** No. Our theory is that it comes from how funding is calculated and settled: Binance settles every 8 hours and Hyperliquid every hour, and the two venues measure the premium against different reference prices (section 3). Hyperliquid's funding has been higher than Binance's on 70% of days, and no 30-day stretch in the data had a negative average spread. This is a theory, not empirical evidence, and it doesn't explain why the spread would persist.

📈 Growth chart: https://claude.ai/artifact/6vovg3j2LzmEnesA6q5irX

The chart shows how $100 would have grown in the strategy since 15 Jan, funding only: $100 → $120.54.

#### **1. Historical funding spread**

*Method:* daily spread = Hyperliquid daily funding − Binance daily funding, with every settlement in the day summed and then annualized (×365). Implied APR = spread × 2.5. All periods end 28 Oct 2026.

| **Period** | **Avg funding spread (annualized)** | **Implied APR at 5×** |
| --- | --- | --- |
| 7 days | 22.24% | 55.6% |
| 30 days | 6.79% | 17.0% |
| 90 days | 11.24% | 28.1% |
| 180 days | 13.31% | 33.3% |
| Max track record (287 days) | 10.45% | 26.1% |

**Daily behavior**

| **Spread** | **Days** | **Share** |
| --- | --- | --- |
| Positive | 200 | 69.7% |
| Zero (both venues at the base rate) | 19 | 6.6% |
| Negative | 68 | 23.7% |

**Worst cases**

|  | **Dates** | **Avg spread (annualized)** | **Implied APR at 5×** | **Funding P&L** | **% of notional** |
| --- | --- | --- | --- | --- | --- |
| Worst funding spread, single day | 5 Sep | −39.5% | −98.7% | −$541 | −0.05% |
| Worst funding drawdown | 9 – 19 Oct (11 days) | −7.5% | −18.8% | −$1,131 | −0.11% |

The worst funding drawdown is the biggest drop in cumulative funding P&L from a high to a low. 9 – 19 Oct is where funding cost us the most, and it was made back by 22 Oct.

📈 Funding chart: https://claude.ai/artifact/FgMiRy3BPQ261RdENzXF1v

In every period in the table above (the last 7, 30, 90 and 180 days, and the full 287 days), Hyperliquid's average funding rate was higher than Binance's, so the average spread was positive. The spread moves around, from 6.8% over the last 30 days to 22.2% over the last 7. About 1 day in 4 is negative, but those days are cheap: the worst stretch cost $1,131 (0.11% of notional) and was made back within 3 days.

#### **2. Mark-to-market risk**

**What it is:** we're long and short the same perp on two venues, so the M2M risk is the price gap between them. If both prices move the same, M2M is zero. Funding is not included. In practice it doesn't affect the trade profitability, because the gap closes quickly.

|  | **Date** | **P&L** | **% of notional** |
| --- | --- | --- | --- |
| Worst adverse daily M2M | 4 Mar | −$1,613 | −0.16% |

**The gap closed the next day. It went from −27.5 bps on 4 Mar to −4.1 bps the day after, recovering $1,166 of the loss.**

📈 Price chart: https://claude.ai/artifact/M9wck9LMWAfhBCXTf3TgvP

Across the period, the gap between venues averaged −2.5 bps (Hyperliquid slightly above), stayed within ±10 bps on 89% of days and never went past 27.5 bps. It doesn't persist: a gap that opens one day mostly closes the next.

Through a −53% price crash and a +87% price rally the gap stayed under 28 bps, and the worst day cost $1,613 (0.16% of notional).

#### **3. Oracles, contract specs and correlation**

Neither the oracles nor the contract specs are the same:

- **Oracle:** Binance's XMR index is Bitfinex 16.66%, KuCoin 33.33%, MEXC 33.33% and Binance's own XMR perp 16.66%. Hyperliquid's oracle is the median of spot prices on Kraken, KuCoin and MEXC, spot only (venue set not yet confirmed with `oracle_check.py`).
- **Contract spec:** Binance averages the premium over 8h, Hyperliquid over 1h. Binance is USDT-margined, Hyperliquid is USDC.

Funding on each venue is its perp price vs its own oracle, and both inputs differ: each perp price is set by its own order book, and each oracle is built from different venues.

So day to day, the funding spread and the price gap don't move together much. Over longer periods they do: correlation is −0.23 daily, −0.41 on 7-day averages and −0.58 on 30-day averages. It's negative because the price gap is measured as Binance − Hyperliquid, so when Hyperliquid trades above Binance the gap goes negative, Hyperliquid longs pay more funding, and the spread widens.

#### **4. Spreads during Bear vs Bull periods**

|  | **Bear: 15 Jan – 6 Feb** | **Bull: 7 Feb – 22 Oct** |
| --- | --- | --- |
| Days | 23 | 258 |
| XMR Price Action | $678 → $322 (−52.6%) | $322 → $601 (+86.9%) |
| **Avg funding spread (annualized)** | **2.13%** | **11.04%** |
| Implied APR at 5× | 5.3% | 27.6% |
| Negative spread days | 13 of 23 | 55 of 258 (+19 at zero) |
| Cumulative funding P&L during the period | +$671 (+0.07%) | +$39,029 (+3.90%) |
| Worst adverse daily M2M | −$1,267 on 3 Feb (−0.13%) | −$1,613 on 4 Mar (−0.16%) |

*Note:* all % figures in the table are based on the $1M total notional ($500k per leg).

The strategy clearly does better in the bull period. The spread averaged 11.04% (27.6% APR) in the bull against 2.13% (5.3% APR) in the bear, and negative days dropped from more than half (13 of 23) to about 1 in 5 (55 of 258). It still made money in the bear, just much less. M2M stayed small in both periods.

#### **Conclusion**

I don't know why Hyperliquid funding runs above Binance, but the spread has been consistent. It averaged 10.45% annualized over the full track record, which is 26.1% APR at 5×. Negative stretches are short and cheap. M2M between the venues is small and closes within a day. I see no reason not to deploy.
