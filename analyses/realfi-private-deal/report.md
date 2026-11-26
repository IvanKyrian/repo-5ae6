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
1. We send $5M USDC to RealFi Reserve and receive 5M USDrf, which we hold for 2 months.
2. The USDC buys ~$3M OUSG and ~$2M jAAA, held in a dedicated Safe.
3. At maturity they redeem the assets and pay us back $5M at par.

| | Rate | $ (2 months) | Paid by |
| --- | --- | --- | --- |
| Backing yield | ~4.5% | ~$37.6k | RealFi Reserve |
| Top-up (delta) | ~7.5% | ~$62.7k | RealFi Foundation (pre-funded into a separate wallet) |
| **Total cash** | **12%** | **~$100k** | |
| RFG tokens | 8% | ~$66.8k | Valued at $0 |

**Why it's good**
- **Our assets are segregated from the main lending book.** If the lending book goes to zero, we don't care. We are only exposed to our own collateral, OUSG and jAAA, and this is set out in the agreement.
- The collateral sits in a 3-of-5 Safe where no party can move funds on its own. **The trust assumption is HT Digital**, the independent signer, doing what the legal agreement says. HT Digital is a reputable firm that Re7 already works with.
- **OUSG** is short-dated T-Bills from Ondo. **jAAA** we know well, and here we hold it spot with no leverage, so there is no liquidation risk.
- The term is **2 months**, and the top-up is pre-funded into a separate wallet.

---

#### **4. How can we lose money?**

**Q1. What if the protocol is hacked, or someone mints unbacked USDrf?**
Nothing happens to us. Our backing is off-chain in our own Safe, which the USDrf contracts can't touch. Minting also requires KYB and whitelisting.

**Q2. What if someone tries to steal all the reserves?**
They can't reach ours. The main reserve is held off-chain with custodians, and our Safe needs 3 of 5 signatures.

**Q3. What if the lending book goes to zero?**
We don't care. Our collateral is segregated, and we're only exposed to OUSG and jAAA. *Legal must confirm that the side letter really ring-fences the Safe. Today the term sheet says the Safe assets are owned by the fund and that we rank "pari passu with other unstaked USDrf".*

**Q4. What if HT Digital doesn't do what was agreed, and won't release interest or our principal?**
We have a legal contract under which HT must cooperate. With HT's key we have 3 of 5 keys and can exit without RealFi. HT is the trust assumption.

**Q5. What if keys are stolen?**
An attacker would need 3 keys across two organizations. Stealing RealFi's 2 keys isn't enough: they would also need HT's key or both of ours.

**Q6. What if OUSG or jAAA lose value?**
- **OUSG:** T-Bills. KYC is required to mint it and Ondo can freeze it, so it's very hard to hack and it won't go to zero.
- **jAAA:** AAA CLOs. Spot exposure on $2M, against the ~$100k we earn in 2 months:

| Scenario | Drawdown | jAAA loss | Net P&L |
| --- | --- | --- | --- |
| Fund max DD (Mar-26) | 0.22% | −$4.4k | +$95.9k |
| JAAA ETF max DD | 2.6% | −$52k | +$48.3k |
| COVID | 8.33% | −$166.6k | −$66.3k (−1.3%) |
| Extreme | 10% | −$200k | −$99.7k (−2.0%) |

This assumes RealFi also fails to pay par, which is their obligation first.

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

- We receive **$66.8k in RFG**, priced at the higher of the 7-day VWAP after TGE and a floor price that hasn't been set yet. The tokens are unlocked and delivered 7 days after TGE. TGE is expected in Q1 2027.
- Because the amount is fixed in USD, a high FDV doesn't give us more: we just receive fewer tokens. The value depends on TGE happening and on where the price is when we sell.

| Case | Value | Extra annualized yield |
| --- | --- | --- |
| No TGE | $0 | 0% |
| Sold at VWAP | $66.8k | +8% |
| Sold 30% below VWAP | $46.8k | +5.6% |
| Sold 50% below VWAP | $33.4k | +4% |

We don't count on it.
