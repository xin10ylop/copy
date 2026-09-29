import json,time,urllib.request,collections,statistics as st,sys,pickle
def post(body):
    for a in range(6):
        try:
            req=urllib.request.Request('https://api.hyperliquid.xyz/info',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
            return json.loads(urllib.request.urlopen(req,timeout=60).read())
        except Exception: time.sleep(3*(a+1))
    return None
def all_fills(u):
    out=[];start=0;seen=set()
    while True:
        r=post({'type':'userFillsByTime','user':u,'startTime':start,'aggregateByTime':False})
        if not r: break
        new=[f for f in r if f['tid'] not in seen]
        for f in new: seen.add(f['tid'])
        out+=new
        if len(r)<2000 or not new: break
        start=max(f['time'] for f in r)
        time.sleep(0.5)
    return sorted(out,key=lambda f:(f['time'],f['tid']))
def episodes(fills,u):
    pos=collections.defaultdict(float); cur={}; eps=[]
    for f in fills:
        c=f['coin']
        if c.startswith('@') or c.startswith('#') or '/' in c: continue   # skip spot and outcome markets
        sz=float(f['sz'])*(1 if f['side']=='B' else -1); px=float(f['px'])
        sp=float(f['startPosition'])
        e=cur.get(c)
        if e is None or abs(sp)<1e-12:
            if e is not None: eps.append(e)
            e=cur[c]={'coin':c,'dir':1 if sz>0 else -1,'t0':f['time'],'t1':None,'in_n':0.0,'in_sz':0.0,'out_n':0.0,'out_sz':0.0,'pnl':0.0,'fee':0.0,'bfee':0.0,'maxntl':0.0,'liq':False,'invo':False}
        opening = (sz>0)==(e['dir']>0)
        if opening: e['in_n']+=abs(sz)*px; e['in_sz']+=abs(sz)
        else: e['out_n']+=abs(sz)*px; e['out_sz']+=abs(sz)
        e['pnl']+=float(f['closedPnl']); e['fee']+=float(f['fee']); e['bfee']+=float(f.get('builderFee') or 0)
        if float(f.get('builderFee') or 0)>0: e['invo']=True
        if f.get('liquidation') and f['liquidation'].get('liquidatedUser','').lower()==u.lower(): e['liq']=True
        newpos=sp+sz
        e['maxntl']=max(e['maxntl'],abs(newpos)*px)
        if abs(newpos)<1e-9 or (sp!=0 and (newpos>0)!=(sp>0)):
            e['t1']=f['time']; eps.append(e); del cur[c]
    open_eps=list(cur.values())
    closed=[e for e in eps if e['t1'] and e['in_sz']>0 and e['out_sz']>0]
    for e in closed:
        e['entry']=e['in_n']/e['in_sz']; e['exit']=e['out_n']/e['out_sz']
        e['ret_bps']=e['dir']*(e['exit']/e['entry']-1)*1e4     # price move captured, before fees
        e['net']=e['pnl']-e['fee']
    return closed,open_eps
def maxdd(pnl_hist,acct_hist):
    # drawdown of cumulative pnl relative to (peak account value)
    peak=-1e18;mdd=0.0
    av=dict((t,float(v)) for t,v in acct_hist)
    for t,v in pnl_hist:
        v=float(v); peak=max(peak,v)
        base=max(av.get(t,0),1)
        if peak-v>0: mdd=max(mdd,(peak-v)/max(base+(peak-v),1))
    return mdd
def validate(u,slip_bps,fee_side_bps=7.7,since_ms=0):
    p=post({'type':'portfolio','user':u}); pd=dict(p) if p else {}
    ch=post({'type':'clearinghouseState','user':u})
    fills=all_fills(u)
    closed,open_eps=episodes(fills,u)
    rec={'wallet':u,'n_fills':len(fills)}
    at=pd.get('perpAllTime',{})
    rec['allTimePnl']=float(at['pnlHistory'][-1][1]) if at.get('pnlHistory') else None
    rec['acct_now']=float(ch['marginSummary']['accountValue']) if ch else None
    rec['acct_peak']=max((float(x[1]) for x in at.get('accountValueHistory',[])),default=None)
    rec['month_pnl']=float(pd['perpMonth']['pnlHistory'][-1][1]) if pd.get('perpMonth',{}).get('pnlHistory') else None
    rec['week_pnl']=float(pd['perpWeek']['pnlHistory'][-1][1]) if pd.get('perpWeek',{}).get('pnlHistory') else None
    rec['allTimeVlm']=float(at.get('vlm',0))
    rec['maxDD']=maxdd(at.get('pnlHistory',[]),at.get('accountValueHistory',[])) if at else None
    E=[e for e in closed if e['t0']>=since_ms]
    rec['episodes']=len(E); rec['episodes_alltime']=len(closed)
    if E:
        nets=[e['net'] for e in E]
        rec['win_rate']=sum(1 for x in nets if x>0)/len(nets)
        wins=[x for x in nets if x>0]; losses=[-x for x in nets if x<0]
        rec['profit_factor']=sum(wins)/sum(losses) if losses else float('inf')
        rec['net_sum']=sum(nets)
        rec['liqs']=sum(1 for e in E if e['liq'])
        rec['top_trade_share']=max(wins)/sum(wins) if wins else None
        rec['median_hold_min']=st.median((e['t1']-e['t0'])/60000 for e in E)
        rec['leader_bps_mean']=st.mean(e['ret_bps'] for e in E)
        # copier simulation: worse entry & exit by slip_bps each, plus Invo fees both sides
        cop=[e['ret_bps']-2*slip_bps-2*fee_side_bps for e in E]
        rec['copier_bps_mean']=st.mean(cop)
        rec['copier_win_rate']=sum(1 for x in cop if x>0)/len(cop)
        rec['copier_bps_sum']=sum(cop)
        rec['coins']=collections.Counter(e['coin'] for e in E).most_common(4)
        rec['last_trade']=max(e['t1'] for e in E)
        rec['invo_share']=sum(1 for e in E if e['invo'])/len(E)
    rec['open_positions']=[(x['position']['coin'],x['position']['szi'],x['position'].get('leverage',{}).get('value')) for x in (ch or {}).get('assetPositions',[])]
    return rec
if __name__=='__main__':
    print(json.dumps(validate(sys.argv[1],float(sys.argv[2]) if len(sys.argv)>2 else 5),indent=1,default=str))
