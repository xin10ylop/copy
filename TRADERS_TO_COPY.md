# Invo traders worth copying: who they are and whether they hold up

*Data as of 2026-09-29.* Sources: Hyperliquid public fills and API, June–September 2026. Not financial advice: these are leveraged derivatives.

## Bottom line

- **The traders Invo users actually copy lose money, and so do their copiers.** I identified 45 confirmed "mimic leaders". Their median all-time result is a loss, most of their accounts hold $0–$600, and they've been liquidated 11–118 times each.
- **Replaying their last 50 days as a copier** (your real lag, slippage and fees; 5% of bankroll per trade):

  | Copy leverage | Median copier result | Leaders where copying made money |
  |---|---|---|
  | 5x | -8% | 9 of 29 |
  | 10x | -34% | 7 of 29 |
  | 20x | -50% | 5 of 29 |

- **None of the 160 candidates is proven safe to copy.** One is worth a small, capped test; two are on a watchlist. Details below.

## How I found who Invo users copy

Invo doesn't publish which wallet belongs to which username, so I found them from behaviour. I checked 10.6M Invo-routed fills for two things:

1. **The crowd follows in:** a wallet opens a position, and within 10 minutes 10 or more other Invo users open the same coin in the same direction.
2. **The crowd follows out:** when that wallet closes, 40–76% of those followers close within 30 minutes. Invo copies take-profit/stop-loss levels and sends a "trader closed" alert, which produces this pattern.
   - Control test: the same followers checked 3 hours later show about 0% overlap. So these are real mimic leaders, not coincidence.

This produced 160 candidates, of which 45 were confirmed leaders.

Every candidate was then checked against Hyperliquid's own all-time PnL, which includes liquidations, fees and funding. Every trade was rebuilt from open to close.

Each one was then **replayed as a copier would have lived it:**
- entering after that leader's real measured copier lag (26–207 seconds);
- at their real copier slippage;
- paying Invo's roughly 7.7 bps per side;
- using isolated margin;
- with liquidation checks on 15-minute candles.

## Invo's most-copied leaders: avoid

Copier replay columns use 5% of bankroll per trade over the last 50 days.

| Wallet | Copiers per trade | Followers exit with them | All-time PnL | Account now | Liquidations | Win rate | Profit factor | Copy at 5x | Copy at 10x |
|---|---|---|---|---|---|---|---|---|---|
| `0x37a4…73d3` | **291** | 72% | -$258 | $14 | 31 | 77% | 0.63 | inactive | inactive |
| `0xc790…04fa` | 134 | 66% | -$272 | $0 | 17 | 71% | 0.36 | -21% | **-84%** |
| `0xca8e…8ce3` | 108 | 68% | -$13 | $0 | 11 | 61% | 0.43 | inactive | inactive |
| `0xb0b1…43df` | 96 | 56% | -$63 | $104 | 27 | 84% | 1.02 | +27% | +2% |
| `0x2263…ef31` | 93 | 45% | -$220 | $244 | 33 | 80% | 0.89 | +18% | 0% |
| `0x9d67…9427` | 79 | 47% | -$74 | $148 | 34 | 71% | 0.55 | -34% | **wiped out** |
| `0x1171…c9fb` | 70 | 76% | -$46 | $3 | 50 | 73% | 0.70 | -11% | -26% |
| `0x9c90…ff8d` | 63 | 63% | -$137 | $0 | 88 | 71% | 0.64 | -40% | **wiped out** |

**The pattern: a high win rate hides losses that are bigger than the wins.** 70–85% of trades win, but the losses (mostly liquidations at 20–40x) outweigh them; any profit factor under 1 means that. This is the "win streak" that Invo's feed shows off.

## The one worth a small test: `0x84d420ab8107f4bd474147fc5d88ce696c6cec49`

**What's good:**
- It is the only candidate whose copier replay stays positive across 6 of 6 weeks, in both halves of the period, and when you enter 5 minutes late with 10 bps of extra slippage.
- Its median hold is about 3 hours, so copying late doesn't kill the edge.
- It trades 100% through Invo.

| Copier replay (2% of bankroll per trade) | Result | Copier liquidations |
|---|---|---|
| 3x | +28% | 5 |
| **5x** | **+39%** | 6 |
| 10x | +31% | 26 |
| 5x, entering 5 minutes late with +10 bps slippage | +25% | — |

**What's bad (read this before copying):**
- **It's only 5 weeks old.** First trade Aug 25; the account is $609.
- **Its own profit is thin.** +$125 on closed trades (+$227 all-time including open positions); only $24 of it in September. Profit factor is 1.16.
- **It was liquidated 18 times,** including three times in the last week.
- **It averages down: 88% of its add-ons are at worse prices.** This is a martingale pattern. It looks great until one trade doesn't come back.
- The replay is positive mainly because a copier at 5x with fixed small sizes avoids the leader's own blowups. **If you copy its leverage (Invo's default, up to 40x), you inherit those blowups.**

**Finding it in Invo.** Look for a profile whose open trades match these (as of Sep 29, ~07:00 UTC):
- **Shorts:** SOL @ 114.68 (5x), BNB @ 763.03 (10x), ADA @ 0.24767 (10x), HBAR @ 0.1182 (5x), IOTA @ 0.055157 (3x).
- **Longs:** LTC @ 68.151 (4x), NEAR @ 4.749 (10x), SAGA @ 0.02681 (3x), XMR @ 544.16 (5x), ASTER @ 0.70126 (1x), AVNT @ 0.12115 (2x).
- **Recent entries:** UNI long @ 8.7273 (Sep 29 06:34 UTC), XRP long @ 1.4846 (Sep 29 04:33 UTC).

**If you copy it, set these rules first:**
- Leverage at most **5x**, whatever the leader uses.
- **1–2% of bankroll per mimic.** It often holds 10–20+ positions at once.
- Copy its adds ("blue circle" updates) only if you're copying at the same small size.
- Hard stop: **quit after any 2 losing weeks, or if your total is down 15%.**
- Start with money you'd accept losing entirely.

## Watchlist (not yet)

| Wallet | Why it's interesting | Why not yet |
|---|---|---|
| `0x15fd8f2d1684e8f48e2bff324c62ca81c371c786` | 3 of 3 weeks positive; robust to slippage; low frequency (about 3 trades a day) | First trade Sep 19 (10 days of history); $71 account; 5 liquidations; uses 40x on BTC; averages down |
| `0x2726d6b0d2ae07838f14d1a96bb6616c55b4913f` | +62% replay at 5x | Flat in the first half and all the gain in the second; turns negative with 20 bps extra slippage; about 18 trades a day |

**Rejected:**
- `0xcfc641ab…`: turns negative if you copy 5 minutes late.
- `0xde3c4db5…`: turns negative with 5 bps of slippage.
- `0x9272e598…`: fading; the second half was negative.
- `0x7cba0d4f…`: copiers lose about 23 bps per entry to slippage, so -6% even though the leader's month was +$1.4K.

## Outside Invo (whole-Hyperliquid screen)

I screened all 46,723 accounts on Hyperliquid's leaderboard and fully validated the 80 most promising. Five passed all 10 checks, but on closer inspection none is a clean copy:

| Wallet | Profile | Status |
|---|---|---|
| `0x757df2c060ec6c7ba898fa6570aa98c1f46294ba` | $698K account; +$426K in 30 days; replay positive and robust to lag | **Holds big losers:** ZEC -$152K and HYPE -$51K unrealized at 10x, carried by PUMP +$350K. Copying now means copying $4.7M of concentrated bets |
| `0x98e073b579fd483eac8f10d5bd0b32c8c3bbd7e0` | +$832K all-time; profit factor 6.7; 4 of 4 weeks; robust to a 5-minute lag | **Hasn't traded since Sep 3** |
| `0xed7c45acfd7d2d3b21f3039d86e1da540596d23a` | 98% win rate, HYPE only | **Martingale:** 97% of adds at worse prices; account fell from $239K to $2.3K. Avoid |
| `0x01cd055a4c422cd498d35c3691e965819758d479` | Profitable on paper | Account is empty; funds moved elsewhere |
| `0xf7619dfb29b83bf5118fd0107c676156cd5e5605` | Stocks and oil (HIP-3) trader | Only 16 trades; about +1–2% replay |

These aren't Invo users, so Invo's Mimic can't follow them.

## Check any trader yourself

```
cd analysis/traders
pip install lz4
python3 validate_trader.py <wallet> --lag 90 --slip 5 --fee 7.7
```

It prints:
- the trader's real PnL (liquidations included);
- red flags: too new, liquidations, averaging down, one-trade luck, weak profit factor;
- the copier replay at 3x, 5x and 10x.

**Rules I'd hold any trader to before copying:**
1. At least 60 days of history.
2. Zero or very few liquidations.
3. Profit factor of 1.5 or more.
4. No single trade above 35% of profits.
5. Not averaging down.
6. Median hold of at least 1 hour.
7. Copier replay positive at 3–5x **and** with 5 minutes of lag and 10 bps of extra slippage.
8. Most weeks positive.

`find_leaders.py` and `exit_sync.py` regenerate the leader list from the public fill data.
