"""Find Invo mimic leaders: wallets whose openings are followed by >=10 other Invo users
(same coin+side) within 10 minutes. Writes leaders.pkl and leader_rank.pkl."""
import urllib.request,lz4.frame,csv,io,datetime,collections,pickle,time,bisect
B='0x557edb253b1d7ed5f15b248a5a3fd919fa5d3c81'
start=datetime.date(2026,6,1); end=datetime.date(2026,9,28)
W=600  # follower window seconds
led=collections.defaultdict(list)   # wallet -> list of (ds,t,coin,side,px,notional,nfollowers,follower_notional,follower_vwap,median_lag)
nopen=collections.Counter()
d=start
while d<=end:
    ds=d.strftime('%Y%m%d'); raw=None
    for a in range(4):
        try: raw=urllib.request.urlopen(f'https://stats-data.hyperliquid.xyz/Mainnet/builder_fills/{B}/{ds}.csv.lz4',timeout=60).read(); break
        except urllib.error.HTTPError as e:
            if e.code in (403,404): break
            time.sleep(2**a)
        except Exception: time.sleep(2**a)
    if not raw: d+=datetime.timedelta(days=1); continue
    orders={}
    for r in csv.DictReader(io.StringIO(lz4.frame.decompress(raw).decode())):
        if float(r['closed_pnl'])!=0: continue
        t=datetime.datetime.fromisoformat(r['time'].replace('Z','+00:00')).timestamp()
        k=(r['user'],r['coin'],r['side'],int(t)//5)   # merge partial fills of one order (5s bucket)
        o=orders.setdefault(k,[0.0,0.0,t])
        o[0]+=float(r['px'])*float(r['sz']); o[1]+=float(r['sz']); o[2]=min(o[2],t)
    by=collections.defaultdict(list)
    for (u,c,s,_),v in orders.items(): by[(c,s)].append((v[2],u,v[0],v[0]/v[1]))
    for (c,s),lst in by.items():
        lst.sort(); ts=[x[0] for x in lst]
        for i,(t,u,n,px) in enumerate(lst):
            nopen[u]+=1
            # leader condition: no other opening of same coin/side in previous W seconds
            j0=bisect.bisect_left(ts,t-W)
            if any(lst[k][1]!=u for k in range(j0,i)): continue
            j1=bisect.bisect_right(ts,t+W)
            fol=[lst[k] for k in range(i+1,j1) if lst[k][1]!=u]
            fu={f[1] for f in fol}
            if len(fu)<5: continue
            fn=sum(f[2] for f in fol); fv=sum(f[2]*f[3] for f in fol)/fn
            lags=sorted(f[0]-t for f in fol)
            led[u].append((ds,t,c,s,px,n,len(fu),fn,fv,lags[len(lags)//2]))
    print(ds,len(orders),sum(1 for u in led),flush=True)
    d+=datetime.timedelta(days=1)
pickle.dump(dict(led=dict(led),nopen=nopen),open('leaders.pkl','wb'))
# rank: wallets with >=8 openings that pulled >=10 copiers (input for exit_sync.py)
import statistics as st
rows=[]
for u,tr in led.items():
    big=[t for t in tr if t[6]>=10]
    if len(big)<8: continue
    sl=[(1 if t[3] in ('B','Bid') else -1)*(t[8]-t[4])/t[4]*1e4 for t in big]
    rows.append((u,len(big),nopen[u],len(big)/max(nopen[u],1),st.median(t[6] for t in big),st.median(sl),st.median(t[9] for t in big),max(t[0] for t in big),sum(t[7] for t in big)))
rows.sort(key=lambda r:-(r[1]*r[3]*r[4]))
pickle.dump(rows,open('leader_rank.pkl','wb'))
print('DONE',len(rows),'candidates')
