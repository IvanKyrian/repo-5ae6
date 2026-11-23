# HYPE Funding Arb (Long Binance ; Short Hyperliquid)

**Date: 23 November 2026**

**Strategy category: Funding Arb**

**Expected Yield Range: 15-25%**

**Protocol exposure: Hyperliquid, Binance**

**Size: tbc**

---

#### **Strategy overview**

Long HYPE perp on Binance, short HYPE perp on Hyperliquid, and capture the funding spread. The price exposure cancels out, so what's left is the difference in funding between the two venues.

Over the full data series, 5 Nov 2025 – 22 Nov 2026 (383 days of data; the last 12 months of Grafana data plus the update to 22 Nov), the spread averaged **4.23% annualized**.

At 5× leverage per leg we multiply the spread by 2.5, because $500k of notional per leg earns the spread on $200k of total margin. That gives a **10.6% APR**.

**Sizing tbc**

- $1M total notional: $500k per leg
- 5× leverage on each leg: $100k margin on Binance and $100k on Hyperliquid, $200k in total

Binance Market OI: $263m

Hyperliquid Market OI: $1,161m. Current exposure is $2.05m (0.18%) and the OI limit is 2.22% ($25.8m), so we could add around $23.7m.

**Assumptions**

- All $ figures use the sizing above.
- % of notional = $ figure ÷ $1M total notional.
- Daily funding P&L = daily spread × $500k.
- Implied APR = annualized spread × 2.5 ($500k notional per leg ÷ $200k margin).
- Daily M2M = HYPE held per leg × change in the $ price gap between Binance and Hyperliquid. Both legs hold the same amount of HYPE, sized to $500k at the previous close.
- Days are UTC. Annualized = daily × 365. No compounding, before trading fees.

**Do we know what causes the spread, or have reason to believe it will persist?** No. Our theory is that it comes from how funding is calculated and settled: Binance settles every 4 hours and Hyperliquid every hour, and each venue measures the premium against a different reference price. Hyperliquid's funding has been higher than Binance's on 70% of days, and the 30-day average spread was positive 99.7% of the time. This is a theory, not empirical evidence, and it doesn't explain why the spread would persist.

📈 Growth chart: https://claude.ai/artifact/BHM9AfozCK9RLhatgEKVyS

The chart shows how $100 would have grown in the strategy since 5 Nov, funding only: $100 → $111.08.

#### **1. HYPE Historical funding spread**

*Method:* daily spread = Hyperliquid daily funding − Binance daily funding, with every settlement in the day summed and then annualized (×365). Implied APR = spread × 2.5. All periods end 22 Nov 2026.

| **Period** | **Avg funding spread (annualized)** | **Implied APR at 5×** |
| --- | --- | --- |
| 7 days | 3.79% | 9.5% |
| 30 days | 3.63% | 9.1% |
| 90 days | 3.13% | 7.8% |
| 180 days | 4.37% | 10.9% |
| Max track record (383 days) | 4.23% | 10.6% |

**Daily behavior**

| **Spread** | **Days** | **Share** |
| --- | --- | --- |
| Positive | 270 | 70.5% |
| Zero (both venues at the base rate) | 21 | 5.5% |
| Negative | 92 | 24.0% |

**Worst cases**

|  | **Dates** | **Avg spread (annualized)** | **Implied APR at 5×** | **Funding P&L** | **% of notional** |
| --- | --- | --- | --- | --- | --- |
| Worst funding spread, single day | 25 Feb | −21.4% | −53.5% | −$293 | −0.03% |
| Worst funding drawdown | 23 Feb – 4 Mar (10 days) | −6.8% | −17.1% | −$935 | −0.09% |

The worst funding drawdown is the biggest drop in cumulative funding P&L from a high to a low. 23 Feb – 4 Mar is where funding cost us the most, and it was made back by 21 Mar.

📈 Funding chart: https://claude.ai/artifact/4XC4rVQmRC675tjuGh1Nic

In every period in the table above (the last 7, 30, 90 and 180 days, and the full 383 days), Hyperliquid's average funding rate was higher than Binance's, so the average spread was positive. The spread moves around, from 3.6% over the last 30 days to 3.8% over the last 7. About 24% of days are negative, but those days are cheap: the worst stretch cost $935 (0.09% of notional) and was made back within 17 days.

#### **Mark-to-market risk**

**What it is:** we're long and short the same perp on two venues, so the M2M risk is the price gap between them. If both prices move the same, M2M is zero. Funding is not included. In practice it doesn't affect the trade profitability, because the gap closes quickly.

|  | **Date** | **P&L** | **% of notional** |
| --- | --- | --- | --- |
| Worst adverse daily M2M | 28 May | −$823 | −0.08% |

**This loss was the gap closing, not opening: the day before, Binance traded 22.0 bps above Hyperliquid (a gain of $495 that day), and on 28 May it was back to 5.2 bps.**

📈 Price chart: https://claude.ai/artifact/WJfVjFVfbMfLZVUdWKo77i

Across the period, the gap between venues averaged 1.1 bps (Binance slightly above), stayed within ±10 bps on 90% of days and never went past 22.0 bps. It doesn't persist: a gap that opens one day mostly closes the next.

Through a −50% price crash and a +105% price rally the gap stayed under 23 bps, and the worst day cost $823 (0.08% of notional).

#### **3. Spreads during Bear vs Bull periods**

|  | **Bear: 7 Nov – 20 Jan** | **Bull: 2 Apr – 31 May** |
| --- | --- | --- |
| Days | 75 | 60 |
| HYPE Price Action | $42 → $21 (−50.3%) | $35 → $72 (+104.9%) |
| **Avg funding spread (annualized)** | **3.58%** | **4.46%** |
| Implied APR at 5× | 8.9% | 11.1% |
| Negative spread days | 14 of 75 (+6 at zero) | 17 of 60 (+2 at zero) |
| Cumulative funding P&L during the period | +$3,673 (+0.37%) | +$3,664 (+0.37%) |
| Worst adverse daily M2M | −$682 on 25 Nov (−0.07%) | −$823 on 28 May (−0.08%) |

*Note:* all % figures in the table are based on the $1M total notional ($500k per leg).

The strategy does slightly better in the bull period. The spread averaged 4.46% (11.1% APR) against 3.58% (8.9% APR) in the bear, and negative days were 19% of the bear and 28% of the bull. It made money in both. M2M stayed small in both periods.

#### **Conclusion**

The spread has been consistent: positive in every period we looked at, averaging 4.23% annualized over the full track record, which is 10.6% APR at 5×. Negative stretches are short and cheap, and M2M between the venues is small. The carry is real but modest, less than half of XMR's.
