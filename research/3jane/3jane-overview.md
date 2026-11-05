# 3Jane: overview and due diligence (updated 5 Nov 2026)

Sources: live app (backing, FCC facility detail, LCC), docs, data room (Slope tape analysis, LendSwift vintages, Settle back-book memo, LendSwift SPE LLC agreement), Morpho API, Telegram answers (26–27 Oct). Meeting notes from 16 Jul.

## Overview

3Jane is a credit-backed stablecoin protocol. It channels DeFi capital into short-duration US fintech credit through Fintech Credit Conduits (FCCs). The original uncollateralized crypto credit lines (CCL) are being sunset.

- TVL **$115.0M** (≈$75M in July). USD3 APY **6.30%**, sUSD3 APY **13.23%**.
- **USD3 (senior)** and **sUSD3 (junior, first loss)** sit on one pool. sUSD3 is **7.4%** of the pool (USD3 OC 108.9% vs an 8% target).
- Both tranches take a fixed *share* of pool income (no fixed senior coupon). Losses reduce pool income first, then sUSD3 principal, then USD3 principal. **Seniority protects USD3's principal, not its yield.**
- Accountable proof of reserves: $115.05M reserves vs $115.01M supply (100.04%).

## What backs USD3 ($115.4M)

| Bucket | $M | % | What it is | Cushion before 3Jane loses |
|---|---:|---:|---|---|
| Slope | 64.9 | 56.3% | 3Jane owns ~1,660 SMB trade-credit loans (30–90d) | None (eligibility box, R&W — terms not public) |
| Settle | 27.5 | 23.8% | 3Jane owns ~1,090 e-commerce inventory/payables loans (30–180d) | None (obligor reps, EPD putback, repurchase) |
| Aave USDC | 11.2 | 9.7% | Idle cash | n/a |
| LendSwift | 6.6 | 5.7% | Senior participation in a warehouse loan against ~22k subprime installment loans | 41% OC (min 33%), haircuts, DACA, cash sweep |
| Erebor bank cash | 4.1 | 3.6% | Cash in transit | n/a |
| Crypto credit lines | 1.1 | 0.9% | V1, payments only, 0% loss | Borrowers' verified assets |

**80% of backing is two forward-flow books that 3Jane owns outright, with no OC cushion.** LendSwift, the riskiest-looking line, is the smallest and best protected.

## Credit facilities

### Slope: SMB trade credit, forward flow (56%)
- B2B BNPL. A business buys inventory, Slope pays the supplier, and the business repays in 30–90 days. 3Jane buys the loans outright (true sale into its SPV). Slope services them for 0.5%.
- Live: $63.5M outstanding, 1,662 loans, 16.0% WA APR, 47 days average remaining, 0.00% NCO to date. Geography: NY 23%, NJ 14%, CA 12%.
- **Phase: Amortization, $0 remaining capacity.** About $45M comes back in Nov–Dec. Why?
- Protection: an eligibility box (>12m in business, >$1M revenue, SBFE tier ≤4, size caps $350k/$200k, no EPD) plus R&W. The trigger schedule and R&W repurchase show "Pending data" in the app.
- History (5,080 terminated loans, $260M): net loss 1.72% of originated, **0.27% excluding 3 obligors, 0.00% inside the eligibility box**. Losses are name-driven: the top 20 obligors caused 81% of losses, one obligor lost $2.9M, and recoveries were ~0%. The box's 0% partly relies on excluding EPD loans after the fact, so it only holds if there is an EPD putback.

### Settle: inventory/payables finance, back-book + forward flow (24%)
- Settle pays a brand's supplier invoice and the brand repays over 30–180 days (54% single-pay). 3Jane bought a ~$14.8M seasoned back-book in Sep 2026 (par + 0.40%) and buys new loans through a forward flow of up to $25M.
- Live: $28.2M outstanding, 1,088 loans, 16.9% WA APR, 109 days average remaining, 0.00% NCO.
- Protection: Settle represents that no obligor is delinquent or in forbearance anywhere at Settle. Breach or first-payment default means mandatory repurchase. Twice-weekly remittance, Nelnet backup servicer.
- 3Jane memo: expected loss 0.81% of balance, 9.4% IRR central case, breakeven at a 2.3% loss. Settle's lifetime loss is 1.5% of $3.8B originated, with H1-26 at 3.9% annualized (tariff cluster).
- Risk: lumpy obligors (67, largest 3%), tariff exposure, and a thinly capitalized counterparty for repurchases ($44M equity vs $303M warehouse debt; the seller SPV has no standalone financials).

### LendSwift: subprime consumer installment, senior warehouse (5.7%)
- About $500, ~4-month, ~690% APR installment loans. 3Jane holds a senior participation, advanced at 75% with a 15% coupon. The $10M line is 65.6% drawn and revolves until May 2027, with final maturity Nov 2027.
- Live (30 Oct): OC **41.4%** vs 33% minimum. Net collateral $9.4M vs $6.65M owed. Haircuts are $4.4M (>45 DPD $2.7M, 30–45 DPD $0.27M, payment shortfall $1.5M). About $0.56M more in haircuts would breach the OC test, which triggers the cash sweep.
- 31% of balance is 31+ DPD. That is expected at this APR: seasoned vintages collect ~1.3× the loan amount (1.5× cash funded) and the pool is back to 100% by months 3–4. Apr–May 2026 vintages are tracking at the low end (~117–121%).
- The real risks are the servicer (only a "cold" backup), regulation (~59% of balance in Texas) and the legal chain (see below).

## Loss scenarios: how much has to default?

Layers protecting USD3 principal: **pool income ~$7.8M/yr → sUSD3 $8.5M → USD3**.

- USD3 principal is hit beyond **~$16.3M of losses in 12 months** (16.5% of the $99M FCC book), or **$8.5M in a sudden shock** (8.6% of FCC).
- One facility at a time, at 0% recovery: Slope 13% of its book in a shock, or 3.9% loss per 2-month cycle sustained for a year. Its history is 1.72% whole book and 4.82% in the worst quarter. Settle needs 31% in a shock or ~58% annualized. **LendSwift cannot reach USD3 alone**, because the whole note is smaller than sUSD3.

| Scenario (12m) | Loss | USD3 | sUSD3 | Odds* |
|---|---:|---|---|---:|
| Base: Slope ex-3 history, Settle FY25 run-rate | $1.9M | ~4.8% yield | ~10% yield | 55% |
| Soft: Slope 2× that, Settle at memo EL | $3.7M | ~3.3% yield | ~7% yield | 25% |
| Stress: Slope whole-book history, Settle 2× H1-26 | $9.4M | ~0% yield, principal intact | −18% | 13% |
| Severe: 6 months of Slope's worst quarter, LendSwift halved | $15.5M | 0% yield, principal intact | −91% | 5% |
| Tail: Slope fraud or servicer collapse (25% lost), LendSwift halved | $19.5M | **−8.5%** | −100% | 2% |

*Indicative odds (mine). Expected USD3 principal loss is ~0.2%/yr. Expected yield is ~3.5% probability-weighted vs 6.3% today, because realized losses have been zero so far.

## Liquidity

- If 3Jane stopped redeploying: **~43% of the pool is cash within 30 days, ~66% within 60, ~80% within 90**. The July "loans can't be called" concern is real, but the loans are very short.
- The real run risk is **~$53M of USDC borrowed on Morpho** against USD3 ($10.2M at 6.43%) and PT-USD3-17DEC2026 ($43.3M). That is about half of USD3, levered largely for JANE. **The PT matures on 17 Dec**, while Slope repays $22.5M in December.
- USD3 redeems "up to the tranche ratio", subject to cash. sUSD3 has a 1-month lock plus cooldown. Committed liquidity facilities are on the roadmap.

## Opportunity for Re7: LCC

**Mechanics ($1M promise):** post $75k margin (7.5%) and earn 1.25% × $1M = $12.5k/yr from 3Jane, plus Aave on the margin. That's **20.2% on margin** (the app's 41.6% includes JANE at an assumed $250M FDV). On a call you have 9 days to deliver USDC. You receive **USD3 (not sUSD3)** with a 35-day cooldown, +0.75% APR during the cooldown, and margin released pro-rata. Missing a call slashes the margin into an auction. Looping borrows up to 84% LTV on a USD3l/USDC Morpho market (86% LLTV, **not live yet**), so 16% of the promise is enough capital.

**Constraints:** **$1M promise cap per address, one position per address** (about $15k/yr, which is immaterial). Exit takes at least 2 epochs (42 days) through a per-epoch cap (the app shows 6.67%, the docs 20%), and you stay callable meanwhile. 3Jane controls call timing and size, can pause, and can revoke positions. Live: $18.0M promised, $3.9M exiting, no calls yet. Our Cred Score of 845 ("Very Good") changes nothing until score-based terms go live.

| Option | Organic return (no JANE) | Clears 12–15%? |
|---|---|---|
| A. LCC, never called | 20.2% on margin; ~11.3% all-in on the $160k needed for a looped promise; +1.25% overlay if fully covered | On margin yes; all-in only at loop-sized backing |
| B. Called → hold USD3 | ~6.4% | No, but cheap to hold briefly (~0.5% drag vs 12% over 35 days) |
| C. Called → loop 6.25× | ~6.1% at 6.43% borrow (10.3% during cooldown) | Only if borrow ≤ ~5.2% or with JANE |
| D. Loop USD3 now (no LCC) | ~5.8% at 5×. Borrow 6.43% > yield 6.30% | No. It's a JANE farm |
| E. Lend USDC to loopers | 5.5–7.4% today (3Jane targeted ~10% net with incentives) | Possibly, with incentives |

**View:** pursue LCC only with a bespoke cap (≥ $10M promise), as a 1.25% overlay on liquidity we hold anyway, and be comfortable holding USD3 for 35 days if called. Don't underwrite the loop at current borrow rates. JANE (final mint 2026, supply 1.1–6.7B) is upside, not base case.

## Key risks
1. **Slope concentration and opacity:** 56% of backing, owned outright, no OC, R&W and triggers not public, amortizing.
2. **Thin junior:** sUSD3 is 7.4% vs the 15% in 3Jane's own loss example.
3. **Leverage loop:** ~$53M of Morpho debt against USD3 and PT, JANE-driven, with the PT maturing 17 Dec.
4. **LendSwift legal chain:** the SPE's separateness covenants only apply while it's party to a *Participation Agreement with Series 78 of Cadence Group (Percent)*, so 3Jane may sit behind Percent as lender of record. The LLC agreement has no independent manager, no limit on voluntary bankruptcy, and allows dissolution by member consent.
5. **Originator and servicer failure:** LendSwift has a cold backup servicer. Settle is thinly capitalized.
6. **Regulatory:** ~690% APR with 59% of balance in Texas.
7. **Governance:** 3Jane sets the tranche income split and call timing, and can pause LCC. Upgrades run through a 7-day timelock. Audits: Veridise, Sherlock, Electisec (core), Guardian (LCC, helper on 27 Oct).

## Questions for 3Jane (priority order)
1. Why is Slope in amortization with $0 capacity? Renewal? Where does the ~$45M returning in Nov–Dec go?
2. Slope repurchase, EPD putback and trigger terms ("Pending data" in the app). Please share the Slope sale agreement.
3. Top-1 and top-10 obligor % in the current Slope and Settle pools, and the hard caps.
4. Borrower APR is ~16% but facility net APY is 8.65%. Who keeps the gap, and is any of it subordinated to 3Jane?
5. How and when are FCC defaults marked in PPS (FULL_MARKDOWN_DURATION)? Does the 6.3% net an expected-loss provision?
6. What's the hard minimum sUSD3 ratio, and what happens below the 8% OC target?
7. Plan for the 17 Dec PT-USD3 maturity (~$43M Morpho debt). Is Slope's amortization timed for it?
8. Can Re7 get a bespoke LCC allocation above the $1M per-address cap? Better fee or exit terms?
9. Expected call timing and size over the next 3 epochs.
10. USD3l/USDC Morpho market: launch date, oracle (exchange rate vs market), IRM/target rate, supply incentives. Could Re7 curate or supply it?
11. LendSwift: lender of record and lien holder (3Jane SPV vs Percent Series 78)? What makes the SPE bankruptcy-remote?
12. LendSwift: collections if the originator stops (cold backup), Texas licensing (CSO/CAB), recent vintage quality.
13. Settle: parent guarantee on repurchases? Forward-flow docs and equity raise status?
14. JANE final mint date and supply. Does the Cred Score affect the promise fee (docs) or only JANE (wumpy)?
15. LCC unstake capacity: 6.67% (app) vs 20% (docs)? Realistic exit time for $5M+?
