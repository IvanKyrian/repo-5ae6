#!/usr/bin/env python3
"""Which venues actually feed the XMR oracle (Hyperliquid) and index (Binance)?

Hyperliquid's documented rule: oracle = weighted median of spot mid prices on
Binance 3, OKX 2, Bybit 2, Kraken 1, KuCoin 1, Gate 1, MEXC 1, Hyperliquid spot 1.
This script checks which of those venues list XMR spot right now, rebuilds the
weighted median from the ones that do, and compares it with Hyperliquid's live
oraclePx. It also prints Binance's own index constituents for XMRUSDT.

Usage: python3 xmr_oracle_check.py [samples] [seconds_between]
Only uses public endpoints and the standard library.
"""
import json
import sys
import time
import urllib.request

TIMEOUT = 10


def get(url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", "User-Agent": "xmr-oracle-check"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read())


# Each venue returns (bid, ask) for XMR spot, or raises if XMR isn't listed.
def binance():
    d = get("https://api.binance.com/api/v3/ticker/bookTicker?symbol=XMRUSDT")
    return float(d["bidPrice"]), float(d["askPrice"])


def okx():
    d = get("https://www.okx.com/api/v5/market/ticker?instId=XMR-USDT")["data"][0]
    return float(d["bidPx"]), float(d["askPx"])


def bybit():
    d = get("https://api.bybit.com/v5/market/tickers?category=spot&symbol=XMRUSDT")["result"]["list"][0]
    return float(d["bid1Price"]), float(d["ask1Price"])


def kraken():  # quoted in USD, not USDT
    d = get("https://api.kraken.com/0/public/Ticker?pair=XMRUSD")
    if d.get("error"):
        raise ValueError(d["error"])
    t = next(iter(d["result"].values()))
    return float(t["b"][0]), float(t["a"][0])


def kucoin():
    d = get("https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=XMR-USDT")["data"]
    return float(d["bestBid"]), float(d["bestAsk"])


def gate():
    d = get("https://api.gateio.ws/api/v4/spot/tickers?currency_pair=XMR_USDT")[0]
    return float(d["highest_bid"]), float(d["lowest_ask"])


def mexc():
    d = get("https://api.mexc.com/api/v3/ticker/bookTicker?symbol=XMRUSDT")
    return float(d["bidPrice"]), float(d["askPrice"])


VENUES = [("Binance", 3, binance), ("OKX", 2, okx), ("Bybit", 2, bybit), ("Kraken (USD)", 1, kraken),
          ("KuCoin", 1, kucoin), ("Gate", 1, gate), ("MEXC", 1, mexc)]


def hl_perp():
    meta, ctxs = get("https://api.hyperliquid.xyz/info", {"type": "metaAndAssetCtxs"})
    i = next(k for k, a in enumerate(meta["universe"]) if a["name"] == "XMR")
    c = ctxs[i]
    return float(c["oraclePx"]), float(c["markPx"]), c.get("premium"), c.get("funding")


def hl_spot_lists_xmr():
    meta = get("https://api.hyperliquid.xyz/info", {"type": "spotMeta"})
    return any(t["name"].upper() in ("XMR", "UXMR") for t in meta["tokens"])


def weighted_median(points):
    points = sorted(points)
    half = sum(w for _, w in points) / 2
    acc = 0
    for px, w in points:
        acc += w
        if acc >= half:
            return px


def snapshot():
    rows = []
    for name, w, fn in VENUES:
        try:
            bid, ask = fn()
            rows.append((name, w, (bid + ask) / 2, None))
        except Exception as e:
            rows.append((name, w, None, type(e).__name__))
    oracle, mark, premium, funding = hl_perp()
    listed = [(mid, w) for _, w, mid, _ in rows if mid is not None]
    return rows, oracle, mark, premium, funding, (weighted_median(listed) if listed else None)


def main():
    samples = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    gap = float(sys.argv[2]) if len(sys.argv) > 2 else 10

    print("Binance XMRUSDT index constituents:")
    try:
        print(json.dumps(get("https://fapi.binance.com/fapi/v1/constituents?symbol=XMRUSDT"), indent=2))
        pi = get("https://fapi.binance.com/fapi/v1/premiumIndex?symbol=XMRUSDT")
        print(f"Binance index {pi['indexPrice']}  mark {pi['markPrice']}  last funding {pi['lastFundingRate']}")
    except Exception as e:
        print("  could not fetch:", e)
    try:
        print("Hyperliquid spot lists XMR:", hl_spot_lists_xmr())
    except Exception as e:
        print("  could not check Hyperliquid spot:", e)

    diffs = []
    for n in range(samples):
        rows, oracle, mark, premium, funding, rebuilt = snapshot()
        if n == 0:
            print("\nVenue           weight   XMR spot mid")
            for name, w, mid, err in rows:
                print(f"{name:<15} {w:>6}   {f'{mid:.3f}' if mid else 'not listed / error (' + str(err) + ')'}")
        bps = (rebuilt / oracle - 1) * 1e4 if rebuilt else float("nan")
        diffs.append(bps)
        print(f"[{n + 1}/{samples}] HL oracle {oracle:.3f}  rebuilt median {rebuilt}  diff {bps:+.1f} bps  "
              f"| HL mark {mark:.3f}  premium {premium}  funding/h {funding}")
        if n < samples - 1:
            time.sleep(gap)
    if samples > 1:
        ok = [d for d in diffs if d == d]
        print(f"\nAvg |diff| rebuilt vs HL oracle: {sum(abs(d) for d in ok) / len(ok):.2f} bps over {len(ok)} samples")
        print("Within ~1-2 bps on most samples means the venue list above is what feeds the oracle.")


if __name__ == "__main__":
    main()
