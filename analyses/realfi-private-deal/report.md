# RealFi Private Deal: USDrf Allocation

**Date: 26 Nov 2026**

**Strategy category: Private deal (fixed rate, backed by T-Bills and AAA CLOs)**

**Expected Yield: 12% p.a. in USDC + 8% p.a. in RFG tokens**

**Protocol exposure: RealFi Reserve, Ondo OUSG, Anemoy jAAA, HT Digital**

**Size: $5M · Term: 2 months**

---

#### **TL;DR**

- We mint $5M of USDrf. The USDC goes 1:1 into ~60% OUSG and ~40% jAAA, held in a dedicated 3-of-5 Safe: Re7 ×2, RealFi ×2, HT Digital ×1.
- We earn **12% p.a. fixed in USDC**, about **$100k over 2 months**, plus **8% p.a. in RFG**. We value the RFG at zero.
- **Risk-adjusted, the deal is very good.** We hold T-Bills and AAA CLOs spot for 2 months, with no leverage and no exposure to RealFi's lending book, and get paid 12% instead of ~4.5%.

---

#### **1. RealFi Protocol Overview**

**Origin.** RealFi was incubated inside **IOG** (Cardano) from 2023 and spun out into its own structure in 2026. It is backed by IOG through the Hoskinson Family Office. It launched on Cardano in October 2026 and now wants to grow on EVM. This private deal is how it starts on Ethereum.

**Product.** A yield-bearing stablecoin:
- **USDrf**: a 1:1 USD stablecoin. Only KYB'd institutions can mint or redeem it.
- **sUSDrf**: staked USDrf, targeting 8–10% APY, with a 7-day cooldown.
- **RFG**: governance token, TGE expected in Q1 2027.

**Reserve / yield engine.** The reserve is split in two:
- **Liquid part:** tokenized T-Bills (OUSG) and AAA CLOs (jAAA).
- **Private credit:** their own direct lending to emerging-market fintechs (Africa, LatAm, Southeast Asia). Loans are senior secured, 6–12 months, ~14% gross. Target is 30–40% of the reserve.

**Legal structure.**
- **RealFi Foundation** (Cayman) owns the issuers: **RealFi Reserve** (BVI) issues USDrf and **RealFi Alpha** (BVI) issues sUSDrf.
- The issuers invest as LPs in a **CIMA-regulated Cayman fund**, which holds the assets.
- USDrf is the Senior LP and sUSDrf the Junior LP.

**Traction.** ~$5.6M TVL on Cardano, mostly from three institutional wallets. Another $7.5M is expected in the coming weeks. Ethereum launch is on 1 December.

---

#### **2. Team, Backers & Investors**

**Backers**
- Hoskinson Family Office / IOG: **$13M committed launch capital**.
- **$9.5M raised** in total.
- **$6.44M IOG credit facility** to the Foundation ($2.25M drawn, matures Dec 2027).

**Team overview.** About **30 people**, mainly in Cape Town and Nairobi.
- **Leadership:** the CEO (John O'Connor) and CPO (Dynal Patel) are ex-IOG / Cardano Foundation executives who helped build Cardano.
- **Investment team:** spent their careers in emerging-market private equity and private credit (Untapped Global, Abraaj, EG Capital), mostly in Africa, so they know the market they lend into.
- **Track record:** they have already deployed **$11.5M across 25+ borrowers**, $4.5M of it at RealFi since 2023 with no loss events (unaudited).
- **References:** Royce has worked with Seny before, and Jordan knows the founder.
- **Gap:** the CVs of the CIO (Kleiterp) and GC (Singh) are missing from the data room.

**Detail**

| Person | Role | Background |
| --- | --- | --- |
| John O'Connor | CEO | First hire at the Cardano Foundation; Commercial Director at IOG (2018–23); Oxford PPE |
| Dynal Patel | CPO | CPO at IOG (2019–23, 80-person team); Vodafone; PhD in CS |
| David Kleiterp | CIO | Untapped Global (Head of Investments Africa), Abraaj, 54 Capital; founder of Mobilis ($7M deployed) |
| Sahil Shah | COO | Ran RealFi investment ops at IOG since 2023; Mara; EG Capital |
| Seny Orlov | Head of GTM | Morgan Stanley ECM; Keyrock; Lisk DeFi growth |
| Shawn Singh | General Counsel | GC/CCO at Luminus, Cheyne Capital and Guggenheim |
| Leonidas Tsagkalias | Head of Finance | At IOG since 2016 (Treasurer, Financial Controller) |
| Advisors | IC | Paul Tregidgo (ex-Vice Chair DCM, Credit Suisse); Steven McClurg (Canary Capital, Valkyrie) |

---

#### **3. What's the Opportunity**

**The deal.**
- We **mint 5M USDrf** with $5M USDC.
- RealFi invests that USDC 1:1 into **~60% OUSG and ~40% jAAA** (proposed allocation). These assets are held in a **dedicated 3-of-5 Safe**: 2 keys Re7, 2 keys RealFi, 1 key HT Digital.
- **Our USDrf is backed by those OUSG and jAAA**, not by RealFi's lending book.
- We receive the **organic yield** from those assets (~4.5%), and RealFi pays the **difference up to 12%** (~7.5%). The team has offered to pre-fund this delta into a separate wallet and pay us from it.
- On top of that, we receive **8% in RFG tokens**.
- **At maturity (2 months)**, the assets are redeemed and our USDrf is redeemed at par for USDC.

| | APR | $5M over 2 months |
| --- | --- | --- |
| Cash yield (USDC) | 12% | ~$100k |
| RFG tokens | 8% | ~$66.8k |
| **Total** | **20%** | **~$167k** |

**Why it's a great risk-adjusted opportunity**
- **Our assets are segregated from the main lending book.** If the lending book goes to zero, we don't care. We are only exposed to our own collateral, OUSG and jAAA, and this is set out in the agreement.
- The collateral sits in a 3-of-5 Safe where no party can move funds on its own. **The trust assumption is HT Digital**, the independent signer, doing what the legal agreement says. HT Digital is a reputable firm that Re7 already works with.
- **OUSG** is short-dated T-Bills from Ondo. **jAAA** we know well, and here we hold it spot with no leverage, so there is no liquidation risk.
- The term is **2 months**, and the top-up is pre-funded into a separate wallet.

---

#### **4. How can we lose money?**

**Q1. What if the protocol is hacked, or someone mints unbacked USDrf?**
It doesn't affect us. Our collateral sits in our own dedicated Safe, separate from the protocol. As the team explained on the call, even if the protocol were hacked, the rest of its backing is held off-chain: direct lending, plus T-Bills and CLOs with custodians.

**Q2. What if someone steals the reserves?**
- **OUSG and jAAA** can only be held by KYC'd addresses. Ondo's KYC registry gates OUSG, and jAAA is a restricted token with a whitelist. The issuers can freeze them: Ondo by removing an address from its registry (it also has an admin burn role), Anemoy/Centrifuge by freezing the address. A thief couldn't use or redeem them.
- **Direct lending** is off-chain loans, so there is nothing to steal on-chain.
- **USDrf:** minting is permissioned (KYB'd and whitelisted institutions only, 1:1 against USDC) and auto-suspends if backing falls below 100%. Admin is a 3-of-5 multisig with an emergency pause. *To confirm with the team: whether they can burn or freeze any holder's USDrf balance.*

**Q3. What if the lending book goes to zero?**
It doesn't affect us. Our collateral is segregated from the lending book, and we are only exposed to OUSG and jAAA. The team explicitly agreed this on the call, and the legal draft is meant to reflect it. We need to be careful with the wording, because the term sheet currently says the Safe assets are owned by the fund and that we rank "pari passu with other unstaked USDrf". **Chris and Kirill should review it.**

**Q4. What if HT Digital doesn't do what was agreed, and won't release interest or our principal?**
This is the main risk and the weakest point of the deal. HT Digital is our trust assumption. With their key we hold 3 of 5 and can exit without RealFi. If they act against us, I don't have a clear mitigation beyond the legal agreement. That said, I don't see why they would: they are a reputable firm, Re7 already works with them, and they would be breaching a signed agreement.

Context from Jordan:
- HT Digital is the digital-asset arm of **Harris & Trotter**, which is **Re7's own accountant**; our registered office is also with them.
- They act as independent professionals in the digital-asset space, not as a RealFi counterparty, so they should be neutral between the two sides and follow the legal agreement.
- The key point is the detail of when 3 keys can sign, and for whom. The backstop is a clear legal agreement that HT Digital has reviewed and commits to comply with.

They are also RealFi's proof-of-reserves attestor.

**Q5. What if the Safe keys are stolen?**
An attacker would need 3 of the 5 keys across two organizations. Stealing RealFi's 2 keys isn't enough: they would also need HT Digital's key or both of ours.

**Q6. What if OUSG or jAAA lose value?**
This is a real risk, and it's the exposure we keep. Holding T-Bills and AAA CLOs for 2 months at 12% more than compensates for it.

The table below assumes the worst historical drawdowns hit jAAA ($2M) and we exit at the bottom at maturity. In practice it's a mark-to-market loss that recovers if we hold.

| Scenario | Drawdown | jAAA loss | Net P&L incl. 12% |
| --- | --- | --- | --- |
| Fund max DD (Mar-26) | 0.22% | −$4.4k | +$95.9k |
| JAAA ETF max DD | 2.6% | −$52k | +$48.3k |
| COVID | 8.33% | −$166.6k | −$66.3k (−1.3%) |
| Extreme | 10% | −$200k | −$99.7k (−2.0%) |

**Q7. What if the Foundation disappears or goes bankrupt?**
We still have our collateral: it is segregated and it's ours. The Foundation only owes us the top-up, and that is pre-funded into a separate wallet.

**Q8. What if RealFi doesn't execute the redemption?**
RealFi executes the redemption at maturity, so we depend on them doing it. If they don't, we take the collateral out of the Safe with our keys plus HT's. We're already onboarded with Ondo, so we can redeem OUSG ourselves. For jAAA we still need to onboard with Anemoy.

---

#### **5. Key Requirements**

1. **Financials.** They sent unaudited financials: ~$1.12M liquid (cash and OUSG) plus $4.19M undrawn on the credit line, against a ~$62.7k top-up. They'll also pre-fund the top-up wallet. Do we need any more proof?
2. **Legal review (Kirill & Chris).** Check the agreement and side letter for any weak point or wording that could hurt us, especially that the Safe is legally ring-fenced and that HT signs with us.
3. **HT Digital call.** Get their commitment to follow the legal agreement, and a clear exit process.

---

#### **Annex: How much could the token be worth?**

The tokens are a **fixed USD amount: 8% APR on $5M for 2 months ≈ $66.8k**. That amount is converted into RFG at the 7-day VWAP after TGE (or a floor price, if higher). There is no vesting: the tokens are delivered 7 days after TGE. TGE is expected in Q1 2027.

So the tokens are worth either:
- **~$66.8k**, if TGE happens and we sell around the VWAP; less if the price drops after delivery (e.g. ~$33k at −50%), or
- **$0**, if TGE doesn't happen.

A higher FDV doesn't increase the value: we just receive fewer tokens. We don't count on them.
