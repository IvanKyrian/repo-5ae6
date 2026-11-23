# HYPE Funding Arb (Long OKX ; Short Hyperliquid)

**Date: 23 November 2026**

**Strategy category: Funding Arb**

**Expected Yield Range: [TBD]**

**Protocol exposure: Hyperliquid, OKX**

**Size: tbc**

---

#### **Strategy overview**

Long HYPE perp on OKX, short HYPE perp on Hyperliquid, and capture the funding spread. The price exposure cancels out, so what's left is the difference in funding between the two venues.

Over the full data series, 24 Jun – 22 Nov 2026 (152 days of data; OKX history in Grafana starts on 24 Jun), the spread averaged **5.18% annualized**.

At 5× leverage per leg we multiply the spread by 2.5, because $500k of notional per leg earns the spread on $200k of total margin. That gives a **13.0% APR**.

**Sizing tbc**

- $1M total notional: $500k per leg
- 5× leverage on each leg: $100k margin on OKX and $100k on Hyperliquid, $200k in total

OKX Market OI: $88m

Hyperliquid Market OI: $1,161m. Current exposure is $2.05m (0.18%) and the OI limit is 2.22% ($25.8m), so we could add around $23.7m.

**Assumptions**

- All $ figures use the sizing above.
- % of notional = $ figure ÷ $1M total notional.
- Daily funding P&L = daily spread × $500k.
- Implied APR = annualized spread × 2.5 ($500k notional per leg ÷ $200k margin).
- Daily M2M = HYPE held per leg × change in the $ price gap between OKX and Hyperliquid. Both legs hold the same amount of HYPE, sized to $500k at the previous close.
- Days are UTC. Annualized = daily × 365. No compounding, before trading fees.

**Do we know what causes the spread, or have reason to believe it will persist?** No. Our theory is that it comes from how funding is calculated and settled: OKX settles every 8 hours and Hyperliquid every hour, and each venue measures the premium against a different reference price. Hyperliquid's funding has been higher than OKX's on 84% of days, and no 30-day stretch in the data had a negative average spread. This is a theory, not empirical evidence, and it doesn't explain why the spread would persist.

📈 Growth chart: https://claude.ai/artifact/Nh68CKDmUWdK91vgAkjniB

The chart shows how $100 would have grown in the strategy since 24 Jun, funding only: $100 → $105.40.

#### **1. HYPE Historical funding spread**

*Method:* daily spread = Hyperliquid daily funding − OKX daily funding, with every settlement in the day summed and then annualized (×365). Implied APR = spread × 2.5. All periods end 22 Nov 2026.

| **Period** | **Avg funding spread (annualized)** | **Implied APR at 5×** |
| --- | --- | --- |
| 7 days | 6.43% | 16.1% |
| 30 days | 6.66% | 16.6% |
| 90 days | 4.67% | 11.7% |
| Max track record (152 days) | 5.18% | 13.0% |

**Daily behavior**

| **Spread** | **Days** | **Share** |
| --- | --- | --- |
| Positive | 127 | 83.6% |
| Zero (both venues at the base rate) | 3 | 2.0% |
| Negative | 22 | 14.5% |

**Worst cases**

|  | **Dates** | **Avg spread (annualized)** | **Implied APR at 5×** | **Funding P&L** | **% of notional** |
| --- | --- | --- | --- | --- | --- |
| Worst funding spread, single day | 15 Nov | −9.6% | −24.1% | −$132 | −0.01% |
| Worst funding drawdown | 5 – 10 Aug (6 days) | −2.5% | −6.3% | −$207 | −0.02% |

The worst funding drawdown is the biggest drop in cumulative funding P&L from a high to a low. 5 – 10 Aug is where funding cost us the most, and it was made back by 14 Aug.

📈 Funding chart: https://claude.ai/artifact/AE2QKF6aFnJw2MNiXkh4Pp

In every period in the table above (the last 7, 30 and 90 days, and the full 152 days), Hyperliquid's average funding rate was higher than OKX's, so the average spread was positive. The spread moves around, from 6.7% over the last 30 days to 6.4% over the last 7. About 1 day in 7 is negative, but those days are cheap: the worst stretch cost $207 (0.02% of notional) and was made back within 4 days.

#### **Mark-to-market risk**

**What it is:** we're long and short the same perp on two venues, so the M2M risk is the price gap between them. If both prices move the same, M2M is zero. Funding is not included. In practice it doesn't affect the trade profitability, because the gap closes quickly.

|  | **Date** | **P&L** | **% of notional** |
| --- | --- | --- | --- |
| Worst adverse daily M2M | 22 Aug | −$648 | −0.06% |

**The gap swung from +5.8 bps (OKX above) to −6.8 bps that day, a move of about 13 bps, and stayed within its usual ±10 bps range afterwards.**

📈 Price chart: https://claude.ai/artifact/3Avas5PupxRAvdNmMWPQL8

Across the period, the gap between venues averaged 2.7 bps (OKX slightly above), stayed within ±10 bps on 90% of days and never went past 14.3 bps. It doesn't persist: a gap that opens one day mostly closes the next.

#### **3. Spreads during Bear vs Bull periods**

OKX data starts on 24 Jun, so it doesn't cover the bear (7 Nov – 20 Jan) or bull (2 Apr – 31 May) periods used for HYPE. All of the OKX track record sits after them.

#### **Conclusion**

The spread has been consistent: positive in every period we looked at, averaging 5.18% annualized over the full track record, which is 13.0% APR at 5×. Negative stretches are short and cheap, and M2M between the venues is small. The track record is short (152 days) and doesn't include a bear market.
