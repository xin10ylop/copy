"""KPIs, cohort retention, revenue concentration and "mimic cascade" detection.

Run 01_aggregate_builder_fills.py first (writes fills_agg.pkl), and
02_check_file_coverage.py (writes coverage.json) so partial days can be excluded.

Usage: python3 03_kpis_cohorts_cascades.py
"""
import collections
import csv
import datetime
import io
import json
import pickle
import statistics as st
import urllib.request

import lz4.frame

BUILDER = '0x557edb253b1d7ed5f15b248a5a3fd919fa5d3c81'  # Invo, from app.invoapp.com main.dart.js

A = pickle.load(open('fills_agg.pkl', 'rb'))
days, users, udays = A['days'], A['users'], A['udays']
try:
    cov = json.load(open('coverage.json'))
except FileNotFoundError:
    cov = {}


def is_full(k):
    v = cov.get(k)
    return v is None or (isinstance(v, list) and v[1][11:13] >= '23')


# ---- monthly KPIs (full days only for daily averages) ----
M = collections.defaultdict(list)
for k in sorted(days):
    if is_full(k):
        M[k[:6]].append(days[k])
print('month  full_days  avgDAU  avg_daily_vol_$M  avg_daily_builder_$')
for m, l in sorted(M.items()):
    print(m, len(l), round(st.mean(d['nusers'] for d in l)),
          round(st.mean(d['vol'] for d in l) / 1e6, 1), round(st.mean(d['bfee'] for d in l)))

# ---- concentration / ARPU ----
bfs = sorted((s[3] for s in users.values()), reverse=True)
T, n = sum(bfs), len(bfs)
print('\ntraders', n, 'builder fees $%.0f' % T, 'mean $%.2f median $%.2f' % (T / n, st.median(bfs)))
for k in (100, 1000, 5000):
    print(' top %d = %.1f%% of revenue' % (k, sum(bfs[:k]) / T * 100))

# ---- cohort retention ----
size = collections.Counter()
coh = collections.defaultdict(collections.Counter)
for u, dl in udays.items():
    f = dl[0][:6]
    size[f] += 1
    for m in {x[:6] for x in dl}:
        coh[f][m] += 1


def add(m, k):
    y, mo = int(m[:4]), int(m[4:]) + k
    while mo > 12:
        mo -= 12
        y += 1
    return f'{y}{mo:02d}'


last = max(size)
print('\ncohort size  M+0..M+5 retention')
for c in sorted(size):
    if size[c] < 50:
        continue
    row = [f'{coh[c][add(c, k)] / size[c] * 100:.0f}%' for k in range(6) if add(c, k) <= last]
    print(c, size[c], ' '.join(row))

# ---- mimic cascades: >=20 distinct users opening same coin+side within 10 min ----
for ds in ('20260820', '20260920'):
    raw = urllib.request.urlopen(
        f'https://stats-data.hyperliquid.xyz/Mainnet/builder_fills/{BUILDER}/{ds}.csv.lz4', timeout=60).read()
    rows = csv.DictReader(io.StringIO(lz4.frame.decompress(raw).decode()))
    orders = {}
    for r in rows:
        if float(r['closed_pnl']) != 0:  # opening fills only
            continue
        t = datetime.datetime.fromisoformat(r['time'].replace('Z', '+00:00')).timestamp()
        o = orders.setdefault((r['user'], r['coin'], r['side'], int(t)), [0.0, 0.0, t])
        o[0] += float(r['px']) * float(r['sz'])
        o[1] += float(r['sz'])
    ol = sorted((v[2], k[1], k[2], k[0], v[0], v[0] / v[1]) for k, v in orders.items())
    by = collections.defaultdict(list)
    for o in ol:
        by[(o[1], o[2])].append(o)
    casc = []
    for (coin, side), lst in by.items():
        i = 0
        while i < len(lst):
            j, us = i, set()
            while j < len(lst) and lst[j][0] - lst[i][0] <= 600:
                us.add(lst[j][3])
                j += 1
            if len(us) >= 20:
                grp, px0 = lst[i:j], lst[i][5]
                sgn = 1 if side in ('B', 'Bid') else -1
                slip = [sgn * (g[5] - px0) / px0 * 1e4 for g in grp[1:]]
                casc.append((coin, side, len(us), sum(g[4] for g in grp), st.median(g[0] - lst[i][0] for g in grp[1:]), st.mean(slip)))
                i = j
            else:
                i += 1
    tot = sum(o[4] for o in ol)
    print(f'\n{ds}: {len(casc)} cascades, {sum(c[3] for c in casc) / tot * 100:.1f}% of opening notional')
    for c in sorted(casc, key=lambda c: -c[2])[:5]:
        print('  %s %s users=%d notional=$%.0f median_lag=%.0fs mean_slippage=%.1fbps' % c)
