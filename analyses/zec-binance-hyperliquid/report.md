# ZEC Funding Rate Arb (Long Binance - Short Hyperliquid)

**Date: 4 Nov 2026**

**Strategy category: Funding Rate Arbitrage**

**Expected Yield Range: [TBD]**

**Protocol exposure: Binance, Hyperliquid**

**Size: TBD**

---

#### **Strategy overview**

Long ZEC perp on Binance, short ZEC perp on Hyperliquid, and capture the funding spread. The price exposure cancels out, so what's left is the difference in funding between the two venues.

Over the full data series, 1 Jan – 4 Nov 2026 (308 days of data; Grafana's ZEC history starts on 1 Jan), the spread averaged **8.10% annualized**.

At 5× leverage per leg we multiply the spread by 2.5, because $500k of notional per leg earns the spread on $200k of total margin. That gives a **20.3% APR**.

**Sizing**

- $1M total notional: $500k per leg
- 5× leverage on each leg: $100k margin on Binance and $100k on Hyperliquid, $200k in total

**Assumptions**

- All $ figures use the sizing above.
- % of notional = $ figure ÷ $1M total notional.
- Daily funding P&L = daily spread × $500k.
- Implied APR = annualized spread × 2.5 ($500k notional per leg ÷ $200k margin).
- Daily M2M = ZEC held per leg × change in the $ price gap between Binance and Hyperliquid. Both legs hold the same amount of ZEC, sized to $500k at the previous close.
- Days are UTC. Annualized = daily × 365. No compounding, before trading fees.

**Do we know what causes the spread, or have reason to believe it will persist?** No. Our theory is that it comes from how funding is calculated and settled: Binance settles every 8 hours and Hyperliquid every hour, and each venue measures the premium against a different reference price (section 3). Hyperliquid's funding has been higher than Binance's on 82% of days, and no 30-day stretch in the data had a negative average spread. This is a theory, not empirical evidence, and it doesn't explain why the spread would persist.

📈 Growth chart: https://claude.ai/artifact/1xrxU3F3qBsKjjo873vZpJ

The chart shows how $100 would have grown in the strategy since 1 Jan, funding only: $100 → $117.09.

#### **1. Historical funding spread**

*Method:* daily spread = Hyperliquid daily funding − Binance daily funding, with every settlement in the day summed and then annualized (×365). Implied APR = spread × 2.5. All periods end 4 Nov 2026.

| **Period** | **Avg funding spread (annualized)** | **Implied APR at 5×** |
| --- | --- | --- |
| 7 days | 6.13% | 15.3% |
| 30 days | 5.09% | 12.7% |
| 90 days | 8.02% | 20.1% |
| 180 days | 8.25% | 20.6% |
| Max track record (308 days) | 8.10% | 20.3% |

**Daily behavior**

| **Spread** | **Days** | **Share** |
| --- | --- | --- |
| Positive | 254 | 82.5% |
| Zero (both venues at the base rate) | 12 | 3.9% |
| Negative | 42 | 13.6% |

**Worst cases**

|  | **Dates** | **Avg spread (annualized)** | **Implied APR at 5×** | **Funding P&L** | **% of notional** |
| --- | --- | --- | --- | --- | --- |
| Worst funding spread, single day | 5 Jun | −31.3% | −78.3% | −$429 | −0.04% |
| Worst funding drawdown | 9 – 15 Jan (7 days) | −5.8% | −14.4% | −$551 | −0.06% |

The worst funding drawdown is the biggest drop in cumulative funding P&L from a high to a low. 9 – 15 Jan is where funding cost us the most, and it was made back by 23 Jan.

📈 Funding chart: https://claude.ai/artifact/YJ7fHXdc1psJjh3CfeXkd4

In every period in the table above (the last 7, 30, 90 and 180 days, and the full 308 days), Hyperliquid's average funding rate was higher than Binance's, so the average spread was positive. The spread moves around, from 5.1% over the last 30 days to 6.1% over the last 7. About 14% of days are negative; the worst stretch cost $551 (0.06% of notional) and was made back within 8 days.

#### **2. Mark-to-market risk**

**What it is:** we're long and short the same perp on two venues, so the M2M risk is the price gap between them. If both prices move the same, M2M is zero. Funding is not included. In practice it doesn't affect the trade profitability, because the gap closes quickly.

|  | **Date** | **P&L** | **% of notional** |
| --- | --- | --- | --- |
| Worst adverse daily M2M | 4 Mar | −$1,177 | −0.12% |

**The gap closed the next day. It went from −16.0 bps on 4 Mar to −0.9 bps the day after, recovering $760 of the loss.**

📈 Price chart: https://claude.ai/artifact/7wbfTwaXPYBRQNVjpZ7nbk

Across the period, the gap between venues averaged −4.1 bps (Hyperliquid slightly above), stayed within ±10 bps on 85% of days and never went past 28.0 bps. It doesn't persist: a gap that opens one day mostly closes the next.

Through a −50% price crash and a +100% price rally the gap stayed under 29 bps, and the worst day cost $1,177 (0.12% of notional).

> **ZEC volatility:** the daily price moved more than 15% on 14 days and more than 20% on 8 days, the biggest being +29.1% on 21 Aug and −26.0% on 4 Jun. The hedge cancels this across the two legs, but each leg is margined on its own venue. At 5× each venue holds 20% margin, so a move like these can liquidate the losing leg unless collateral is moved during the day or leverage is lower.

#### **3. Oracles, contract specs and correlation**

Neither the oracles nor the contract specs are the same:

- **Oracle:** Binance's ZEC index is [constituents + weights from Binance's References tab]. Hyperliquid's oracle is [venues].
- **Contract spec:** Binance averages the premium over 8h, Hyperliquid over 1h. Binance is USDT-margined, Hyperliquid is USDC.

Funding on each venue is its perp price vs its own oracle, and both inputs differ: each perp price is set by its own order book, and each oracle is built from different venues.

So the funding spread and the price gap don't move together much day to day. The link is weak to moderate at every horizon: correlation is −0.29 daily, −0.37 on 7-day averages and −0.24 on 30-day averages. Negative is the expected sign: the price gap is measured as Binance − Hyperliquid, so when Hyperliquid trades above Binance the gap goes negative, Hyperliquid longs pay more funding, and the spread widens.

#### **4. Spreads during Bear vs Bull periods**

|  | **Bear: 6 Jan – 4 Feb** | **Bull: 5 Aug – 4 Sep** |
| --- | --- | --- |
| Days | 30 | 31 |
| ZEC Price Action | $502 → $252 (−49.8%) | $512 → $1,022 (+99.7%) |
| **Avg funding spread (annualized)** | **2.94%** | **10.08%** |
| Implied APR at 5× | 7.3% | 25.2% |
| Negative spread days | 8 of 30 (+1 at zero) | 3 of 31 (+1 at zero) |
| Cumulative funding P&L during the period | +$1,207 (+0.12%) | +$4,279 (+0.43%) |
| Worst adverse daily M2M | −$558 on 7 Jan (−0.06%) | −$619 on 26 Aug (−0.06%) |

*Note:* all % figures in the table are based on the $1M total notional ($500k per leg).

The strategy clearly does better in the bull period. The spread averaged 10.08% (25.2% APR) against 2.94% (7.3% APR) in the bear, and negative days were 27% of the bear and 10% of the bull. It made money in both. M2M stayed small in both periods.

#### **Conclusion**

I don't know why Hyperliquid funding runs above Binance, but the spread has been consistent: positive in every period we looked at, averaging 8.10% annualized over the full track record, which is 20.3% APR at 5×. Negative stretches are short and cheap, and M2M between the venues is small. The main risk is ZEC's volatility: eight daily moves were larger than a leg's 20% margin at 5×. [Recommendation]
