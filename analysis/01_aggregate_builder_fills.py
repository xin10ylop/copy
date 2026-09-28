import lz4.frame, csv, io, json, sys, datetime, urllib.request, collections, os, time, pickle
B='0x557edb253b1d7ed5f15b248a5a3fd919fa5d3c81'
start=datetime.date(2025,12,1); end=datetime.date(2026,9,27)
days={}
users={}   # user -> [first_day, last_day, vol, bfee, hlfee, closed_pnl, nfills, set(days) count]
udays=collections.defaultdict(set)
coins=collections.Counter(); coinfee=collections.Counter()
d=start
while d<=end:
    ds=d.strftime('%Y%m%d')
    url=f'https://stats-data.hyperliquid.xyz/Mainnet/builder_fills/{B}/{ds}.csv.lz4'
    raw=None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url,timeout=60) as r: raw=r.read(); break
        except urllib.error.HTTPError as e:
            if e.code in (403,404): raw=b''; break
            time.sleep(2**attempt)
        except Exception as e:
            time.sleep(2**attempt)
    if not raw:
        d+=datetime.timedelta(days=1); continue
    txt=lz4.frame.decompress(raw).decode()
    rd=csv.DictReader(io.StringIO(txt))
    dv=dict(vol=0.0,bfee=0.0,hlfee=0.0,pnl=0.0,fills=0,users=set(),taker_vol=0.0,liq=0)
    for row in rd:
        u=row['user']; px=float(row['px']); sz=float(row['sz']); n=px*sz
        bf=float(row['builder_fee'] or 0); pnl=float(row['closed_pnl'] or 0)
        taker = row['crossed']=='true'
        hl = n*(0.00045 if taker else 0.00015)
        dv['vol']+=n; dv['bfee']+=bf; dv['hlfee']+=hl; dv['pnl']+=pnl; dv['fills']+=1; dv['users'].add(u)
        if taker: dv['taker_vol']+=n
        if row.get('special_trade_type','Na')!='Na': dv['liq']+=1
        s=users.get(u)
        if s is None: s=users[u]=[ds,ds,0.0,0.0,0.0,0.0,0]
        s[1]=ds; s[2]+=n; s[3]+=bf; s[4]+=hl; s[5]+=pnl; s[6]+=1
        udays[u].add(ds)
        coins[row['coin']]+=n; coinfee[row['coin']]+=bf
    dv['nusers']=len(dv['users']); del dv['users']
    days[ds]=dv
    print(ds, round(dv['vol']/1e6,2),'M', round(dv['bfee']), dv['nusers'], flush=True)
    d+=datetime.timedelta(days=1)
pickle.dump(dict(days=days,users=users,udays={k:sorted(v) for k,v in udays.items()},coins=coins,coinfee=coinfee),open('fills_agg.pkl','wb'))
print('DONE', len(users))
