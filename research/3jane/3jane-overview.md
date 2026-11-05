# 3Jane: research and due diligence

*Updated 5 Nov 2026. Sources: live 3Jane app (backing, facility detail tabs, LCC), 3Jane docs, data room (Slope historical tape, LendSwift vintages, Settle back-book memo, LendSwift SPE LLC agreement, Slope–3Jane Loan Sale Agreement), Morpho API, Trenches LCC LP Deal, calls with 3Jane (16 Jul; Jeremy Obadia, 5 Nov) and Telegram (26–27 Oct).*

*Charts: standalone HTML and PNG files in `charts/`, referenced below as **[Chart NN]**.*

---

## Executive summary

- **What USD3 is.** A ~$115M credit-backed stablecoin pool funding short-duration US fintech credit. USD3 is the senior tranche (6.3% APY). sUSD3 is the junior, first-loss tranche (13.2% APY) and makes up 7.4% of the pool. Both take a fixed *share* of pool income, so seniority protects USD3's principal, not its yield.
- **What backs it.** 80% of backing is two forward-flow books that 3Jane **owns outright**: Slope ($64.9M, SMB working-capital lines) and Settle ($27.5M, e-commerce invoice and inventory finance). Neither has an overcollateralization (OC) cushion. LendSwift, the riskiest-looking line (subprime consumer loans), is only 5.7% of backing and the best protected (41% OC). The rest is cash (13%) and a sunsetting crypto book (1%).
- **Default risk.** USD3 principal only loses money after pool income (~$7.8M/yr) and sUSD3 (~$8.5M) are gone: roughly $16M of losses in a year, or $8.5M in a sudden shock. Per 3Jane, and confirmed by the Slope tape, bad vintages come from **single large obligors**, not broad deterioration. The main mitigants are obligor caps by risk tier and merchant, and excluding the lowest tiers. Markdowns are taken immediately on any expected loss. **The Slope sale agreement is thinner than described.** It has no early-payment-default putback, reps that only speak at the sale date, a capped repurchase remedy, and a 101.5% purchase price.
- **Liquidity risk.** The liquidity sleeve (Aave + bank) is 13% of TVL against a 15% target. It's shared by both tranches, and primary redemption needs no KYC. Beyond the sleeve, 3Jane can simply **stop buying** on its uncommitted forward flows and let the book run off: ~43% of the pool would be cash within 30 days and ~66% within 60. The amplifier is leverage: **~50% of TVL is looped on Morpho (~$53M of debt)**. If USD3 underperforms, those loops unwind and pull on a sleeve that can't cover them.
- **Opportunity (LCC).** Promise looping isn't live (no market, no liquidity), so we don't count on it. That leaves spot LCC or the **Trenches private deal**. Uncalled, the margin earns ~34% (16% hard USD + 18% JANE). If called, our capital becomes USD3 at a fixed 18% for 70 days, of which only ~6.3% is organic. A call inside the 78–99-day term looks likely, and JANE makes up ~60% of the return in that case.

---

## Key figures

| Metric | Value | Note |
|---|---|---|
| TVL (USD3 + sUSD3) | $115.0M | Supply cap reached; caps raised in line with deployment, fill in ~10 min |
| USD3 APY / sUSD3 APY | 6.30% / 13.23% | USD3 trailing 30d >6.5% per 3Jane |
| sUSD3 share of pool | 7.4% | App shows USD3 OC 108.9% vs an 8% target |
| Liquidity sleeve | $15.3M (13.3%) | Aave $11.2M + Erebor bank $4.1M; target 15% |
| Looped share of TVL | ~50% | ~$53M USDC borrowed on Morpho against USD3 / PT‑USD3 |
| FCC deployed | $97.6M | 3 facilities, ~25k underlying loans, ~2-month WA remaining term |
| Realized net charge-offs | 0.00% | Slope and Settle to date |
| Proof of reserves | 100.04% | Accountable: $115.05M reserves vs $115.01M supply |
| LCC promised | $18.0M | $1.35M margin staked, no calls yet, $3.9M exiting |
| Pipeline | 4 more deals | Smaller; 2 near close in payments / settlement float |

---

## What backs USD3

Depositors put in USDC and get USD3 (senior) or sUSD3 (junior). Both sit on one pool of assets. Losses hit pool income first, then sUSD3, then USD3. 3Jane doesn't promise USD3 a fixed coupon: a fixed share of pool income goes to each tranche, so if income falls, USD3's yield falls with it.

**[Chart 01 · USD3 backing by asset]** `charts/01-backing-composition`

| Bucket | $M | % pool | What it is | Cushion before 3Jane loses |
|---|---:|---:|---|---|
| Slope | 64.9 | 56.3% | 3Jane owns ~1,660 SMB working-capital loans (30–90 days) | None. Eligibility box; sale reps only at sale |
| Settle | 27.5 | 23.8% | 3Jane owns ~1,090 e-commerce invoice / inventory loans (30–180 days) | None. Obligor reps, EPD putback, repurchase |
| Aave USDC | 11.2 | 9.7% | Idle cash, instantly available | n/a |
| LendSwift | 6.6 | 5.7% | Senior participation in a warehouse loan against ~22k consumer loans | 41% OC (min 33%), haircuts, DACA, cash sweep |
| Erebor bank cash | 4.1 | 3.6% | Cash in transit to or from facilities | n/a |
| Crypto credit lines | 1.1 | 0.9% | V1 unsecured lines, payments only, 0% loss | Borrowers' verified assets ($7.6M) |

**Two structures.** 3Jane uses two ways of funding fintech lenders, and the risk is different in each:
- **Forward flow (Slope, Settle).** 3Jane buys the loans outright and pays the originator to keep servicing them. 3Jane owns every loss, so there's more variance. The protections are eligibility rules, concentration caps and repurchase obligations. Both forward flows are **uncommitted**: 3Jane can stop buying at any time.
- **Warehouse (LendSwift).** 3Jane lends against a pool of loans at an advance rate (75%). Delinquent loans drop out of the borrowing base and the originator has to post more collateral. The originator takes the first 25% of losses. This is typically used for earlier-stage originators. As they mature, advance rates rise (up to 95–97%), and they eventually move to forward flow.

---

## Credit facilities

### Slope: SMB working-capital lines, forward flow (56% of backing)

**What it is.** Slope lends to small and mid-sized US businesses, embedded directly in the platforms they sell on (e.g. an Amazon seller gets a credit line inside Amazon). It's mostly short lines of credit for working capital, with some B2B BNPL. Lead Bank (a Missouri state bank) originates the loans and Slope buys them as program manager. 3Jane then buys them from Slope and pays Slope Financing, LLC 0.5% to service them.

| Key figures | |
|---|---|
| Exposure | $64.9M backing · $63.5M outstanding · ~$67M per Jeremy |
| Loans | 1,662 · WA APR 16.0% · avg remaining 47 days |
| Geography | NY 23% · NJ 14% · CA 12% · TX 10% · FL 8% |
| Realized net charge-offs | 0.00%; some delinquent loans, curing weekly |
| Facility status | Active; app labels the phase "Amortization", $0 remaining capacity |
| Commitment | Uncommitted forward flow; 3Jane can stop buying at any time |
| Risk tiers | Slope has 5 tiers; 3Jane buys only tiers 1–4, very little tier 4 |
| History analysed | 5,080 terminated loans · $260M · 679 obligors · top‑10 = 39% |

**Legal terms (Loan Sale Agreement, 17 Jun 2026).**

| Term | What the document says | Read |
|---|---|---|
| Parties | Slope Tech, Inc. → **3Jane Capital Corporation** (Wyoming corp.) | Confirm this is the bankruptcy-remote purchaser SPV the docs describe |
| Structure | One-off whole-loan sale of scheduled loans (1,130 loans, 287 obligors); true sale with a back-up first-priority security interest | Ongoing forward-flow purchases need separate documents, which we haven't seen |
| Price | **101.5% of unpaid principal** + accrued interest | On ~50-day loans a 1.5% premium costs roughly 10 pts of annualized yield if it repeats on every purchase. It likely explains much of the gap between the 16% APR and the 8.65% facility net APY |
| Loans | Promissory notes; only 63 of 1,130 have security agreements | Essentially unsecured |
| Seller reps | Only as of cut-off and closing: 0 DPD, not defaulted, not modified, no bankruptcy. Origination compliance "to Seller's knowledge". Slope acts "solely as program manager" | No rep on credit quality or future performance |
| Remedy | Repurchase (at UPB × 101.5%) or substitution for a material rep breach uncured in 30 days. Indemnity **excludes post-closing credit deterioration** | **No early-payment-default putback**, no concentration limits, no performance triggers in this document |
| Liability cap | 100% of purchase price (title, true sale, schedule, eligibility); 50% otherwise; uncapped for fraud | |
| Servicing | Slope keeps the servicing rights (A&R Servicing Agreement, not provided). 3Jane **can't sell the loans without Slope's consent** (not unreasonably withheld) | 3Jane can pledge the loans to a lender with notice |
| Law | New York; AAA arbitration | |

> Jeremy said forward flows include a repurchase if a loan is 30 DPD on its first payment. That isn't in this agreement (§11.1 is "[Reserved]"), so it must be in the forward-flow or servicing terms. It matters, because the zero-loss history of the eligibility box relies on it.

**Default risk.** On Slope's own history, losses came from a few large names. The top 20 obligors caused 81% of all losses, one manufacturer lost $2.9M (37.5% of its exposure), and recoveries were ~0%. Lifetime net loss is 1.72% of originations. Excluding three obligors it's 0.27%, and inside 3Jane's eligibility box it's 0.00%. The box requires >12 months in business, >$1M revenue, SBFE tier ≤4, size caps of $350k (tier ≤3) / $200k (tier 4), and no EPD, with caps per merchant. Of the three facilities, Slope is the most exposed to a US recession, because its borrowers depend on consumer demand through Amazon and similar platforms.

**[Chart 02 · Slope losses by quarter]** `charts/02-slope-losses-by-quarter`

**Liquidity.** The book is very short. If 3Jane stopped buying, ~42% of principal would be back in 30 days, 71% in 60, 89% in 90 and 99% in 180. That's ~$45M back in Nov–Dec alone.

**[Chart 03 · Slope repayment schedule]** `charts/03-slope-repayment-schedule`

| Main risks | Mitigants |
|---|---|
| Single large obligor defaults (historical driver of bad vintages) | Obligor caps by tier and per merchant; lowest tier excluded; tier 4 minimal |
| No structural cushion; 3Jane owns the loss | Loan yield, then sUSD3; immediate markdowns |
| Contractual protection weaker than presented (no EPD putback in the sale agreement, reps only at sale, 1.5% premium) | Eligibility box at purchase; confirm forward-flow terms |
| Macro: SMBs reliant on consumer demand | Short WAL; 3Jane can stop buying |
| Servicer / originator (Slope keeps servicing; loans can't be sold without consent) | Servicing standard; servicer termination events (agreement not seen) |

### Settle: e-commerce invoice and inventory finance, forward flow (24% of backing)

**What it is.** Invoice and payables financing for e-commerce and consumer-goods brands. Settle pays a brand's supplier now, and the brand repays over 30–180 days in 30-day fee blocks (54% single payment at maturity, 46% amortizing). Settle has originated $3.8B since 2019. 3Jane bought a seasoned ~$14.8M back-book in Sep 2026 at par + 0.40% and keeps buying under an uncommitted forward flow. The memo says up to $25M; Jeremy mentioned up to $100M. Settle Funding, LLC services the loans for 0.5%.

| Key figures | |
|---|---|
| Exposure | $27.5M backing · $28.2M outstanding |
| Loans / obligors | 1,088 loans · 100+ obligors (back-book: 67, largest 3.0%) |
| WA APR / WAL | 16.9% · ~70-day WAL (109 days avg remaining) |
| Realized net charge-offs | 0.00% |
| Risk tiers | Settle has tiers 1–9; 3Jane takes none of tier 9 and <1% of tier 8 |
| Protections | Whole-book obligor reps; mandatory repurchase; EPD putback; twice-weekly remittance; Nelnet backup servicer |
| 3Jane memo (back-book) | Expected loss 0.81% of balance · 9.4% IRR · breakeven at 2.3% loss |
| Originator | Settle Inc.: $44M equity vs $303M warehouse debt (Jun‑26); first profitable half H1‑26; seller entity has no standalone financials |

**Default risk.** Losses concentrate in mid-size obligors and in receivables that ever entered deferral. That's why the purchase relies on whole-book obligor reps (no delinquency or forbearance anywhere at Settle) rather than payment status alone. Per Jeremy, the largest obligors have historically performed best, because their loans are small relative to their revenue. Settle's brands sell to less price-sensitive consumers, so it should hold up better than Slope in a downturn. H1‑26 losses were higher (3.9% annualized) because of a tariff-driven cluster.

**[Chart 04 · Settle loss drivers]** `charts/04-settle-loss-drivers`

| Back-book scenario (3Jane memo) | Loss, % balance | Net IRR | Weight |
|---|---:|---:|---:|
| Central | 0.81% | 9.4% | 45% |
| Softening | 1.0% | 8.5–8.7% | 40% |
| Stress | 1.4%+ | 6.5–7.5% | 15% |
| Breakeven (≈ largest obligor defaults in full) | 2.3% | 0% | — |

**Liquidity.** Longer than Slope: ~26% of principal back in 30 days, 53% in 60, 74% in 90 and ~100% in 180.

**[Chart 05 · Settle repayment schedule]** `charts/05-settle-repayment-schedule`

| Main risks | Mitigants |
|---|---|
| Lumpy obligors; mid-size segment loses 4.5–5% | Obligor reps across Settle's whole book; per-obligor deferral disclosure; size caps |
| Untested single-pay principal; tariff sensitivity | Short term; losses priced at the elevated recent run-rate |
| Repurchase only as good as a thinly capitalized originator | Short exposure window; twice-weekly remittance; parent support under negotiation |
| Servicer commingling | 2-business-day remittance; Nelnet backup servicer |

### LendSwift: subprime consumer installment loans, senior warehouse (5.7% of backing)

**What it is.** Short-term emergency loans to US consumers ($200–1,500, typically ~$500, ~4 months, ~690% APR): money needed before the end of the month, repaid as fast as possible. 3Jane **doesn't own these loans**. It holds a senior secured participation in a loan to LendSwift's SPV, advanced at 75% of eligible collateral, with a 15% coupon (~16% net APY). Jeremy describes the team as very competent, working with a reputable law firm.

| Key figures | |
|---|---|
| Facility | $10.0M commitment · $6.56M drawn (30 Oct) · ~$6.9M per Jeremy (5 Nov) |
| Term | Revolving to 26 May 2027 · final maturity 26 Nov 2027 |
| Collateral | 21,923 loans · WA APR 692% · WA term 116 days · largest obligor 0.0002% |
| Coverage | Net collateral $9.4M vs $6.65M owed → **OC 41.4%** (min 33%) |
| OC history | 34.7–46.6% weekly since June; never breached |
| Delinquency | 31% of balance 31+ DPD (25–33% band every week since May) |
| Borrowers | 69% new / 31% repeat · ~59% of balance in Texas |
| Protections | Haircuts (>45 DPD 0% credit; 30–45 DPD 60%; payment shortfall 0%; obligor >2% of net collateral 0%); weekly OC test; DACA; cash sweep on breach; 3-month write-off trigger; bad-boy guarantees on founders |
| Servicing | LendSwift; backup servicer "cold" |
| Legal | SPE separateness tied to a Participation Agreement with Series 78 of Cadence Group (Percent); no independent manager in the LLC agreement |

**Default risk.** The high delinquency is priced in. The metric 3Jane watches is cash returned per dollar lent, which is always above 120–125% against a 75% advance. 3Jane's note only loses money after ~$7.2M of the $13.8M of gross loans plus cash is gone. Another ~$0.56M of haircuts would breach the 33% OC test, which stops new draws and sends all collections to 3Jane until OC is restored. The real risks are elsewhere. If loans were worthless through fraud, recovery would rely on suing the founders under bad-boy guarantees, a long process that depends on LendSwift's equity (financials refreshed every 6–12 months). Other risks are servicer failure (cold backup), regulation (690% APR, 59% in Texas) and the participation chain via Percent. In a recession, demand for emergency loans rises and fast turnover limits the losses from any one moment.

**[Chart 06 · LendSwift borrowing base]** `charts/06-lendswift-borrowing-base`
**[Chart 07 · LendSwift delinquency]** `charts/07-lendswift-delinquency`
**[Chart 08 · LendSwift collections by vintage]** `charts/08-lendswift-collections-by-vintage`

**Liquidity.** It's a committed line, so 3Jane has to keep ~$3.1–3.4M undrawn capacity available. Collections recycle into new loans until May 2027. After a trigger they sweep to 3Jane: the $2.0M of cash plus scheduled principal would cover the $6.65M owed by ~Feb 2027, before counting interest and fees.

**[Chart 09 · LendSwift payoff schedule]** `charts/09-lendswift-payoff-schedule`

| Main risks | Mitigants |
|---|---|
| Fraud: collateral worthless | Bad-boy guarantees; weekly surveillance and loan-level data |
| Servicer failure (cold backup) | DACA control of collections; cash sweep |
| Regulatory (690% APR, Texas concentration) | Reputable counsel; small share of backing |
| Recent vintages tracking at the low end (~117–121%) | 33% OC test; write-off trigger stops funding |
| Legal chain (participation via Percent; thin SPE agreement) | Senior position; to confirm via the participation and credit agreements |

### Crypto credit lines (0.9%)

V1 unsecured USDC lines to crypto users, in wind-down. $1.08M outstanding, 0% past due, 0% loss, backed by $7.6M of verified borrower assets.

---

## How much has to default?

*Scenarios to be completed with 3Jane's stress cases (Jeremy is consolidating facility-level stress tests to USD3 level). The framework and breakevens below come from the structure and won't change.*

**Loss order:** pool income (~$7.8M/yr paid to holders today) → sUSD3 (~$8.5M) → USD3 principal. 3Jane marks down expected losses immediately: a loan 10 days past due with an expected 10% recovery is written down 90% at once. So losses would show up in the USD3 price quickly rather than being smoothed.

| Breakeven for USD3 (0% recovery) | Sudden shock | Over 12 months | Historical reference |
|---|---:|---:|---|
| Slope ($64.9M) | 13% of book | 3.9% loss per ~2-month cycle | Whole book 1.72% · worst quarter 4.82% · ex‑3 obligors 0.27% |
| Settle ($27.5M) | 31% of book | ~58% annualized | H1‑26 3.9% annualized · lifetime 1.5% |
| LendSwift ($6.6M note) | Cannot reach USD3 alone | Cannot reach USD3 alone | ~52% of gross collateral must vanish before 3Jane loses $1 |
| All FCC ($99M) | 8.6% of book | 16.5% of book per year | 3Jane docs illustrate a 19% break with a 15% junior; today's junior is 7.4% |

Slope's short loans cut both ways. Each loss only hits one ~2-month cycle, but the book turns over ~6.6× a year (~$417M of purchases at today's size). One bad month is easily absorbed. Slope's worst quarter repeated for a full year would reach USD3, unless 3Jane stops buying or tightens the box first.

---

## Liquidity

**How a USD3 holder gets out.**
1. **Primary redemption** against the liquidity sleeve: Aave + Erebor, $15.3M (13.3% of TVL) against a 15% target. No KYC. The sleeve is shared by USD3 and sUSD3 (sUSD3 unstakes to USD3, then redeems). USD3 redeems "up to the tranche ratio". sUSD3 has a 1-month lock, then cooldown.
2. **Secondary markets** (Curve and other pools). Not deep, and 3Jane says so.
3. **Asset run-off.** Both forward flows are uncommitted, so 3Jane can stop buying and let the books amortize. Loans can't be called early, but they're short.

**[Chart 10 · Pool liquidity ladder]** `charts/10-pool-liquidity-ladder`

| If 3Jane stops buying | Cash available | % of pool |
|---|---:|---:|
| Today | $15.3M | 13% |
| 30 days | $49.2M | 43% |
| 60 days | $75.6M | 66% |
| 90 days | $92.7M | 80% |
| 180 days | $106.1M | 92% |

**Design choices that matter.**
- **No idle cash.** Deposit caps are raised only in line with deployment and fill in ~10 minutes. That's good for yield, but the sleeve is the only buffer.
- **Committed outflows.** ~$3.1–3.4M of undrawn LendSwift commitment.
- **Can't sell loans quickly.** Slope loans can't be sold without Slope's consent, so liquidity comes from run-off, not loan sales. They can be pledged to a lender, which leaves room for a future liquidity facility.
- **Ideas not live.** "Inverse LCC" for redemptions is under discussion (3Jane offsite next week; they flag wrong-way risk). Committed liquidity facilities are on the roadmap.

| Morpho market (Ethereum) | LLTV | Borrowed | Borrow APY |
|---|---:|---:|---:|
| USD3 / USDC | 91.5% | $10.2M | 6.43% |
| PT‑USD3‑17DEC / USDC (a) | 86% | $17.3M | 8.73% |
| PT‑USD3‑17DEC / USDC (b) | 86% | $14.5M | 6.34% |
| PT‑USD3‑17DEC / USDT | 91.5% | $11.4M | 3.49% |
| USD3l / USDC (LCC loops) | ~similar, slightly lower | Not live | — |

---

## Risks

### 1. Liquidity risk (main risk)

- **What can go wrong.** Redemptions above the 13% sleeve, with thin secondary liquidity. Holders then wait for run-off (30–60 days for most of the book) while USD3 trades at a discount on secondary markets. NAV isn't lost, but exit is delayed and the price on screen depegs.
- **The amplifier is leverage.** About half of TVL is looped (~$53M of USDC debt against USD3 and PT‑USD3), sized largely for JANE farming. Loopers are diversified (no single 20% holder), but they react to the same signals. If USD3 underperforms (a loss, a yield drop) or borrowing gets expensive (the Morpho markets already run at 86–91% utilization), loops stop paying and unwind together. Each unwind redeems USD3 into a sleeve sized for ~13%. 3Jane itself doesn't like how loop-dependent the TVL is.
- **Scheduled pressure points:**
  - **PT‑USD3‑17DEC2026 maturity**, with ~$43M of Morpho debt against it.
  - **JANE TGE.** December per Trenches, "very early next year" per Jeremy. Incentives and loop economics change after it.
- **Mitigants:**
  - Very short assets.
  - Uncommitted forward flows (3Jane controls the run-off tap).
  - Slope repaying ~$45M in Nov–Dec, which happens to line up with the PT maturity.
  - Immediate markdowns, so the price stays honest.
  - No KYC on exit.
- **For Re7:** USD3 belongs in the **1-month liquidity bucket**, not instant liquidity. Exit in a stress scenario relies on run-off, not on the sleeve.

### 2. Default risk

- **Where it sits.** 80% of backing is owned loans with no OC. The only buffers are loan yield and a 7.4% junior. A sudden loss of 8.6% of the FCC book reaches USD3.
- **What drives it.** Concentration. Bad vintages come from one big obligor, not from loss rates rising across the book. That's why the obligor caps (by tier and merchant) and tier exclusions matter most.
- **Contract strength.** The Slope sale agreement only protects the condition of loans at sale. There's no EPD putback, no protection against later credit deterioration, a 101.5% price, and a capped remedy. Settle's terms are stronger (EPD putback, whole-book reps), but its repurchase depends on a thinly capitalized originator.
- **Recoveries.** ~0% on Slope, modest on Settle (median 6 months, single digits to mid-teens). Underwrite on gross losses.
- **Macro.** All of it is US credit. Slope is the most cyclical, Settle less so, and LendSwift sees more demand in a downturn. 3Jane calls this a major risk that is hard to hedge, and is diversifying into settlement-float facilities whose risk is unrelated to credit (funds backed 1:1).
- **Fraud or originator failure.** LendSwift is covered by bad-boy guarantees (slow recovery); Slope and Settle by reps and indemnities (capped, except for fraud). Originator financials are refreshed only every 6–12 months.

### 3. Other risks

| Risk | Detail |
|---|---|
| Thin junior | sUSD3 is 7.4% vs the 15% in 3Jane's own example; the minimum isn't disclosed |
| Legal chain | Slope buyer is "3Jane Capital Corporation" (confirm it's an SPV); LendSwift exposure runs through a Percent participation and an SPE with no independent manager |
| Servicers | Slope keeps servicing, and loans can't be sold without its consent; LendSwift has only a cold backup; Settle has Nelnet as backup |
| Regulatory | LendSwift's ~690% APR with 59% of balance in Texas |
| Governance | 3Jane sets the tranche income split, deposit caps, call timing and size; it can pause LCC and revoke positions; 7-day upgrade timelock |
| Smart contract | Audits: Veridise, Sherlock, Electisec (core); Guardian (LCC, plus the looping helper on 27 Oct) |
| Token | JANE supply 1.1–6.7B, final mint pending; part of LCC yield depends on JANE value and liquidity |

---

## Opportunity for Re7: LCC

**How it works.**
- Post margin (7.5% of the commitment) and promise to deliver USDC when 3Jane calls.
- 3Jane pays a fee on the commitment, sent weekly in USDC. The margin keeps earning Aave yield.
- On a call you have 9 days to deliver USDC. You receive USD3 (not sUSD3) with a 35-day cooldown, and the matching margin is released.
- Missing a call slashes the margin into a backstop auction.

**Why we don't count on looping.** The USD3l/USDC Morpho market isn't live. Parameters are similar to the USD3 market (slightly lower LLTV), but there's no date and no supply side yet. The existing USD3/USDC market borrows at 6.43% against USD3 at 6.30%, which is negative carry. The private deal also bars using called USD3 in DeFi without approval. **So the options are spot LCC or the private deal.**

### Public LCC vs the Trenches private deal

| | Public LCC | Trenches LCC LP Deal |
|---|---|---|
| Access | App; $1M promise cap per address, one position per address | Via Trenches (separate Telegram group, capital calls pinged there) |
| Minimum | $25k promise | $100k commitment / $7.5k margin |
| Term and exit | Perpetual; exit ≥2 epochs (42+ days) through a per-epoch cap, callable meanwhile | Fixed: 4 call windows (78–99 days); margin locked, released manually at the end; then rolls into public terms |
| Margin yield, uncalled | ~3.5% Aave + 16.7% USDC fee = **20.2% hard** + variable JANE (app shows ~21% at a $250M FDV) | ~4% Aave + 12% USDC + 18% JANE = **~34%**, of which **16% hard** |
| JANE | Variable emissions | Fixed 18% APY, valued at a 3-day TWAP after TGE; 3-day cliff + 7-day linear vest |
| If called | USD3 at organic yield + 0.75% for 35 days (~6.4% hard) + USD3 emissions | USD3 at a **fixed 18% for up to 70 days** (organic ~6.3% + JANE top-up); 35-day cooldown |
| Notice | Announced in app / Telegram; 9-day funding window | 3 days' notice + 9-day funding window (12 days) |
| Called USD3 in DeFi | Allowed | Not allowed unless approved |

The private deal pays **less hard USDC on margin than public LCC** (16% vs 20.2%). Its edge is the fixed-value JANE and the fixed 18% on called capital for 70 days. Its cost is the 78–99-day lock.

### Scenarios (per $1M commitment, private deal)

What we earn depends on whether and when we're called, and on what JANE is worth.

| Scenario | Capital deployed | Income | Annualized, total | Hard USD | JANE at −50% |
|---|---|---:|---:|---:|---:|
| No call (90 days) | $75k margin | $6.3k | **34.0%** | 16.0% | 25.0% |
| 50% called in window 1 | $75k → $37.5k margin + $500k USD3 for 70 days | $21.1k | **19.7%** | 7.3% | 13.5% |
| Fully called in window 1 | $75k for 21 days + $1M USD3 for 70 days | $36.0k | **18.4%** | 6.5% | 12.4% |
| Fully called in window 4 | $75k for 84 days + $1M USD3 for 70 days | $40.4k | **19.3%** | 7.1% | 13.2% |

*Assumptions: USD3 organic 6.3%, Aave 4%, term 90 days, called USD3 held 70 days then redeemed. "JANE at −50%" = JANE realized at half its TGE value.*

**[Chart 11 · LCC private deal scenarios]** `charts/11-lcc-private-deal-scenarios`

**Reading it:**
- **Uncalled** is the attractive state: 34% on margin, clearing the 20–25% private-deal hurdle even with JANE at half value. But the capital at work is small ($75k per $1M). As an add-on to the $1M we keep liquid anyway, it's worth about **+2.5% annualized** (+1.2% hard).
- **Called** turns into $1M of USD3 at a fixed 18% for 70 days. That clears the 12–15% standard hurdle with JANE, falls just short of 20%, and is only ~6.5–7% in hard USD.
- **A call during the term is likely.** wumpy said the first call would come at least two epochs after 27 Oct, with up to ~$15M per call. Jeremy wants to fund the next big deployment through LCC rather than by raising caps. So underwrite the **called** case: ~18–20% total, ~60% of it JANE.
- **The real risks are JANE and the lock.** The JANE component is valued at TGE (December or early 2026) and then vests over 10 days, so price and liquidity at TGE matter. Called USD3 carries full senior credit and liquidity risk, can't be used in DeFi, and has a 35-day cooldown.

**Open points on the deal:**
- Maximum size, and whether the $1M per-address cap applies.
- Any Trenches fee.
- What happens if TGE slips past the term.
- Whether the fixed 18% post-call return holds if USD3 takes a principal loss. It fixes yield, not principal.
- How the margin is returned at the end of the term (manual process).

**View.** The private deal is a short, JANE-heavy way to get senior USD3 exposure at an attractive headline rate. On hard USD alone it's roughly USD3 spot once called. It makes sense if (a) the IC is comfortable holding USD3 credit for ~3–5 months, in the 1-month liquidity bucket, and (b) we treat JANE as a real but discounted part of the return. Size it so a full call is capital we're happy to have in USD3.

---

## Appendix: chart files

| # | File | Shows |
|---|---|---|
| 01 | `01-backing-composition` | USD3 backing by asset |
| 02 | `02-slope-losses-by-quarter` | Slope realized losses: all loans vs ex-3 obligors vs eligibility box |
| 03 | `03-slope-repayment-schedule` | Slope scheduled cash back by month |
| 04 | `04-settle-loss-drivers` | Settle loss rates by segment vs 3Jane EL and breakeven |
| 05 | `05-settle-repayment-schedule` | Settle scheduled cash back by month |
| 06 | `06-lendswift-borrowing-base` | LendSwift collateral → haircuts → coverage |
| 07 | `07-lendswift-delinquency` | LendSwift DPD distribution |
| 08 | `08-lendswift-collections-by-vintage` | LendSwift cash collected by vintage |
| 09 | `09-lendswift-payoff-schedule` | LendSwift collateral by payoff month |
| 10 | `10-pool-liquidity-ladder` | Pool cash if 3Jane stops buying |
| 11 | `11-lcc-private-deal-scenarios` | LCC private deal return by call scenario |

Each chart has an `.html` (interactive, light and dark) and a `.png` (2×, light) in `charts/`. `build_charts.py` regenerates the HTML files.
