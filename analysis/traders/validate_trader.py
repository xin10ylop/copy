"""Validate a Hyperliquid wallet before copying it.

Usage:
    python3 validate_trader.py <wallet> [--lag 90] [--slip 5] [--fee 7.7] [--days 50]

--lag   seconds between the leader's entry and yours (Invo copiers: median ~30-200s)
--slip  extra bps you pay on entry AND exit vs the leader (Invo cascades: ~2-10bps, memecoins far more)
--fee   your fee per side in bps (Invo all-in ~7.7; Hyperliquid direct ~4.5)

Prints the leader's real record (Hyperliquid all-time PnL incl. liquidations/fees/funding),
red flags (liquidations, averaging down, one-trade luck, too new) and a copier replay:
your entries/exits shifted by lag+slip, your fees, isolated margin at 3x/5x/10x, and
liquidation checks on 15m candles, sized at 2% of bankroll per trade.
"""
import argparse
import collections
import datetime
import statistics as st
import time

from copysim import sim
from validate import all_fills, episodes, post


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('wallet')
    ap.add_argument('--lag', type=float, default=90)
    ap.add_argument('--slip', type=float, default=5)
    ap.add_argument('--fee', type=float, default=7.7)
    ap.add_argument('--days', type=int, default=50)
    a = ap.parse_args()
    u = a.wallet.lower()
    since = int((time.time() - a.days * 86400) * 1000)

    pd = dict(post({'type': 'portfolio', 'user': u}) or [])
    ch = post({'type': 'clearinghouseState', 'user': u})
    fills = all_fills(u)
    closed, _ = episodes(fills, u)
    E = [e for e in closed if e['t0'] >= since]

    def last(k):
        try:
            return float(pd[k]['pnlHistory'][-1][1])
        except (KeyError, IndexError):
            return float('nan')

    first = datetime.datetime.utcfromtimestamp(fills[0]['time'] / 1000) if fills else None
    print(f'Wallet {u}')
    print(f"  account now ${float(ch['marginSummary']['accountValue']):,.2f}   first trade {first:%Y-%m-%d}" if first else '  no fills')
    print(f"  PnL (incl. liquidations/fees/funding): all-time ${last('perpAllTime'):,.2f}  30d ${last('perpMonth'):,.2f}  7d ${last('perpWeek'):,.2f}")
    if not E:
        print('  no closed trades in window')
        return
    nets = [e['net'] for e in E]
    wins = [x for x in nets if x > 0]
    losses = [-x for x in nets if x < 0]
    pf = sum(wins) / sum(losses) if losses else float('inf')
    liqs = sum(e['liq'] for e in E)
    adds = avgdown = 0
    ref = {}
    for f in fills:
        if f['time'] < since or not f['dir'].startswith('Open'):
            continue
        c, px = f['coin'], float(f['px'])
        if abs(float(f['startPosition'])) < 1e-12:
            ref[c] = px
        elif c in ref:
            adds += 1
            d = 1 if 'Long' in f['dir'] else -1
            avgdown += d * (px - ref[c]) < 0
    print(f'  last {a.days}d: {len(E)} trades, win rate {len(wins) / len(nets):.0%}, profit factor {pf:.2f}, '
          f'net ${sum(nets):,.2f}, liquidations {liqs}, median hold {st.median((e["t1"] - e["t0"]) / 60000 for e in E):.0f} min')
    print(f"  coins: {collections.Counter(e['coin'] for e in E).most_common(5)}")

    flags = []
    if first and (datetime.datetime.utcnow() - first).days < 60:
        flags.append(f'too new ({(datetime.datetime.utcnow() - first).days} days of history)')
    if liqs:
        flags.append(f'{liqs} liquidations in window')
    if adds >= 10 and avgdown / adds > 0.6:
        flags.append(f'averages down ({avgdown / adds:.0%} of adds at worse prices) - martingale risk')
    if wins and max(wins) / sum(wins) > 0.35:
        flags.append(f'one trade = {max(wins) / sum(wins):.0%} of profits')
    if pf < 1.2:
        flags.append(f'profit factor {pf:.2f} (wins barely cover losses)')
    if last('perpAllTime') <= 0:
        flags.append('losing all-time')
    print('  RED FLAGS: ' + ('; '.join(flags) if flags else 'none'))

    print(f'  copier replay (lag {a.lag:.0f}s, +{a.slip}bps each side, fee {a.fee}bps/side, 2% of bankroll per trade):')
    for L in (3, 5, 10):
        r = sim(E, L, a.slip, a.lag, fee_side_bps=a.fee)
        if not r:
            continue
        wk = collections.defaultdict(float)
        for x in r:
            wk[datetime.datetime.utcfromtimestamp(x[0] / 1000).strftime('%G-W%V')] += 0.02 * x[2]
        print(f'    {L:>2}x: bankroll {0.02 * sum(x[2] for x in r):+.1%}, your liquidations {sum(x[3] for x in r)}, '
              f'winning weeks {sum(v > 0 for v in wk.values())}/{len(wk)}')


if __name__ == '__main__':
    main()
