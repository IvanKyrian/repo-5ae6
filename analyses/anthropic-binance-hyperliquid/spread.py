#!/usr/bin/env python3
"""Per-share spread between Binance ANTHROPICUSDT and Hyperliquid xyz:ANT.

Conversion follows the Cross-venue tab of the Anthropic pre-IPO perps model:
  Binance quotes valuation / 1B, so Binance per share = price * 1e9 / 12.7e9.
  xyz:ANT quotes one share.
  spread = Binance per share / xyz price - 1   (short Binance / long xyz)

Sources
  Binance 5m and 1m closes : data.binance.vision daily files (published the next morning, UTC)
  Binance today            : the model's "5m candles" tab (--xlsx), for days the portal has not published
  Binance live             : CoinGecko /derivatives (last price), paired with the xyz 1m close of the same minute
  xyz:ANT                  : Hyperliquid info API candleSnapshot

fapi.binance.com refuses cloud IPs in restricted regions, so the script never calls it.

  python3 spread.py --xlsx Anthropic_1.xlsx --start 2026-11-02 --entry "2026-11-08 01:26" --out anthropic_prices.csv
"""
import argparse, csv, datetime as dt, io, json, statistics, urllib.error, urllib.request, zipfile

UTC = dt.timezone.utc
EXCHANGE_SHARES = 12.7e9  # model, Cross-venue!B5
BINANCE_UNIT = 1e9        # model, Cross-venue!E9
UA = {"User-Agent": "spread-monitor/1.0", "Content-Type": "application/json"}


def get(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers=UA)
    return urllib.request.urlopen(req, timeout=60).read()


def ms(t):
    return int(t.timestamp() * 1000)


def utc(ms_):
    return dt.datetime.fromtimestamp(ms_ / 1000, UTC)


def binance_day(day, interval):
    url = (f"https://data.binance.vision/data/futures/um/daily/klines/ANTHROPICUSDT/{interval}/"
           f"ANTHROPICUSDT-{interval}-{day:%Y-%m-%d}.zip")
    try:
        z = zipfile.ZipFile(io.BytesIO(get(url)))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {}
        raise
    text = z.read(z.namelist()[0]).decode()
    return {utc(int(r["open_time"])): float(r["close"]) for r in csv.DictReader(io.StringIO(text))}


def xyz(interval, t0, t1):
    body = {"type": "candleSnapshot", "req": {"coin": "xyz:ANT", "interval": interval, "startTime": ms(t0), "endTime": ms(t1)}}
    return {utc(c["t"]): float(c["c"]) for c in json.loads(get("https://api.hyperliquid.xyz/info", body))}


def excel_binance(path):
    import openpyxl
    ws = openpyxl.load_workbook(path, data_only=True, read_only=True)["5m candles"]
    out = {}
    for t, b, *_ in ws.iter_rows(min_row=2, max_col=2, values_only=True):
        if isinstance(t, dt.datetime) and isinstance(b, (int, float)):
            out[utc(round(t.replace(tzinfo=UTC).timestamp() / 60) * 60000)] = float(b)
    return out


def coingecko_binance():
    rows = json.loads(get("https://api.coingecko.com/api/v3/derivatives?include_tickers=unexpired"))
    r = next(x for x in rows if x.get("market") == "Binance (Futures)" and x.get("symbol") == "ANTHROPICUSDT")
    return dt.datetime.fromtimestamp(r["last_traded_at"], UTC), float(r["price"])


def spread(binance, xyz_px):
    return binance * BINANCE_UNIT / EXCHANGE_SHARES / xyz_px - 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2026-11-02")
    ap.add_argument("--entry", default="2026-11-08 01:26", help="entry minute, UTC")
    ap.add_argument("--xlsx", help="model workbook; fills Binance for days the portal has not published")
    ap.add_argument("--no-live", action="store_true")
    ap.add_argument("--out", default="anthropic_prices.csv")
    a = ap.parse_args()

    start = dt.datetime.fromisoformat(a.start).replace(tzinfo=UTC)
    entry = dt.datetime.fromisoformat(a.entry).replace(tzinfo=UTC)
    now = dt.datetime.now(UTC)

    bn, src = {}, {}
    day = start.date()
    while day <= now.date():
        for t, v in binance_day(day, "5m").items():
            bn[t], src[t] = v, "Binance data portal (data.binance.vision)"
        day += dt.timedelta(days=1)
    if a.xlsx:
        for t, v in excel_binance(a.xlsx).items():
            if t >= start and t not in bn:
                bn[t], src[t] = v, "Anthropic_1.xlsx, 5m candles tab"

    x5 = xyz("5m", start, now)
    last_closed = now.replace(second=0, microsecond=0) - dt.timedelta(minutes=now.minute % 5 + 5)
    rows = []
    for t in sorted(set(x5) | {k for k in bn if k >= start}):
        if start <= t <= last_closed:
            rows.append([t, "5m", bn.get(t), x5.get(t), src.get(t, ""), "Hyperliquid API, xyz:ANT 5m candle" if t in x5 else ""])

    b1 = binance_day(entry.date(), "1m")
    x1 = xyz("1m", entry - dt.timedelta(minutes=5), entry + dt.timedelta(minutes=5))
    rows.append([entry, "1m entry", b1.get(entry), x1.get(entry), "Binance data portal (data.binance.vision), 1m candle", "Hyperliquid API, xyz:ANT 1m candle"])

    if not a.no_live:
        tq, px = coingecko_binance()
        xl = xyz("1m", tq - dt.timedelta(minutes=5), now)
        xm = xl.get(tq.replace(second=0, microsecond=0))
        if xm is not None:
            rows.append([tq, "live quote", px, xm, "CoinGecko derivatives feed, Binance ANTHROPICUSDT last price",
                         "Hyperliquid API, xyz:ANT 1m candle close at the same minute"])

    rows.sort(key=lambda r: (r[0], r[1]))
    with open(a.out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["time_utc", "interval", "binance_close", "xyz_close", "binance_source", "xyz_source"])
        for t, iv, b, x, sb, sx in rows:
            w.writerow([t.strftime("%Y-%m-%d %H:%M:%S"), iv, "" if b is None else repr(b), "" if x is None else repr(x), sb, sx])

    paired = [(r[0], r[1], spread(r[2], r[3])) for r in rows if r[2] is not None and r[3] is not None]
    c = [p for p in paired if p[1] == "5m"]
    v = [p[2] for p in c]
    print(f"{len(c)} paired 5m closes, {c[0][0]:%d %b %H:%M} to {c[-1][0]:%d %b %H:%M} UTC")
    print(f"min {min(v):.2%}  max {max(v):.2%}  mean {statistics.mean(v):.2%}  last candle {v[-1]:.2%}")
    for t, iv, s in paired:
        if iv != "5m":
            print(f"{iv:10s} {t:%d %b %H:%M:%S} UTC  {s:.2%}")


if __name__ == "__main__":
    main()
