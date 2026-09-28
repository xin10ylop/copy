# Invo (invoapp.com): Deep Review and Where the Money Is

*Date: 2026-09-28.*

**How this was researched.** I read every page of the marketing site (26 pages, via the Framer search index). I reverse-engineered the web app at `app.invoapp.com` (Flutter, 9.7 MB bundle).

I also pulled Invo's complete trade history from Hyperliquid's public data:
- 10.66M fills from Dec 2025 to Sep 2026;
- 82,804 wallets;
- all-time PnL for 400 sampled wallets.

Other sources: DefiLlama for all 106 Hyperliquid front-ends, SEC Form D filings, the app stores, and press coverage. Scripts to reproduce every number are in [`analysis/`](analysis/).

> Not financial or legal advice. Everything below is public data plus my analysis.

---

## 0. The answer in 60 seconds

1. **Invo is real and it made money fast.** In about 5 months it grew from nothing to **$616K a month** in fees (August 2026). Lifetime totals:
   - $4.86B of trading volume;
   - **$1.85M of builder fees** (verified on-chain);
   - about $0.24M of Hyperliquid referral income;
   - **82.8K wallets that have traded.**

   It ranks **#6 of 106 Hyperliquid front-ends** by 30-day revenue, behind only four big wallets (MetaMask, Trust Wallet, Phantom, Rabby) and fomo. Invo did this with a small team (2–10 people on LinkedIn) and about **$3.6M raised in SAFEs** (a type of early-stage investment).

2. **Its business burns through the users who pay for it.** Using each wallet's true all-time PnL from Hyperliquid, which includes liquidations, fees and funding:
   - **85% of randomly sampled Invo traders lost money.** The median account peaked at **$18**.
   - **96% of Invo's top 100 revenue-generating users lost money.** Their median loss was **-$6,326**; their accounts went from a **$5,237** median peak to **$26**.
   - Those 100 wallets alone paid Invo $341K in builder fees (about 20% of all builder revenue).
   - **Result:** builder revenue fell 52–57% from August to September, and new traders per month fell from 26.7K (July) to about 9–11K (September). Over the same period competitors grew: fomo +52%, Trust Wallet +31%, HyperDash +137%.

3. **Being Invo's affiliate or creator is not how you get rich.**
   - The average Invo trader generates **$20.53** of builder fees over their lifetime; the median is **$2.10**.
   - At the top affiliate tier (40%), 5,000 referred traders are worth about **$41K** in total. The same traders on **your own** builder code at 5 bps (0.05%) would be worth about **$147K**.
   - A creator whose trade is copied by 483 people earned about **$4.29** (15% of the builder fee).

4. **The money is in owning the builder code:**
   - The app layer on Hyperliquid pays **about $7.7–7.9M a month (about $95M a year)** to front-ends, settled on-chain.
   - Invo proved the social copy-trading niche with very little capital.
   - fomo, the closest competitor, raised **$75M at a $550M valuation**.
   - Invo is losing ground and has obvious, data-backed gaps you can attack.

5. **Recommendation:** build **the copy-trading app Invo should have been**, starting with a cheap web MVP (**Play 2**) and expanding into the full mobile product (**Play 1**). Details are in §5 and the 90-day plan in §7. This repo (`copy`) is a natural home for it.

---

## 1. What Invo actually is (reverse-engineered)

| | |
|---|---|
| **Company** | Involio, Inc. (Delaware, incorporated 2021), 8767 E Via de Ventura, Scottsdale AZ. CEO Ryan Pace; CPO Cy Watson. SEC Form D filings total about $3.6M in SAFEs, the latest being $1.3M in Mar 2026. A Feb 2025 investor memo priced a round at $30M pre-money plus a token warrant; no token exists. |
| **History** | Launched about 2022 as "Involio", a verified social-investing app (stocks, crypto, subscriptions, courses). It moved to Hyperliquid perps in Dec 2025, when the first fills with its builder code appear. It rebranded to Invo around spring 2026 (the X account was created Apr 28, 2026). |
| **Product** | Social feed plus "**Mimic**": one tap copies a leader's trade (same take-profit, stop-loss and leverage, with a size slider). Feeds are Recent, Following, Trending and "Fire Moves". Posted trades can't be deleted. There is an "Invo Score" from 1 to 10, and 170+ perp pairs at up to 40x leverage. |
| **Stack** | Marketing site on Framer. App built in **Flutter** (iOS, Android and web from one codebase). **Turnkey** embedded wallets with passkeys and email one-time codes. Backend at `api.involio.com/v1_0` returns FastAPI-style errors, and the server signs trades via Hyperliquid agent wallets (`/dex/position/create`, `/dex/mimic/copy`). **Transak** card on-ramp; USDC deposits via Solana or Arbitrum. TradingView charts, Sentry, hCaptcha. |
| **How it makes money** | A **Hyperliquid builder fee of 3.5 bps (0.035%) on every fill**. This is hard-coded in the web app: builder `0x557eDb253b1D7ed5f15b248A5A3Fd919fA5D3C81`, fee `35` in tenths of a bp, approval cap `100`. It also earns Hyperliquid's own referral commission through code **`INVO`**. The user pays about **0.077–0.08% per side** all-in. On-chain, **100% of Invo fills are taker (IOC) orders**. |
| **Payouts** | Creators get 15% of fees on trades copied from them (one guide says "up to 50%"). Affiliates get 10/20/30/40% on direct referrals plus 2.5–10% on second-level referrals, with the tier applying to the whole network. Per the Terms, these percentages apply only to fees Invo "actually receives and retains". |
| **Treasury seen on-chain** | $730.7K USDC in spot and $31.9K in the perps account on the builder address. |

## 2. The real numbers (on-chain)

### Monthly

Source: Hyperliquid builder-fill files. September is Sep 1–27, and 12 of those days' published files are only half-days, so September is understated about 20%. DefiLlama puts September at $265K.

| Month | Volume | Builder fees | Monthly traders | New traders | Avg daily traders* |
|---|---|---|---|---|---|
| 2026-03 | $28M | $9.8K | 562 | 468 | 152 |
| 2026-04 | $257M | $89.8K | 6,807 | 6,381 | 1,398 |
| 2026-05 | $251M | $87.7K | 8,638 | 4,718 | 1,812 |
| 2026-06 | $636M | $222.6K | 21,618 | 16,667 | 4,155 |
| 2026-07 | $1,319M | $461.8K | 39,477 | 26,712 | 9,099 |
| **2026-08** | **$1,758M** | **$615.3K** | **39,597** | 18,793 | **9,684** |
| 2026-09 | $601M+ | $210K+ (DefiLlama $265K) | 26,451+ | 8,939+ | 6,369 |

\*Complete days only. Peak day: 12,499 traders on Aug 19; $139M volume and about $44–49K fees on Aug 21. Last 14 complete days: about 6.2K daily traders and about $9K a day in builder fees, **roughly half of August's pace**.

### Leaderboard and trend

Source: DefiLlama, last 30 days. The whole builder market paid about $7.7M.

| # | Front-end | 30-day revenue | Aug → Sep |
|---|---|---|---|
| 1 | MetaMask | $1.47M | flat |
| 2 | Trust Wallet | $1.34M | +31% |
| 3 | Phantom | $1.18M | -14% |
| 4 | **fomo** (social app, like Invo) | $0.91M | **+52%** |
| 5 | Rabby | $0.35M | +37% |
| **6** | **Invo** | **$0.30M** | **-57%** |
| 7 | HyperDash (analytics site plus copy) | $0.25M | +137% |

### Users

- **"Join 250K+ users" is not supported.** On-chain, 84,931 wallets have signed up under code `INVO` and **82,804 have ever traded**. Google Play shows about 211K installs across the app's whole history back to 2022.
- **Revenue per trader is the lowest among the big front-ends:** about $8.6 per active trader per 30 days, versus fomo about $33, Phantom about $29 and MetaMask about $112. Lifetime it is **$20.53 on average and $2.10 at the median**. 35% of traders have paid under $1 in total.
- **Revenue comes from a few whales:**
  - 3.2% of traders (paying $100 or more each) generate **64%** of revenue;
  - the top 1,000 traders generate 48%;
  - the top 100 generate 20%.
- **Retention**, as the share of each monthly cohort still trading:

  | Cohort | M+1 | M+2 | M+3 | M+4 |
  |---|---|---|---|---|
  | Apr | 57% | 27% | 18% | 14% |
  | Jun | 61% | 29% | 15% | |
  | Jul | 52% | 22% | | |
  | Aug | 43% | | | |

  Recent cohorts hold on worse: August kept 43% after one month, versus 57–63% for the April–June cohorts.
- **What gets traded:** BTC 62%, ETH 10%, SOL 6%, XRP 4%, then a long tail of memecoins (195 coins in total). There is **no HIP-3 volume**; HIP-3 covers stocks, gold, oil and pre-IPO shares and is now roughly 30–50% of all Hyperliquid volume, depending on the source (a live API snapshot on Sep 28 showed about 30%).

## 3. Do Invo users make money? No, and it caps Invo's growth.

**Sample results.** PnL here is Hyperliquid's own all-time figure, which includes fees, funding and liquidations.

| Sample | Profitable | Median PnL | Total PnL | Median peak → current account |
|---|---|---|---|---|
| 300 random Invo traders | **15%** | -$9.84 | -$15.7K | $18 → $4 |
| Top 100 revenue payers | **4%** | **-$6,326** | **-$842K** | **$5,237 → $26** |

An independent sample of 150 wallets gave a similar result: 13% profitable, and **79% liquidated at least once**.

**Why users lose:**
- **Fee drag at leverage.** About 0.078% per side on position size works out to about 1.6% of margin per side at 20x, so about **3.1% of margin per round trip** (6.2% at 40x). Every trade is a market (taker) order.
- **Copiers pile in late at worse prices.** On Aug 20, **88% of all new-position volume came in "mimic cascades"**: 20 or more Invo users opening the same coin in the same direction within 10 minutes.
  - Example: 483 users shorted PEOPLE with a median delay of 114 seconds; followers filled about **1.5% worse** than the first order.
  - The same pattern shows up on MOODENG and VINE (+24–25 bps worse).
  - In thin memecoins this flow is predictable and easy for outside traders to front-run. Invo's own guides even suggest waiting for the "discount" entry.
- **High leverage in the product and the marketing.** The homepage shows 30x trades and "65 win streak" badges.

**Why this matters for revenue.** Invo earns from the flow of whales who are wiped out within weeks. When the July–August cohorts were used up and acquisition slowed, revenue halved. **Lifetime value is capped by how fast customers lose their money.** Whoever fixes copier survival wins this category.

## 4. Invo's weaknesses (each one is an opening)

| # | Weakness | Evidence |
|---|---|---|
| 1 | Copiers lose money, so the platform loses them | §3: 85% of traders and 96% of whales lose; retention is falling |
| 2 | Copying is manual, one trade at a time, so followers enter late | Cascades with 1–6 minute median delays; users need a push notification and a swipe per trade; app reviews say "trading is manual" |
| 3 | No stocks, commodities or pre-IPO (HIP-3) markets | 0% HIP-3 volume. Peers route 10–25% there, and fomo's perps launch (Jun 2026, with HIP-3 via trade.xyz) grew past Invo |
| 4 | Lowest revenue per user in its peer group | $8.6 per 30 days versus $29–112. It has no whale or VIP program even though 3% of traders produce 64% of revenue. Its fee tiers just copy Hyperliquid's |
| 5 | Creator pay is too small to attract real traders | 15% of 3.5 bps. A 483-copier cascade paid the leader about $4, and a 331-copier BTC trade about $51. Invo's own example ("$1,000 per trade") assumes 5,000 copiers × $100 × 20x |
| 6 | US regulatory exposure | A US company whose Terms don't exclude US persons, on the US App Store. Reviews mention US states and SSN checks. Phantom, MetaMask, Trust Wallet and fomo **all** block the US from perps. See the 2023 CFTC actions against Opyn, Deridex and ZeroEx |
| 7 | Onboarding friction and trust problems | Reviews since the pivot average about 3.4–3.5 stars, versus 4.3–4.8 before. Complaints: an "11.6% deposit fee", withdrawals that only go out as USDC on Arbitrum or Solana, card declines, KYC lockouts. There are clusters of templated 5-star reviews (Mar 2024, Nov 2024) |
| 8 | Sloppy public materials | "250K+ users" versus 82.8K traders. Creator share given as 15% in one place and "up to 50%" in another. The Tier-4 second-level referral % is missing from the table. The fee table calls maker fees a "Maker Rebate". The Mimic Madness rules still contain the placeholder "[Global/US] residents" (a sweepstakes-law risk: "one mimic = one entry, no cap", with no free way to enter). The Terms link both programs to the same page. The Flutter bundle lists `/admin/*` endpoint names. The liquidation guide criticises exchanges that profit from liquidations, while Hyperliquid's liquidator vault does exactly that |
| 9 | Weak brand and distribution | X @invoxyz has about 680 followers; Discord about 8.3K. Growth was TikTok and influencer driven (referral landing pages exist for Phil Hellmuth, FaZe H1ghSky1, Jordan Welch, Luca Netz and others). The Terms ban users from paying to advertise their referral codes |
| 10 | About 55K dormant wallets | 82.8K ever traded; 28K traded in the last 30 days. Nobody is winning them back |

## 5. Ways to make money, ranked

| Play | Capital | Time to first $ | Realistic 12-month upside | Risk | Verdict |
|---|---|---|---|---|---|
| **1. Build a better copy-trading front-end** on Hyperliquid builder codes | $$ (3–5 people, 3–4 months) | 3–4 months | $0.3M → $6M+ a year in revenue; venture-scale if it works | Medium-high (execution, regulation) | **Best upside** |
| **2. "Copier-PnL" analytics site plus copy button** (HyperDash model) | $ (1–2 engineers, 4–6 weeks) | 1–2 months | $0.1–1.5M a year | Medium | **Best first step; becomes the MVP for Play 1** |
| 3. Invo affiliate (if you already have an audience) | ~0 | Weeks | ~$8K per 1K referred traders | Low money, depends on Invo | Only as a bridge |
| 4. Invo creator | ~0 | Months (20 trades, 6 weeks, 50 followers) | Hundreds to low thousands of dollars | High (you trade at leverage) | Not worth it |
| 5. Sell Invo the fixes, or invest | Relationship | Varies | Consulting fees; a $30M-pre SAFE is only interesting if Invo fixes §4 | High | Opportunistic |
| ✗ Traps | — | — | — | Legal, ethical | See the end of this section |

### Play 1: Build the copy-trading app Invo should have been

**Why it can work (evidence, not hope):**
- Front-ends get paid automatically and on-chain. There is no custody, no card processing and no exchange licence to run. The **front-end market is about $7.7–7.9M a month** and growing, with 106+ front-ends sharing it.
- Invo reached **$616K a month** with a Flutter app, Turnkey wallets and a ~3.5 bp fee, about 5 months after its ramp began, on less than $4M raised. fomo is the same category at a **$550M** valuation.
- Invo is **shrinking (-57%)** while social apps and apps with HIP-3 markets grow. Its unhappy traders are reachable (TikTok, Discord, crypto X).

**Product edge.** Each point below maps to a weakness in §4.

1. **Rank leaders by what their followers made, not by the leader's own PnL.** Show "copier PnL", follower slippage and time to liquidation on every leader. This is the trust feature Invo claims but doesn't measure.
2. **Instant server-side mirroring, not tap-to-copy.** Followers opt into a leader with risk limits (maximum leverage, maximum % per trade, daily loss stop). Orders go out in the same second, which removes the cascade slippage. Use limit or maker orders where possible to cut the 4.5 bp taker fee. Invo's own backend already signs trades through agent wallets, so this is technically straightforward.
3. **Stocks, gold, oil and pre-IPO markets (HIP-3) from day one.** That is roughly 30–50% of Hyperliquid volume, it is where fomo grew, and it brings a new audience ("copy the NVDA trader").
4. **Survival by default.** Default copy leverage at or below 5–10x, automatic reduce-only near liquidation, and "paper follow" before real money. **This is how you raise lifetime value per trader above Invo's $20.**
5. **A VIP tier for the 3% of traders who produce 64% of revenue.** Fee rebates by volume, a dedicated feed and priority execution.
6. **Pay creators enough that good traders come.** 25–35% of builder fees plus rank-based bonuses, because creators are the acquisition channel. Keep performance fees out initially: they raise the regulatory bar.
7. **Block the US from day one**, as every major peer does. Target markets where copy trading is already mainstream on Bitget, Bybit and BingX: LatAm, Turkey, SEA, Nigeria, India. **Get counsel before launch.**

**Unit economics** (from Invo's real data):
- Revenue = volume × fee. At **5 bps** (fomo's and Phantom's rate; Invo charges 3.5, Trust 9.5, MetaMask 10), every $1M of volume earns $500.
- Invo's lifetime builder revenue per trader is about $20, so **paid acquisition only works below about $10 per trader** unless you raise value per trader. Hence: grow through creators, focus on survival and the VIP tier, and target bigger accounts. HyperDash earns about $130 per active trader per month from about 850 large traders.

**Monthly run-rate once ramped** (assumes 5 bps, and 60% net after creator and affiliate payouts):

| Scenario | Monthly traders | Volume per trader per month | Monthly volume | Gross/month | Net/month | Net/year |
|---|---|---|---|---|---|---|
| Niche | 2,000 | $40K | $80M | $40K | $24K | **$0.29M** |
| Solid | 10,000 | $50K | $500M | $250K | $150K | **$1.8M** |
| Invo peak / fomo scale | 30,000 | $60K | $1.8B | $900K | $540K | **$6.5M** |

For reference, Invo in August had 39.6K traders × $44K = $1.76B. fomo's last 30 days: 21K traders × $74K = $1.56B.

**Build cost (rough estimate):** 3–5 people for 3–4 months to launch, similar to Invo's team size. The stack is proven off-the-shelf: Flutter or React Native, Turnkey or Privy wallets, the Hyperliquid SDK, Transak or MoonPay, TradingView. Main costs are salaries, legal structuring for a non-US launch, and creator incentives.

### Play 2: "Copier-PnL" analytics site plus copy button (start here)

- **Proof it works:** HyperDash earns **$112K** (on-chain) to **$247K** (DefiLlama) every 30 days from about **850 traders**, and grew 137% last month.
- **Why it's cheap to build:** every builder's fills and every wallet's PnL are **public** (this review used exactly that data). You can build a site ranking Hyperliquid traders by risk-adjusted, *copyable* performance, including how their followers fared. Add a "copy" or "trade" button that routes through your own builder code.
- **Size:** web only, 4–6 weeks for 1–2 engineers. It becomes the data engine and the first users for Play 1.
- **Distribution:** weekly "who made followers money" leaderboards on X and TikTok, embeddable leader cards, and alerts when a whale moves.

### Play 3: Invo affiliate (only if you already have an audience)

- The most you can expect is **about $8.2K per 1,000 referred traders** over their lifetime at the 40% tier: $20.53 average × 40%. The median trader is worth $0.84.
- The Terms forbid paying to advertise your code, and let Invo change the formula at any time.
- The same audience on your **own** builder code at 5 bps is worth about 3.6× more ($29K per 1,000 traders), plus Hyperliquid's 10% referral commission. **If you can drive traffic, own the code.**

### Play 4: Invo creator

- Payout is 15% of 3.5 bps on copied size.
- Observed examples: 483 copiers paid the leader **$4.29**; 331 copiers on a large BTC trade paid **about $51**.
- The whole creator pool has been worth at most about $280K over Invo's lifetime (15% × $1.85M).
- You also need 20 trades, 6+ weeks and 50 followers first, and you trade at leverage yourself. **Not a path to real money.**

### Play 5: Work with Invo (advise, invest, or position it for acquisition)

- Invo's fixes (§6) are worth millions a year to them, and the data in this report is the pitch.
- Wallets dominate the front-end revenue pool but lack social and copy features, so Invo, or a Play-1 team, could plausibly be acquired by one of them.
- Investing only makes sense if Invo fixes copier survival, blocks the US and adds HIP-3.

### Traps (don't)

- **Farming referrals or promotions with fake accounts.** This includes self-referrals, wash-trading for "Mimic Madness" entries, and fake screenshots. It is banned by the Terms (§10.2–10.3), it can be fraud, and payouts can be clawed back.
- **Front-running the mimic cascades.** It is technically easy because the flow is public and predictable. It is predatory on retail users and a legal and reputational minefield. The right response is to build the product that removes it (Play 1, point 2).
- **Copy-trading on Invo to get rich.** 85% of its traders and 96% of its biggest traders lose money.

## 6. If you are Invo: the 10 highest-value fixes

1. **Add HIP-3 markets** (stocks, commodities, pre-IPO). Peers get 10–25% of their volume there, and it opens a new audience.
2. **Make auto-copy with guardrails the default** (fixes cascades and slippage), and switch mimic orders from market to maker or limit where possible.
3. **Rank by copier outcomes.** Put follower PnL into Invo Score and cap default copy leverage. Retention and lifetime value compound from here.
4. **Create a VIP / whale tier** (3% of traders produce 64% of revenue).
5. **Reprice to 5 bps**, at least on HIP-3 and VIP-routed flow. That is +43% revenue per dollar traded, and peers charge 5–10 bps.
6. **Block the US or get a compliance plan.** This is an existential risk, and every large peer blocks.
7. **Win back about 55K dormant traders** with survival-focused features, not more leverage.
8. **Fix deposits and withdrawals** (on-ramp fees, more networks), which is the main theme of 1-star reviews.
9. **Clean up public claims and legal text** (the 250K figure, 15% vs 50%, placeholders, sweepstakes structure).
10. **Put the idle treasury to work** ($730K USDC sitting in spot).

## 7. 90-day execution plan (Play 2 → Play 1)

| Weeks | Deliverable |
|---|---|
| 0–2 | Legal: pick a non-US entity and jurisdiction with counsel; geofencing and Terms. Register a builder address and a Hyperliquid referral code. Data pipeline: this repo's `analysis/` scripts generalised to all builders and wallets |
| 2–6 | **Web MVP (Play 2):** leader leaderboard with copier PnL, slippage and drawdown; wallet pages; one-click trade with embedded wallets; builder fee 5 bps. Launch with 20–50 recruited leaders (offer 30% fee share) |
| 6–10 | **Auto-copy:** subscribe to a leader with risk limits; server-side mirroring via agent wallets; reduce-only safety. Add HIP-3 markets |
| 10–13 | Mobile (Flutter or React Native), push alerts, TikTok and X creator program, VIP tier. Targets: 2,000 monthly traders, $80M a month in volume, about $40K a month gross |

**Kill or scale test at day 90.** Scale if copier 30-day survival is above 50%, M+1 retention is above 55% (Invo's cohorts: 43–61%) and revenue per trader is above $15 a month (Invo: $8.6). Otherwise rethink or kill.

## 8. Risks

- **Regulation:**
  - The CFTC treats DeFi perps offered to US retail as swaps or leveraged retail commodity transactions. See its 2023 orders against Opyn, Deridex and ZeroEx.
  - Its 2026 no-action relief for wallet front-ends does **not** cover DeFi derivatives.
  - Copy-trading can also raise commodity-trading-advisor and introducing-broker questions.
  - **Block the US; get counsel; start with fee-share, not profit-share.**
- **Platform dependency:** Hyperliquid can change fees, builder-code rules or HIP-3 economics. Hyperliquid's own gross revenue is down about 43% from Q3 2025 to Q2 2026.
- **Competition:** the four big wallets (MetaMask, Trust Wallet, Phantom, Rabby) hold about 57% of front-end revenue and fomo is well funded. Differentiate on copier outcomes, which nobody measures today.
- **Ethics and product:** a platform where most users lose money eventually loses them. Survival features are both the ethical choice and the commercial one.

## 9. Method, caveats, sources

- **Data files:** Hyperliquid daily builder fills at `stats-data.hyperliquid.xyz/Mainnet/builder_fills/<builder>/<YYYYMMDD>.csv.lz4`.
  - Coverage: Dec 2025 to Sep 27, 2026.
  - Jul 8 is missing and 17 days are partial (mostly September), so September figures are lower bounds.
- **Hyperliquid info API:** `referral` gives builder rewards, referral count and the top 5,000 referees; `portfolio` gives all-time PnL including liquidations and funding; `clearinghouseState` gives account state.
- **PnL from fills alone is wrong.** It excludes liquidations, which are not builder-routed. For the 300-wallet sample, fills suggested +$9.7K while the true figure was -$15.7K.
- **Builder address:** read from Invo's own web bundle (`app.invoapp.com/main.dart.js`: builder `0x557e…3c81`, fee `35`, code `INVO`) and confirmed via the Hyperliquid API.
- **Other sources:**
  - DefiLlama API: `/summary/fees/invo-perps` and `/overview/fees` (for the builder leaderboard).
  - SEC EDGAR, CIK 0001938327 (Form D).
  - App stores: [iOS](https://apps.apple.com/us/app/involio/id1601301148) and [Google Play](https://play.google.com/store/apps/details?id=com.involio.app).
  - [Crypto Briefing, Aug 25 2026](https://cryptobriefing.com/invoxyz-surpasses-trust-wallet-hyperliquid-volume/).
  - [CoinDesk on HIP-3 and builder costs](https://www.coindesk.com/business/2026/08/09/hyperliquid-s-rwa-perps-boom-is-eating-into-the-revenue-that-backs-hype).
  - [Hyperliquid builder-code docs](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/builder-codes).
  - [CFTC press release 8774-23](https://www.cftc.gov/PressRoom/PressReleases/8774-23).
  - [fomo perps](https://fomo.family/blog/perpetuals-now-on-fomo).
  - [Datawallet on fomo](https://www.datawallet.com/crypto/fomo-app-explained).
  - [HyperDash docs](https://docs.hyperdash.info/).
  - Invo's own guides at [invoapp.com/guides](https://www.invoapp.com/guides) and its [Terms](https://www.invoapp.com/terms-condition).
- **Not verified:** Invo's off-chain payouts to creators and affiliates; whether the app blocks US IP addresses; fomo and HyperDash figures differ between DefiLlama and on-chain pulls, so ranges are given.
