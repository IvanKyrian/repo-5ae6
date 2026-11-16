# USDE mNAV Trade (Long USDE on IBKR - Short ENA on Hyperliquid)

**Date: 16 Nov 2026**

**Strategy category: Discount-to-NAV arbitrage**

**Expected Yield Range: no fixed yield. The return is the mNAV re-rating (see Scenarios), plus ~9–12% funding on the short leg**

**Protocol exposure: Interactive Brokers (USDE, Nasdaq), Hyperliquid (ENA perp)**

**Size: TBD**

---

#### **Context: what is the trade**

StablecoinX (Nasdaq: USDE) is Ethena's listed treasury company. It came public in June 2026 through a SPAC. It holds about 3.03 billion ENA, roughly 20% of the supply. It has a small infrastructure business, but it is basically a pile of ENA.

So we can value it like a fund: what it owns minus what it owes.

**Balance sheet, at market.** Source: [Q3 2026 results, balance sheet as of 30 Sep 2026](https://www.sec.gov/Archives/edgar/data/2080215/000121390026120186/ea031225601ex99-1.htm). ENA is marked at today's price ($0.1169).

|  | **$** |
| --- | --- |
| ENA tokens (3.029B × $0.1169) | $354.1M |
| Cash | $10.4M |
| Other assets | $3.1M |
| **Total assets** | **$367.5M** |
| Liabilities (current) | $2.0M |
| **Equity (NAV)** | **$365.5M** |
| Class A shares | 24,029,576 |
| **NAV per share** | **$15.21** |
| USDE share price | $4.35 |

The stock trades at $4.35 against $15.21 of NAV per share. **We pay about 29 cents for every dollar of assets.**

Two notes on the filing:

- The balance sheet shows ENA at cost ($212.8M), not at market. We mark it to today's price.
- It also shows a $109.6M warrant liability. We leave it out: it is settled in shares, not cash, and the warrants are out of the money (strike $11.50).

Cash and liabilities are small, so we simplify and compare the stock only with its ENA. That is the **mNAV**:

> **mNAV = market cap ÷ value of the ENA held = (USDE price × 24.03M shares) ÷ (3.029B ENA × ENA price)**

Today: $104.5M ÷ $354.1M = **0.30x**.

**The trade:** buy USDE and short the same dollar amount of ENA. The ENA price risk cancels out. What is left is the mNAV. If it goes up, we make money. If it goes down, we lose.

#### **1. Why the trade makes sense now**

**Before:** the discount made sense. About half of the company's ENA was locked under a 48-month schedule to 2029 ([Q2 10-Q](https://www.sec.gov/Archives/edgar/data/2080215/000121390026090250/ea0301482-10q_stable.htm)). The company could not sell those tokens, so the market did not pay full value for them.

**Now:** the lock-ups are gone.

- On 14 Sep, Ethena and the Ethena Foundation signed a Waiver Letter. Effective 5 Oct, it **permanently removes all lock-ups** on the company's ENA. Source: [8-K, 17 Sep 2026](https://www.sec.gov/Archives/edgar/data/2080215/000121390026100751/ea0305686-8k_stablecoinx.htm).
- The [Waiver Letter itself](https://www.sec.gov/Archives/edgar/data/2080215/000121390026100751/ea030568601ex10-1.htm) (Exhibit 10.1, clauses 1.1 and 5) pre-approves selling ENA to fund *"repurchases of shares … pursuant to a plan adopted in accordance with Rule 10b5-1 … approved by the Foundation"*. In plain words: **the company is allowed to sell ENA to buy back its own stock.**
- The process: the company gives the Foundation 5 business days' notice. In that window the Foundation can buy the ENA itself at the same price. If it doesn't, the company can sell. Either way the tokens don't have to hit the market.

At 0.30x, a buyback is very accretive. Every $1 of ENA sold retires shares backed by about $3.3 of ENA.

**But the spread got wider, not narrower.** On 5 Oct, the day the lock-ups came off, mNAV was 0.48x. Today it is 0.30x. Nothing changed at the company: same ENA, same shares. What changed is the market. ENA fell from $0.25 to $0.12, and holders who own USDE as an ENA proxy sold the stock harder than the token.

This doesn't look rational. The main reason for the discount is gone, so it should be closing, not opening.

#### **2. Historical mNAV**

*Method:* every trading day since the listing on 26 Jun 2026:

> **mNAV = (USDE close × 24,029,576 shares) ÷ (3.029B ENA × ENA price at the Nasdaq close)**

ENA held and share count come from the Q3 results; both were the same at the end of Q2. The ENA price is the Hyperliquid ENA perp at 4pm New York. The last point (16 Nov) is intraday.

📈 mNAV chart: https://claude.ai/artifact/TvrRwmc498eUC7AJtKyzK6

📈 Share price vs ENA per share: https://claude.ai/artifact/KNKrDu8vZW7EBXBqrbpi67

|  | **mNAV** | **Date** |
| --- | --- | --- |
| At listing | 0.37x | 26 Jun |
| Min | 0.13x | 24 Jul |
| Max | 0.52x | 25 Sep |
| Day the lock-ups came off | 0.48x | 5 Oct |
| Average since listing | 0.33x | |
| **Today** | **0.30x** | **16 Nov** |

The stock has never traded above 0.52x of its ENA. It went from 0.13x to 0.52x in two months while ENA rallied, and it has been drifting down since the waiver.

*Note:* Starkiller's chart shows a 0.61x high. With closing prices on both sides we get 0.52x, so we use our number.

#### **3. What can go wrong**

- **The spread doesn't close, or gets wider.** This is the main risk. Nothing forces the discount to close. There is no redemption, and the Foundation still has to approve every sale. Today's Q3 results don't mention a buyback; management talks about growing the operating business. If mNAV goes back to its 0.13x low, we lose 56% on the long (see Scenarios).
- **ENA funding can turn negative.** We are short the perp, so we earn funding when it is positive. On Hyperliquid it has averaged 11.7% annualized since the listing. It was positive in 94% of hours, with only 4 negative days out of 143. But it can flip. We already have exposure to ENA funding today through our ENA Uniswap pool position.
- **USDE is thin.** It trades about 1.0M shares a day (~$4.5M at today's price). Large sellers can push the mNAV lower, and we would need days to get in or out.
- **ENA spikes need margin on Hyperliquid.** The hedge holds on paper, but the two legs sit on different platforms. ENA did +270% in Q3. If ENA jumps, the short loses on Hyperliquid while the gain on USDE sits at Interactive Brokers. We need low leverage and to move collateral.
- **Warrants cap the upside above $11.50.** 11.5M public warrants plus the sponsor warrants (~7.6M according to Starkiller, not yet checked against the 10-Q) convert above that price. With ENA at today's price, that only matters above ~0.78x mNAV.

📈 ENA funding chart: https://claude.ai/artifact/VySKiH2hPx1NoqeKokwVGF

#### **4. Execution**

- **Long:** buy USDE on Interactive Brokers, fully paid.
- **Short:** short the ENA perp on Hyperliquid, same dollar amount, at 2× leverage.
- **Example size:** $500k each side, so $750k of capital ($500k on Interactive Brokers + $250k margin on Hyperliquid).

**Match the dollar amount, not the ENA count.** $500k of USDE buys about 115k shares. Those shares are backed by 14.5M ENA (~$1.7M). We do *not* short 14.5M ENA. We short $500k of ENA (4.3M ENA).

Why: at a given mNAV, the share price moves 1:1 with ENA in % terms. So equal dollars is the hedge. Rebalance when the legs drift apart.

**How it pays**, on $500k per side, from today's 0.30x:

| **What happens** | **Long USDE** | **Short ENA** | **Net** |
| --- | --- | --- | --- |
| mNAV goes up to 0.40x, ENA flat | +$177,425 | $0 | **+$177,425** |
| mNAV goes down to 0.20x, ENA flat | −$161,287 | $0 | **−$161,287** |
| ENA falls 30%, mNAV stays at 0.30x | −$150,000 | +$150,000 | **$0** |
| ENA falls 30%, mNAV goes to 0.40x | −$25,802 | +$150,000 | **+$124,198** |

On top of that, funding on the short pays about $4,900 a month at the average rate since listing.

#### **5. Scenarios**

*Method:* entry at today's 0.30x. Exit at levels the stock has actually traded at since listing. Return on the long = exit mNAV ÷ entry mNAV − 1. ENA flat, before funding and costs. $500k long / $500k short.

| **Exit at** | **mNAV** | **Return on long** | **P&L** |
| --- | --- | --- | --- |
| Historical max (25 Sep) | 0.52x | +76.8% | **+$383,937** |
| Historical average | 0.33x | +12.5% | **+$62,328** |
| Historical min (24 Jul) | 0.13x | −55.9% | **−$279,435** |
| Half the historical min | 0.07x | −77.9% | **−$389,718** |
| Zero | 0.00x | −100% | **−$500,000** |

📈 Scenarios chart: https://claude.ai/artifact/MB3LEJaY5SejBdYXixkg2x

The model (`usde_mnav_model.xlsx`) has the same table with funding, costs and return on capital. It also has a grid of exit mNAV × ENA move. The inputs (price, ENA, size, funding, holding period) can be changed.

#### **Conclusion**

The main reason for the discount, the lock-ups, is gone. The company now has a pre-approved way to buy back stock at 30 cents on the dollar. The market went the other way and widened the discount from 0.48x to 0.30x, mostly because ENA sold off.

Getting back to where it was on the waiver day (0.48x) is worth about +62% on the long. Going back to the July low is −56%. We get paid ~12% annualized funding on the short leg while we wait.

The catalyst is a buyback, and that is in the Foundation's and management's hands, not ours. [Recommendation]

---

*Sources:* [Q3 2026 results (8-K, 16 Nov 2026)](https://www.sec.gov/Archives/edgar/data/2080215/000121390026120186/ea031225601ex99-1.htm) · [Waiver 8-K (17 Sep 2026)](https://www.sec.gov/Archives/edgar/data/2080215/000121390026100751/ea0305686-8k_stablecoinx.htm) · [Waiver Letter, Ex. 10.1](https://www.sec.gov/Archives/edgar/data/2080215/000121390026100751/ea030568601ex10-1.htm) · [Q2 2026 10-Q](https://www.sec.gov/Archives/edgar/data/2080215/000121390026090250/ea0301482-10q_stable.htm) · [Starkiller Capital, "The USDE mNAV Trade"](https://www.starkiller.capital/post/the-usde-mnav-trade) · Prices: Yahoo Finance (USDE), Hyperliquid API (ENA perp and funding). Market data as of 16 Nov 2026, ~1pm New York.
