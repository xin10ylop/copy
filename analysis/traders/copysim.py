import json,time,urllib.request,bisect,os,pickle
from validate import post
META={u['name']:u for u in post({'type':'meta'})['universe']}
CACHE='candles_cache.pkl'
C=pickle.load(open(CACHE,'rb')) if os.path.exists(CACHE) else {}
def candles(coin):
    if coin in C: return C[coin]
    if coin.startswith('#'): C[coin]=[]; return []
    now=int(time.time()*1000); out=[]; start=now-52*86400*1000
    for _ in range(3):
        r=post({'type':'candleSnapshot','req':{'coin':coin,'interval':'15m','startTime':start,'endTime':now}})
        if not r: break
        out+=r
        if len(r)<5000 or r[-1]['t']+1<=start: break
        start=r[-1]['t']+1
    C[coin]=[(c['t'],float(c['h']),float(c['l'])) for c in out]
    pickle.dump(C,open(CACHE,'wb'))
    return C[coin]
def sim(episodes,lev,slip_bps,lag_s,fee_side_bps=7.7,since_ms=0):
    """Replay leader episodes as a copier with isolated margin at leverage `lev`.
    Returns list of per-trade margin returns (fraction of margin; -1 = liquidated)."""
    res=[]
    for e in episodes:
        if e['t0']<since_ms: continue
        mx=META.get(e['coin'],{}).get('maxLeverage',10)
        L=min(lev,mx); mm=1/(2*mx)
        cs=candles(e['coin'])
        if not cs or cs[0][0]>e['t0']: continue
        d=e['dir']; entry=e['entry']*(1+d*slip_bps/1e4); exit_=e['exit']*(1-d*slip_bps/1e4)
        t_in=e['t0']+lag_s*1000
        ts=[c[0] for c in cs]
        i0=max(bisect.bisect_right(ts,t_in)-1,0); i1=bisect.bisect_right(ts,e['t1'])
        seg=cs[i0:i1] or cs[i0:i0+1]
        worst=min(c[2] for c in seg) if d>0 else max(c[1] for c in seg)
        adverse=d*(entry-worst)/entry   # fraction move against
        if adverse>=1/L-mm:
            res.append((e['t0'],e['coin'],-1.0,True)); continue
        r=L*(d*(exit_/entry-1)-2*fee_side_bps/1e4)
        res.append((e['t0'],e['coin'],max(r,-1.0),False))
    return res
