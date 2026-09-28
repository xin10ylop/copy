import urllib.request,lz4.frame,datetime,json
B='0x557edb253b1d7ed5f15b248a5a3fd919fa5d3c81'
d=datetime.date(2026,4,1); out={}
while d<=datetime.date(2026,9,27):
    ds=d.strftime('%Y%m%d')
    try:
        raw=urllib.request.urlopen(f'https://stats-data.hyperliquid.xyz/Mainnet/builder_fills/{B}/{ds}.csv.lz4',timeout=60).read()
        lines=lz4.frame.decompress(raw).decode().rstrip().split('\n')
        out[ds]=[lines[1][:20],lines[-1][:20]]
    except Exception as e: out[ds]=str(e)
    d+=datetime.timedelta(days=1)
json.dump(out,open('coverage.json','w'),indent=0)
print('DONE')
