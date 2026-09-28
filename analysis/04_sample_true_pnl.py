import pickle,random,json,time,urllib.request
A=pickle.load(open('fills_agg.pkl','rb'))
users=A['users']
random.seed(42)
allu=list(users.keys())
rand=random.sample(allu,300)
top=sorted(allu,key=lambda u:-users[u][3])[:100]
out={}
def post(body):
    for a in range(5):
        try:
            req=urllib.request.Request('https://api.hyperliquid.xyz/info',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
            return json.loads(urllib.request.urlopen(req,timeout=60).read())
        except Exception as e:
            time.sleep(3*(a+1))
    return None
for grp,lst in [('random',rand),('top',top)]:
    for u in lst:
        p=post({'type':'portfolio','user':u})
        st=post({'type':'clearinghouseState','user':u})
        rec={'grp':grp}
        if p:
            d=dict(p)
            at=d.get('allTime') or d.get('perpAllTime')
            pat=d.get('perpAllTime')
            def last(x,key): 
                try: return float(x[key][-1][1])
                except: return None
            rec['allTimePnl']=last(d['allTime'],'pnlHistory') if 'allTime' in d else None
            rec['perpAllTimePnl']=last(d['perpAllTime'],'pnlHistory') if 'perpAllTime' in d else None
            rec['acctVal']=last(d['allTime'],'accountValueHistory') if 'allTime' in d else None
            rec['vlm']=float(d['allTime'].get('vlm',0)) if 'allTime' in d else None
            try: rec['maxAcct']=max(float(x[1]) for x in d['allTime']['accountValueHistory'])
            except: pass
        if st: rec['curAcct']=float(st['marginSummary']['accountValue']); rec['openPos']=len(st['assetPositions'])
        out[u]=rec
        time.sleep(1.2)
    json.dump(out,open('sample_pnl.json','w'))
print('DONE',len(out))
