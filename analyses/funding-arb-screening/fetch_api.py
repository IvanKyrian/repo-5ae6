import json, sys, io, zipfile, urllib.request, time
import pandas as pd
OUT = sys.argv[1]
def hl(coin, start_ms):
    rows, t = [], start_ms
    while True:
        req = urllib.request.Request("https://api.hyperliquid.xyz/info", data=json.dumps({"type":"fundingHistory","coin":coin,"startTime":t}).encode(), headers={"Content-Type":"application/json"})
        r = json.load(urllib.request.urlopen(req, timeout=30))
        if not r: break
        rows += r
        nt = r[-1]["time"] + 1
        if len(r) < 500 or nt <= t: break
        t = nt; time.sleep(0.2)
    d = pd.DataFrame(rows); d["t"] = pd.to_datetime(d.time, unit="ms").dt.floor("h"); d["rate"] = d.fundingRate.astype(float); d["hours"] = 1
    return d[["t","rate","hours"]].drop_duplicates("t")
def bn(sym, months):
    out = []
    for m in months:
        try:
            z = urllib.request.urlopen(f"https://data.binance.vision/data/futures/um/monthly/fundingRate/{sym}/{sym}-fundingRate-{m}.zip", timeout=30).read()
        except Exception as e:
            continue
        zf = zipfile.ZipFile(io.BytesIO(z)); out.append(pd.read_csv(zf.open(zf.namelist()[0])))
    d = pd.concat(out); d["t"] = pd.to_datetime(d.calc_time, unit="ms").dt.floor("h")
    return d.rename(columns={"last_funding_rate":"rate","funding_interval_hours":"hours"})[["t","rate","hours"]]
months = [p.strftime("%Y-%m") for p in pd.period_range("2025-09", "2026-11", freq="M")]
for coin, sym in [("ZEC","ZECUSDT"),("XMR","XMRUSDT")]:
    hl(coin, 0).to_csv(f"{OUT}/hl_{coin}.csv", index=False)
    bn(sym, months).to_csv(f"{OUT}/bn_{sym}.csv", index=False)
    print(coin, "done")
