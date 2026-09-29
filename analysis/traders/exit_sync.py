"""Confirm leaders: share of a leader's followers who close within 30 min of the leader's close
(Invo copies TP/SL and sends 'trader closed' alerts). Reads leader_rank.pkl, writes leaders2.pkl."""
import urllib.request,lz4.frame,csv,io,datetime,collections,pickle,time,bisect
B='0x557edb253b1d7ed5f15b248a5a3fd919fa5d3c81'
rows=pickle.load(open('leader_rank.pkl','rb'))
cands={r[0] for r in rows}
L=pickle.load(open('leaders.pkl','rb'))['led']
bydate=collections.defaultdict(list)
for u in cands:
    for t in L[u]:
        if t[6]>=10: bydate[t[0]].append((u,t))
def load(ds):
    for a in range(4):
        try:
            raw=urllib.request.urlopen(f'https://stats-data.hyperliquid.xyz/Mainnet/builder_fills/{B}/{ds}.csv.lz4',timeout=60).read()
            return list(csv.DictReader(io.StringIO(lz4.frame.decompress(raw).decode())))
        except urllib.error.HTTPError as e:
            if e.code in (403,404): return []
            time.sleep(2**a)
        except Exception: time.sleep(2**a)
    return []
def ts(r): return datetime.datetime.fromisoformat(r['time'].replace('Z','+00:00')).timestamp()
dates=sorted(set(bydate))
res=collections.defaultdict(list)  # u -> (ds, nfollowers, frac_exit_sync, leader_closed)
cache={}
def day(ds):
    if ds not in cache:
        rows=load(ds)
        op=collections.defaultdict(list); cl=collections.defaultdict(list)
        for r in rows:
            t=ts(r)
            if float(r['closed_pnl'])==0: op[(r['coin'],r['side'])].append((t,r['user']))
            else: cl[r['coin']].append((t,r['user']))
        for d in (op,cl):
            for k in d: d[k].sort()
        cache[ds]=(op,cl)
        for k in list(cache):
            if k<(datetime.datetime.strptime(ds,'%Y%m%d')-datetime.timedelta(days=2)).strftime('%Y%m%d'): del cache[k]
    return cache[ds]
for ds in dates:
    nxt=(datetime.datetime.strptime(ds,'%Y%m%d')+datetime.timedelta(days=1)).strftime('%Y%m%d')
    op,cl=day(ds); op2,cl2=day(nxt)
    for u,t in bydate[ds]:
        _,t0,coin,side=t[:4]
        lst=op[(coin,side)]
        i=bisect.bisect_left(lst,(t0,''))
        F={x[1] for x in lst[i:bisect.bisect_right(lst,(t0+600,'~'))] if x[1]!=u}
        closes=cl[coin]+cl2[coin]
        tc=next((x[0] for x in closes if x[1]==u and x[0]>t0),None)
        if tc is None or not F:
            res[u].append((ds,len(F),None,False)); continue
        near={x[1] for x in closes if tc-60<=x[0]<=tc+1800}
        res[u].append((ds,len(F),len(F&near)/len(F),True))
    print(ds,flush=True)
pickle.dump(dict(res),open('leaders2.pkl','wb')); print('DONE')
