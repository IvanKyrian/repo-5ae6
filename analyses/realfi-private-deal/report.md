# RealFi Private Deal: USDrf Allocation (12% cash + 8% RFG)

**Date: 26 Nov 2026**

**Strategy category: Private deal: fixed-rate allocation backed by tokenized T-Bills and AAA CLOs**

**Expected Yield: 12% p.a. fixed in USDC + 8% p.a. in RFG tokens (valued at 0 for underwriting)**

**Protocol exposure: RealFi Reserve Ltd. (USDrf issuer), Ondo OUSG, Janus Henderson Anemoy jAAA (Centrifuge), HT Digital (5th signer), Safe{Wallet}**

**Size: $5M (term sheet range; RealFi said $5–10M is possible)**

**Term: 2 months from mint (target mint: first two weeks of December 2026)**

---

#### **TL;DR**

- RealFi wants $5M of USDrf minted on Ethereum around its EVM launch. Our USDC is not put into their lending book. It goes 1:1 into **~60% OUSG / ~40% jAAA** held in a **dedicated 3-of-5 Safe**: 2 keys Re7, 2 keys RealFi, 1 key HT Digital.
- We get **12% p.a. fixed in USDC**: ~4.5% from the backing assets' own yield plus a ~7.5% "delta" paid by the RealFi Foundation. On $5M for 2 months that is **~$100k**, of which **~$62.7k is the delta**. The Foundation has offered to **pre-fund the full delta into a separate wallet at inception**.
- We also get RFG equal to **8% p.a. (~$66.8k)**, priced at the 7-day VWAP after TGE (or a floor price, whichever is higher). The tokens are fully unlocked. **We value this at zero.**
- **Risk-adjusted, the deal is very strong.** We earn 12% in cash over two months on T-Bills and AAA CLOs held spot, with no leverage and no liquidation risk. The yield on the assets themselves is about 4.5%, so RealFi is paying for TVL and launch liquidity. It is not paying us to take credit risk.
- **What we are trusting:** (1) HT Digital signs according to the agreement, and (2) the legal documents actually ring-fence our Safe. **(2) is not true today** (section 4, Q3). The term sheet says the Safe assets *"remain owned and held within the RealFi fund"* and that our USDrf ranks *"pari passu with other unstaked USDrf"*. The standard Minting Agreement doesn't mention the Safe at all. The protection is operational (keys), not legal. This is fixable in the side letter, and it is requirement #1.
- **Recommendation: go ahead with $5M**, conditional on the requirements in section 5: legal ring-fencing, an HT Digital signer agreement, the pre-funded delta and payment at maturity directly from the Safe.

---

#### **1. RealFi Protocol Overview**

**Origin.** RealFi was incubated inside **Input Output Global (IOG)**, the engineering company behind Cardano, founded by Charles Hoskinson. The team has been doing this since 2023 as an IOG project: Sahil's and Harry's CVs list "RealFi, Input Output Global", and the Fin Kenya DD report from Feb 2026 is signed by "IOG Singapore Pte. Ltd. (RealFi)". In 2026 it was spun out into its own structure; the RealFi Foundation was incorporated on 1 April 2026. It is backed by IOG through the **Hoskinson Family Office**, which per their DDQ answer *"has committed $13M of launch capital and funds operations"*. IOG is also the Foundation's lender (credit facility, see section 3). Hoskinson has publicly made RealFi a flagship for Cardano DeFi, with a stated goal of more than $1B in TVL.

**Product.** A yield-bearing stablecoin protocol:
- **USDrf**: a stablecoin pegged 1:1 to USD. Institutions mint and redeem it 1:1 against USDC or fiat after KYB and whitelisting. Retail users can only buy it on DEXs.
- **sUSDrf**: staked USDrf with a 7-day unstaking cooldown. It targets 8–10% net APY from the reserve portfolio. Its structure resembles Ethena's (stake and cooldown); its yield source does not.
- **RFG**: a governance token with fixed supply. TGE is expected in Q1 2027; they say Kraken has approved it and they are in talks with other CEXs and market makers.

**Reserve / yield engine.** Two "books" and four "sleeves":
- **Sleeve A** (≥45% of Book 1): tokenized money-market funds and T-Bills (OUSG etc.), ~3.6% gross.
- **Sleeve B1**: AAA/BBB CLO ETFs (jAAA), ~6.2% gross. Sleeve B2 (investment-grade corporate bonds) is dormant.
- **Sleeve C**: their own **direct lending to emerging-market fintechs**, which lend to SMEs and salaried workers in Kenya, Zambia, Nigeria, Ghana, LatAm and Southeast Asia. Loans are senior secured on the borrowers' loan books, tenors are 6–12 months, and gross yields are ~13–17%. Target is 30–40% of NAV, with a hard cap of 50%. Book 1, which backs unstaked USDrf, may hold up to 40% private credit.

**Legal structure.** At the top is the **RealFi Foundation**, a Cayman foundation company with no shareholders, supervised by DS Limited. It wholly owns:
- **RealFi Reserve Ltd.** (BVI), which issues USDrf and is the *Senior LP* in the fund.
- **RealFi Alpha Ltd.** (BVI), which issues sUSDrf and is the *Junior LP*.
- **RealFi Governance Ltd.** (BVI), which issues RFG.
- **RealFi GP Ltd.** (Cayman), which manages **RealFi Private Credit Master Fund, L.P.**, a Cayman exempted LP registered with CIMA. This fund holds **all** reserve assets: T-Bills, CLOs and private credit.

Service providers: fund administration by NAV Fund Services (the deck says Maples); custody by BitGo, BNY and IRACE; execution through StoneX; KYB through Autonomous; monthly proof-of-reserves by HT Digital. Legal counsel: Walkers (BVI/Cayman) and Skadden (jurisdiction analysis).

**Traction.** Cardano mainnet launched on 1 Oct 2026. USDrf market cap is **~$5.6M** (24 Nov). John said **three institutional wallets hold ~90%** of deposits and one of them will add $7.5M in the next weeks, taking them to ~$12M. Our reading is that most Cardano TVL is sponsor-related capital. The total Cardano stablecoin market is only ~$70M, which is why they are **moving to EVM**. Ethereum mainnet goes live on 30 Nov / 1 Dec. The Cardano and EVM deployments are native and separate, with a LayerZero connection planned for January. EVM distribution plans: an Euler vault with Alphagrowth for sUSDrf looping, Uniswap pools, and a Morpho market with PAXG; RedStone provides the NAV and PoR feeds. **This private deal of up to $5M (expandable to $10M) is their launch-liquidity tool on EVM.**

They are well behind the deck's own plan (Q3: $50M TVL, Q4: $100M). That doesn't affect our deal, but it explains why they are paying 12% for TVL.

---

#### **2. Team, Backers & Investors**

**Sponsor: IOG / Hoskinson Family Office.** IOG is one of the best-funded organizations in crypto, and Hoskinson personally promotes RealFi. They have provided:
- **$13M of committed launch capital** (DDQ).
- A **$6.44M committed credit facility** to the Foundation at 5.94%, maturing 31 Dec 2027, of which ~$2.25M is drawn. Interest is capitalized.
- The TechCo (engineering, product and data, 17 FTEs) is still **"owned by IOG"** per the Operational Overview.

John said they had raised **$9.5M in total**. The Foundation's balance sheet shows no equity line, only the IOG loan, so we should ask what the $9.5M refers to; it may be IOG's spend during incubation. Our reading is that the sponsor's reputation and money are heavily tied to RealFi's success, which is a strong alignment signal. The sponsor is also not a classic VC syndicate: we don't see third-party institutional equity.

**Executive team** (reviewed from the CVs in the data room):

| Person | Role | Background | Our read |
| --- | --- | --- | --- |
| **John O'Connor** | CEO & founder (Nairobi / London) | Oxford PPE. First hire at the Cardano Foundation (Head of Strategy, 2017–18). **Commercial Director at IOHK, 2018–23**: led the Ethiopia Ministry of Education 5M-user digital ID pilot and helped design the bitcoin-wallet project later used in El Salvador. Partner at Lighthouse Capital (crypto multi-manager). Earlier career in ad-tech analytics. | A credible, well-known Cardano ecosystem operator. Not a credit or TradFi person. |
| **Dynal Patel, PhD** | CPO (Cape Town) | **CPO at IOG, 2019–23**: ran an 80-person product org, Atala PRISM and Project Catalyst ($70M+ in grants). VP Product at Wanchain (a cross-chain bridge). ~6 years at Vodafone (co-created the eSIM spec; holds a patent). PhD in CS from UCT. | A senior, verifiable product leader. |
| **David Kleiterp** | CIO / Director of Investments & Capital (Nairobi) | Per the deck and public profiles: ex-**Abraaj** (Associate, 2015–18), Principal at **54 Capital**, **Head of Investments Africa at Untapped Global** (revenue-based financing to EM fintechs), and founder of **Mobilis Capital Partners**, which deployed $7M at a stated 23% IRR. They claim "$600M+ of transactions sourced, structured and managed at 20%+ realised IRRs". | The key credit person. **His CV is not in the data room.** The $600M claim is large for an Associate/Principal-level career, so we should get a CV and references. Abraaj collapsed in a 2018 fraud case; he was a junior Associate and nothing links him to it, but IC may ask. |
| **Sahil Shah** | COO / Director of Strategy & Operations (Nairobi) | Ran RealFi's investment operations inside IOG from 2023. Head of Strategy at Mara (crypto, Kenya/Nigeria). Associate at EG Capital (PE and mezzanine in East Africa). Consultant to IFC, the World Bank and the Central Bank of Kenya. Director at Image Registrars (Kenya). Bristol (First), Strathmore MPP. | A solid East-Africa operator. Runs the Cayman/BVI fund operations. |
| **Seny Orlov** | Head of GTM (London) | 6 years at **Morgan Stanley** (FIG/FinTech ECM, VP). R3. **Keyrock** (strategic partnerships). **Lisk** DeFi Growth Lead (grew TVL from under $1M to over $30M). LBS MBA. | A strong DeFi BD profile. **Royce has worked with him before**, which gives us a direct reference. |
| **Shawn Singh** | General Counsel / director of the GP (Houston) | Per the deck: 30 years as GC/CCO at Luminus, DW Partners and Cheyne Capital; Regulatory Counsel and Global CCO at Guggenheim; led Brevan Howard's US spin-out. | A strong profile on paper. **No CV in the data room**, and public confirmation was thin. |
| **Leonidas Tsagkalias** | Head of Finance / director of the GP (Athens) | **At IOG since 2016**: Treasurer, Global Financial Controller, Africa Operations Manager. Earlier a bank credit analyst. Vlerick MBA. | IOG finance insider. His CV still shows IOG as his current employer. |

**Engineering & credit bench:**
- **Nathan Rhoda**, Head of Engineering: 15+ years; Digital Asset Lead at Absa.
- **Dr. Jann Müller**, Engineering Lead (IOHK): Plutus compiler engineer, co-author of the eUTxO multi-asset papers with Philip Wadler, and **engineering lead on the Djed stablecoin at IOG (2023–25)**. A top-tier Cardano engineer.
- **Harry Plumstead**, Senior Credit Analyst: CFA charterholder; 5 years in private credit at Louw & Co.
- **Clay Crosby** and **Olivier Herlem**, product and data: both ex-Untapped Global.
- **Liam Furman**, Data Science: ex-Meta and Booking.com.
- About 30 people in total, mostly in Cape Town and Nairobi.

**Advisors / IC:**
- **Paul Tregidgo**: 32 years at Credit Suisse, latterly Vice Chair of DCM. Verifiable on Blue Haven Initiative, the Center for Financial Inclusion and FINRA BrokerCheck.
- **Steven McClurg**: founder of Canary Capital; co-founder of Valkyrie.

We could not independently confirm on the web that either is involved with RealFi, so we should confirm through references.

**Track record.** They report $11.5M deployed across 40+ disbursements to 25+ borrowers in 10+ countries:
- $7M at Mobilis, at a 23% IRR.
- $4.5M at RealFi since 2023, at a 15.96% IRR, with "zero loss events".

The figures are unaudited and include unrealized positions. *This doesn't affect our deal, because we have no exposure to the lending book.*

**External references.** Jordan knows the founder personally and has had positive feedback, including from a mutual contact, with no red flags so far. HT Digital is also Re7's accountant (see section 4).

**Overall view:** this is a reputable, long-standing team. They have done EM credit inside IOG for ~3 years and are now taking it on-chain with heavy sponsor backing. The weak points are the documentation gaps (CIO and GC CVs, audited track record) and a small, early book, but neither is relevant to our ring-fenced exposure.

---

#### **3. What's the Opportunity**

**The deal in one sentence:** we lend RealFi our balance sheet for two months to show TVL at their Ethereum launch. In exchange we hold T-Bills and AAA CLOs in a wallet we co-control and get paid 12% instead of ~4.5%.

**Flow of funds**

1. **Onboarding.** Re7 completes KYB with RealFi Reserve Ltd. and gets an EVM minting address whitelisted. A dedicated Ethereum **Safe (3-of-5: Re7 ×2, RealFi Treasury ×2, HT Digital ×1)** is deployed and allowlisted with Ondo (OUSG) and Centrifuge/Anemoy (jAAA). RealFi's fund is already a verified OUSG purchaser.
2. **Mint.** Re7 sends **$5M USDC to RealFi Reserve**, and the Reserve mints **5M USDrf** to our wallet. We hold them unstaked for the whole term; they can't be redeemed early.
3. **Investment.** The Reserve invests the USDC as Senior LP into the RealFi fund, which places it in the **Safe** and buys **~$3M OUSG (60%) and ~$2M jAAA (40%)**. The Safe holds only our allocation.
4. **During the term.** Daily valuation at each issuer's NAV, no haircut. Monthly proof-of-reserves by HT Digital. Coupons are paid monthly or as a bullet: ~4.5% p.a. from the Reserve under a side letter (the yield the Safe assets earn), plus a **~7.5% p.a. delta from the Foundation out of a pre-funded, segregated wallet**.
5. **Maturity.** The signers redeem the assets (jAAA requested a few days early, since settlement is typically T+3; OUSG is near-instant). The USDC goes to RealFi Reserve, our USDrf is redeemed at par and burned, and the final coupons are paid.
6. **RFG.** Tokens equal to 8% p.a. on $5M, delivered 7 days after TGE (Q1 2027 expected), fully unlocked.

**Returns on $5M, 61 days, Act/365**

| Component | Rate | $ | Paid by | Secured by |
| --- | --- | --- | --- | --- |
| Backing yield | ~4.5% | ~$37.6k | RealFi Reserve (side letter) | The Safe assets themselves |
| Delta | ~7.5% | ~$62.7k | RealFi Foundation | Pre-funded segregated wallet (proposed) |
| **Total cash** | **12.0%** | **~$100.3k** | | |
| RFG | 8.0% | ~$66.8k at the reference price | RealFi Governance | Nothing. Valued at **0** |

**Why it makes sense for the fund:**
- **Our exposure is to OUSG and jAAA, not to RealFi's lending book.** The design segregates our assets in their own Safe, valued and attested separately. Economically, if the private-credit book went to zero we would not care: the losses sit with sUSDrf (junior) and with other USDrf backing, and our Safe still holds T-Bills and AAA CLOs. *Caveat:* the legal documents need to say this explicitly (section 4, Q3, and requirement #1).
- **OUSG is new for the fund but very simple:** short-dated US Treasuries through BlackRock BUIDL and other government money-market funds, KYC-gated, with a transfer allowlist. **jAAA we know well** from the deJAAA loop work. Here it is **spot, unlevered**, so there is no liquidation risk at all, unlike the loops we passed on.
- **The trust assumption is narrow:** HT Digital, as the independent 5th signer, acts according to the agreement.
- **Two months only**, with the delta pre-funded.
- **It builds the relationship.** If we're comfortable after the term, the natural next step is curating an sUSDrf vault on Euler/Morpho. sUSDrf yields ~9–12% against ~10% borrow, and RealFi could direct RFG or points to our vault. Jordan is also exploring Re7 products as part of RealFi's yield mix and a Cardano mandate.

---

#### **4. How can we lose money? (Q&A)**

**Q1. What if the protocol is exploited, for example someone mints unbacked USDrf on Ethereum?**
A: It doesn't touch our assets. The backing is in a separate Safe that the USDrf contracts have no control over, and the wider reserve is held off-chain with custodians (BitGo, BNY). Minting is permissioned: KYB'd and whitelisted institutions only, 1:1 against USDC received. Minting auto-suspends if backing falls below 100%, and mints or redemptions above $2M need manual approval. Our USDrf is just a claim. Even if the USDrf contract were paused or broken, our exit runs through the Safe (Re7 2 keys + HT 1 key). *Residual:* an exploit that leads to a group insolvency brings us back to the legal point in Q3. The EVM audits are reported inconsistently (TxPipe/Sherlock on the call, Anastasia Labs in the DDQ, "in progress" in the term sheet), so we should ask for the final reports.

**Q2. Can someone drain the whole reserve?**
A: Not our part. The main reserve is off-chain, with custodians, the administrator and bank mandates. Our assets are in our own Safe, where **any movement needs 3 of 5 signatures across at least two organizations.** RealFi alone has 2 keys and can't move anything. To steal the funds, an attacker would need keys from RealFi **and** HT Digital, or from Re7 **and** HT Digital. Compromising RealFi alone is not enough.
*Hardening we should ask for:* a Safe Guard or Zodiac Roles setup so that the Safe can only send to the Ondo and Centrifuge redemption contracts, the Re7 address and the RealFi Reserve address. No other modules, and no owner or threshold changes, during the term. That way even 3 colluding keys can't send the assets to an arbitrary address.

**Q3. What if RealFi's lending book goes to zero?**
A: **Economically, we don't care.** Our allocation is backed 1:1 by its own OUSG and jAAA in its own Safe and has no exposure to Sleeve C. The book's losses fall first on sUSDrf (the Junior LP). Operationally, the 3-of-5 means RealFi can't use our assets to plug a hole without HT Digital.
**But today this rests on keys, not on law, and that is the one real hole we found:**
- The **term sheet (§18)** says the Safe assets *"remain owned and held within the RealFi fund"*: the same Cayman LP that holds the private-credit book.
- The **term sheet (§19)** says our USDrf ranks *"senior to sUSDrf… pari passu with other unstaked USDrf"*. If losses exceed the sUSDrf tranche, we share them with all other USDrf holders. Book 1, which backs other USDrf, may hold up to 40% private credit.
- The **Minting Agreement** gives us only an unsecured claim on RealFi Reserve (*"USDrf only represents your right to require the Company to redeem USDrf for an equivalent amount of U.S. dollars"*, §2) and **doesn't mention the Safe, HT Digital or segregation at all.**
- The FAQ talks about "segregated cells" and a "Cayman SPC", but the entity one-pager says the fund is an **exempted LP**, which has no statutory cell segregation.

In a fund or Reserve insolvency, a Cayman or BVI liquidator could treat the Safe as a general fund asset. HT Digital would follow a court order, not our side letter.
**The fix (requirement #1):** the side letter, LPA and fund documents must ring-fence the Safe for our allocation. That means one or more of the following: a separate class, segregated portfolio or SPV; a perfected security interest over the Safe assets in Re7's favour; or explicit limited-recourse wording so that no other LP or creditor has recourse to them. Walkers should confirm it in a legal opinion, and our USDrf should be carved out from the pari passu ranking.

**Q4. What if HT Digital doesn't do what was agreed, i.e. doesn't release coupons or our principal at maturity?**
A: We would rely on a **legal contract under which HT Digital must sign according to pre-agreed instructions**: at maturity, or on our instruction after an event of default. With HT's key we hold **3 of 5 and can exit without RealFi.** The trust assumption sits here.
What we know about HT Digital (ht.digital): it was spun out of **Harris & Trotter LLP** (a London accountancy and BKR member, not a law firm) in 2023 and raised $10M at an $85M valuation. It provides independent proof-of-reserves for Chainlink PoR and Falcon Finance (USDf). **It is also Re7's accountant and our registered office (per Jordan) and RealFi's paid PoR attestor**, so it has commercial relationships with both sides. That is reassuring in that a reputable regulated firm won't side with fraud, but we need it in writing.

**Q5. What if someone steals the keys?**
A: They would need **3 keys from at least two organizations**. Stealing both of RealFi's keys is not enough; they would also need either HT Digital's key or both of ours. With the Safe Guard in Q2, even that only lets them send assets to pre-approved addresses. We should check how HT stores its key (HSM or MPC, with dedicated signers).

**Q6. What if OUSG or jAAA lose value?**
- **OUSG:** a short-dated US Treasury fund held through government money-market funds (BlackRock BUIDL and others). It is KYC-only: holders must be allowlisted, and Ondo controls mint, redeem and transfer permissions. That makes it hard to "hack" in the usual DeFi sense. A hacker can't sell it to anyone who isn't KYC'd, and Ondo can freeze or stop redemptions. The realistic tail risks are operational: the issuer pausing redemptions (for example if BUIDL paused, or USDC depegged), not credit. **Price risk ≈ 0.** *(We couldn't load ondo.finance from our environment; check fees, limits and current APY on the Ondo docs.)*
- **jAAA:** Janus Henderson Anemoy AAA CLO Fund on Centrifuge, a BVI SPC managed by Anemoy with Janus Henderson as sub-advisor. AAA CLO tranches have never defaulted, but they can mark down in a liquidity shock. Our own deJAAA model gives these drawdowns. Applied to the **$2M jAAA (40%), spot**:

| Scenario | Drawdown | jAAA MTM loss | Net P&L over 2 months, delta pre-funded (12%) | Net P&L if delta not paid (4.5% only) |
| --- | --- | --- | --- | --- |
| Anemoy fund max DD (Mar-26) | 0.22% | −$4.4k | **+$95.9k (+1.92%)** | +$33.2k (+0.66%) |
| JAAA ETF max DD | 2.60% | −$52.0k | **+$48.3k (+0.97%)** | −$14.4k (−0.29%) |
| COVID AAA CLO (LlamaRisk) | 8.33% | −$166.6k | **−$66.3k (−1.33%)** | −$129.0k (−2.58%) |
| Extreme stress | 10.00% | −$200.0k | **−$99.7k (−1.99%)** | −$162.4k (−3.25%) |

*How to read it:* redemption is at **par**, so a jAAA markdown is in the first instance **RealFi Reserve's** shortfall to cover, not ours. We would only take the loss above if RealFi *also* fails to pay par **and** we are forced to sell at the trough at maturity. Even then, the worst case is about −2% of the allocation. *Mitigants to negotiate:* (a) an option to **extend the term or take jAAA in kind** if jAAA trades below NAV at maturity, since AAA CLOs recover; (b) a higher OUSG share; (c) a mark-to-market top-up from RealFi if jAAA's NAV drops more than ~1%.

**Q7. What if the Foundation disappears or goes bankrupt?**
A: The Foundation's **only** obligation to us is the delta (~$62.7k), and it has offered to **pre-fund the full amount into a segregated wallet at inception.** If that wallet is multisig with our keys, Foundation credit risk on the top-up is gone. The principal and the 4.5% sit with RealFi Reserve and the Safe, which are separate entities. *Context:* the Foundation's unaudited balance sheet at 31 Oct shows total assets of $1.45M, including ~$1.12M liquid (mostly OUSG), and $4.19M undrawn on the IOG facility. Its net position is negative at −$0.91M because of the drawn IOG loan, which matures in Dec 2027 with no near-term debt service. The delta is ~5.6% of its liquid resources. If the *whole group* fails, we are back to Q3: our recourse is the Safe, which is why the legal ring-fencing matters.

**Q8. (Added) What if the redemption at maturity fails or is delayed?**
- jAAA settles T+3 per the term sheet, and same or next day per other sources, so request it early.
- OUSG redemption depends on Ondo and BUIDL liquidity.
- Redemption is in USDC, so there is a small USDC depeg risk.
- **Bigger point:** under §20 the USDC goes from the Safe **to RealFi Reserve first** and then to us. For that moment it leaves joint control. We should require **delivery-versus-payment straight from the Safe to Re7** against our USDrf burn, or in-kind delivery of OUSG and jAAA.
- *Backup exit:* we're already onboarded with Ondo for OUSG, but **not yet with Anemoy for jAAA** (we only have the MNDA from July 2026). We should complete Anemoy onboarding so that in-kind delivery is possible. Also note that the issuers' KYC relationship is with RealFi's fund, not with us. In a dispute, Ondo or Anemoy could freeze based on instructions from the legal owner. That's one more reason to fix the legal ownership (Q3).

**Q9. (Added) Can RealFi change the terms or close our account?**
On the standard Minting Agreement, yes:
- §6: they can close an account *"for any or no reason"*, with *"forfeit[ure of] all proprietary rights and claims… in relation to any assets otherwise eligible for redemption"*.
- §8: they can suspend redemptions for many reasons, including a catch-all.
- §14: their liability is **capped at $100**.
- §17: they can amend the agreement unilaterally.
- §18: they can assign it freely.
- §1 and §20: the **US, UK and EU are Restricted Jurisdictions**, so our contracting entity has to be eligible.
- §8: the agreement is written for **Cardano** addresses only.

All of this must be overridden by the side letter for our allocation (requirement #1).

---

#### **5. Key Requirements before signing**

1. **Legal review by Kirill & Chris.** Give them this memo, the term sheet, the Minting Agreement, the entity one-pager and the Foundation note. Ask them to look for any flaw, weak point or wording that could hurt us, specifically:
   - **Ring-fencing of the Safe** (Q3): segregated class, portfolio or SPV, or a security interest; limited recourse; carve-out from "pari passu with other unstaked USDrf"; Walkers opinion.
   - **Side-letter overrides** of Minting Agreement §6, §8, §14, §17, §18 and §22 (Q9), and confirmation that the 12% is fixed whatever the actual backing yield.
   - **Unconditional redemption at maturity** with **DvP from the Safe straight to Re7**, plus an extension or in-kind option in a jAAA stress (Q6, Q8).
   - **Contracting entity**: which Re7 vehicle signs, and whether it's eligible given the UK/EU/US restriction.
   - **The tri-party signer agreement with HT Digital**: when it signs, on whose instruction, what happens if RealFi and Re7 conflict, and how a liquidator's request is handled.
2. **Call with HT Digital.** Confirm in writing that they will act strictly on the agreed instructions, including signing with Re7 at maturity or after an event of default without RealFi. Get their key-management setup (HSM/MPC, signers, response time), liability and insurance, and how they handle their relationships with both Re7 and RealFi.
3. **Financials / ability to pay.** The Foundation sent unaudited financials as at 31 Oct 2026: ~$1.12M liquid (cash, stablecoins and OUSG) plus a $4.19M undrawn IOG facility. That comfortably covers a ~$62.7k delta. **If they pre-fund the full delta into a segregated wallet with Re7 keys, we don't need more proof.** Optionally: verify the OUSG wallet on-chain and get the IOG facility letter.
4. **Safe configuration check at deployment:** owners and threshold (3-of-5 with the right addresses), no modules or delegate calls, a Guard restricting where assets can be sent, and the OUSG/jAAA allowlist done before we mint.
5. **Backup exit:** complete Re7 onboarding with Anemoy (jAAA). Ondo (OUSG) is already done.
6. **Team references:** Jordan's references and Royce's past work with Seny. Get the CVs of David Kleiterp (CIO) and Shawn Singh (GC), and confirm the involvement of Tregidgo and McClurg.

---

#### **Annex A: What could the RFG tokens be worth?**

We don't count on them for underwriting. The mechanics matter, though, because this is **not** a classic equity kicker:

- The amount is **fixed in USD**: 8% p.a. × $5M × 61/365 ≈ **$66.8k**.
- Number of tokens = $66.8k ÷ **max(7-day VWAP after TGE, floor price)**. The floor is still blank (`[●]`) in the term sheet.
- So **upside from a high FDV doesn't accrue to us.** A higher price just means fewer tokens. The floor **only hurts us**: if RFG trades below it, we get fewer tokens than $66.8k worth. We should push for a low floor or no floor.
- Tokens are delivered **7 days after the VWAP window**, fully unlocked, so post-TGE price drift is our risk. TGE timing (Q1 2027) is not guaranteed.

Realized value under rough assumptions:

| Case | Value | Annualized uplift on $5M |
| --- | --- | --- |
| No TGE (or indefinitely delayed) | $0 | 0% |
| Price ≥ floor, sold at VWAP | $66.8k | 8.0% |
| Price ≥ floor, sold 30% below VWAP (typical post-TGE bleed) | $46.8k | 5.6% |
| Price ≥ floor, sold 50% below VWAP | $33.4k | 4.0% |
| Market at 50% of floor, sold at market | $33.4k | 4.0% |
| Market at 50% of floor, then −30% | $23.4k | 2.8% |
| Price ≥ floor, sold 50% *above* VWAP | $100.3k | 12.0% |

*Rough FDV view:* RFG supply splits 27.5% ecosystem, 27.5% protocol, 20% investors, 15% labs and 10% liquidity. If the floor were set at, say, a $100M FDV and RFG listed at a $50M FDV, we would receive half the USD value ($33.4k). If it listed at $200M, we would still receive $66.8k, just in fewer tokens. **Base case for IC: $0. Realistic if TGE happens: ~$25–50k, i.e. +3–6% annualized on top of the 12%.**

#### **Annex B: Inconsistencies in the data room (to clarify, not blockers)**

- **Fund administrator:** NAV Fund Services (term sheet, strategy note) vs Maples Fund Services (deck).
- **Custodians:** BitGo + StoneX (DDQ) vs BitGo + BNY + IRACE (strategy note).
- **EVM design:** a CCTP-fork bridge with an Anastasia Labs audit (DDQ, Sep) vs native deployments with TxPipe/Sherlock audits and LayerZero in January (call, Nov). The term sheet says the audit is "in progress".
- **Fund structure:** "Cayman SPC / segregated cells" (FAQ) vs Cayman exempted LP (entity one-pager). This matters for Q3.
- **Funding:** "$9.5M raised" (call) vs "$13M committed launch capital" (DDQ) vs an IOG loan with no equity on the Foundation balance sheet.
- **Track-record claims** ("$600M+ at 20%+ realised IRRs") are unaudited, and the supporting CVs are missing.
- **Not reviewed:** the "Viso" DD mentioned internally (we couldn't find it in Drive or email), the full Halborn pentest and the Cardano audits (not relevant to our EVM, Safe-based exposure), and the individual borrower files (Tala, 4G, Flow, Unifi, Fin Kenya), since we have no lending-book exposure.

#### **Sources**

Data room (Drive) and email: Indicative Term Sheet; USDrf Institutional Minting Agreement (23 Jul 2026); Foundation Financial Overview for Allocators (31 Oct 2026, unaudited); Private Credit Strategy Note; Entity One-Pager V2 (Walkers); Company Deck (1 Nov 2026); Operational Overview; Fund Investor FAQ; Liquid Credit Strategy V3; Org Chart; Team Track Record Summary; team CVs; RealFi DDQ responses; Re7 call (24 Nov) and call with Jordan (24 Nov); internal "JAAA Loops" stress model.

Web:
- [Stablecoin News: RealFi launches USDrf](https://stablecoin-news.net/latest-news/realfi-launches-usdrf-cardano-defi-tvl-halves/)
- [Yahoo Finance: Cardano's RealFi pays up to 9%](https://finance.yahoo.com/markets/crypto/articles/cardano-realfi-pays-9-stablecoins-211203637.html)
- [DefiLlama: RealFi](https://defillama.com/protocol/realfi)
- [Crypto Briefing: RedStone NAV feed for RealFi](https://cryptobriefing.com/redstone-nav-feed-realfi-stablecoins/)
- [The Crypto Basic: Hoskinson on RealFi](https://thecryptobasic.com/2026/07/15/hoskinson-says-realfi-will-become-a-major-tvl-and-transaction-driver-for-cardano/)
- [BKR: HT Digital appointed for Falcon Finance PoR](https://bkr.com/bkr-member-firm-ht-digital-appointed-to-provide-proof-of-reserves-assurance-for-falcon-finance/)
- [Harris & Trotter: Chainlink PoR attestations](https://harrisandtrotter.co.uk/digital-assets/news/)
- [Investing.com: Harris and Trotter Digital Assets raises $10M](https://WWW.investing.com/news/cryptocurrency-news/harris-and-trotter-digital-assets-secures-10-million-in-funding-3405938)
- [SuperReturn: David Kleiterp](https://informaconnect.com/superreturn-emerging-markets/speakers/david-kleiterp/)
- [TheOrg: David Kleiterp at Untapped Global](https://theorg.com/org/untapped-global/org-chart/david-kleiterp)
- [Blue Haven Initiative: Paul Tregidgo](https://www.bluehaveninitiative.com/about-us/meet-the-team/advisors/paul-tregidgo/)
- [Eco: OUSG deep dive](https://eco.com/support/en/articles/15254014-ousg-deep-dive-2026-ondo-s-short-treasury-fund)
- [RWA.xyz: OUSG](https://app.rwa.xyz/assets/OUSG)
- [Token Terminal: jAAA](https://tokenterminal.com/explorer/projects/centrifuge/jaaa/metrics/asset-apy)
- [Anemoy: JAAA onchain launch](https://www.anemoy.io/news/janus-henderson-anemoy-aaa-clo-onchain)
