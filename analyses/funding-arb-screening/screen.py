"""Funding arb screening: one row per arb (long Binance, short Hyperliquid).

Usage:
  python3 -I screen.py --data "<folder with funding CSVs>" --positions other.xlsx --end 2026-11-24 --out .

Input CSVs: one per venue/symbol, columns Time, funding_rate (annualized, e.g. "11.0%").
Each row is one settlement. Binance oil settles every 4h, Binance XMR/ZEC every 8h,
Hyperliquid every 1h.
"""
import argparse, glob, json, os
import pandas as pd

LEVERAGE = 5
APR_MULT = LEVERAGE / 2  # leg notional / total margin (both legs at 5x) = 2.5

ARBS = [
    # name, long (Binance) file prefix, short (Hyperliquid) file prefix, interval h of Binance, start override
    ("Brent", "Binance_BZUSDT", "HyperLiquid_BRENTOIL", 4, "2026-05-01"),
    ("WTI", "Binance_CLUSDT", "HyperLiquid_WTIOIL", 4, "2026-05-01"),
    ("XMR", "Binance_XMRUSDT", "HyperLiquid_XMR", 8, "2026-01-16"),  # 15 Jan: HL data starts 09:00 (partial day)
    ("ZEC", "Binance_ZECUSDT", "HyperLiquid_ZEC", 8, None),
]

# Rows in the positions sheet: (Binance row asset, Hyperliquid row asset). The sheet lists
# WTI as "CL / Hyperliquid" and "WTI / Binance"; CL is the Binance ticker, so the platform
# labels look swapped. We take Binance = CL row's OI, Hyperliquid = WTI row's OI (see README).
POS = {"Brent": ("BZ", "BRENT"), "WTI": ("CL", "WTI"), "XMR": ("XMR", "XMR"), "ZEC": ("ZEC", "ZEC")}


def daily(folder, prefix, interval_h):
    f = glob.glob(os.path.join(folder, prefix + "*.csv"))
    assert len(f) == 1, (prefix, f)
    d = pd.read_csv(f[0])
    d["t"] = pd.to_datetime(d["Time"])
    d["r"] = d["funding_rate"].str.rstrip("%").astype(float) / 100  # annualized
    d["ret"] = d["r"] * interval_h / 8760  # funding actually paid in that settlement, fraction of notional
    d["date"] = d["t"].dt.normalize()
    return d.groupby("date").agg(ret=("ret", "sum"), n=("r", "size"))


def drawdown(s):
    """s: daily spread (fraction of notional). Worst peak-to-trough of cumulative funding."""
    cum = s.cumsum()
    peak = cum.cummax().clip(lower=0)  # start counts as a peak at 0
    dd = cum - peak
    trough = dd.idxmin()
    depth = dd.min()
    before = cum.loc[:trough]
    # peak date = last date the running max was set before the trough (or inception if never above 0)
    pk_val = peak.loc[trough]
    hits = before[before >= pk_val - 1e-15]
    peak_date = hits.index[-1] if len(hits) and pk_val > 0 else None
    window = s.loc[s.index > peak_date] if peak_date is not None else s
    window = window.loc[:trough]
    after = cum.loc[trough:]
    rec = after[after >= pk_val - 1e-15]
    rec_date = rec.index[0] if len(rec) else None
    return dict(
        depth=depth,
        start=(window.index[0] if len(window) else trough),
        peak_date=peak_date,
        trough=trough,
        days_peak_to_trough=len(window),
        avg_spread_ann=window.mean() * 365,
        recovered=rec_date,
        days_to_recover=(rec_date - trough).days if rec_date is not None else None,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--positions", required=True)
    ap.add_argument("--end", required=True, help="last full UTC day to include, YYYY-MM-DD")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    end = pd.Timestamp(a.end)

    px = pd.read_excel(a.positions, header=None)
    aum = float(px[px.eq("Portfolio AuM").any(axis=1)].iloc[0].dropna().iloc[-1])
    hdr = px[px.eq("Notional Exposure").any(axis=1)].index[0]
    pos = px.iloc[hdr + 1:].dropna(how="all", axis=0).dropna(how="all", axis=1)
    pos.columns = ["asset", "platform", "notional", "oi", "oi_pct"]
    pos = pos.dropna(subset=["asset"])

    rows, checks = [], []
    for name, bfile, hfile, bint, start in ARBS:
        B = daily(a.data, bfile, bint)
        H = daily(a.data, hfile, 1)
        j = B.join(H, lsuffix="_bin", rsuffix="_hl", how="inner")
        first_both = j.index.min()
        if start:
            j = j[j.index >= pd.Timestamp(start)]
        j = j[j.index <= end]
        s = j["ret_hl"] - j["ret_bin"]  # short HL receives HL funding, long Binance pays Binance funding

        exp_bin = 24 // bint
        bad = j[(j.n_bin != exp_bin) | (~j.n_hl.isin([23, 24, 25]))]
        gaps = pd.date_range(j.index.min(), j.index.max()).difference(j.index)
        checks.append(f"{name}: {len(j)} days {j.index.min().date()}..{j.index.max().date()}, "
                      f"days with unexpected settlement count: {len(bad)}, missing days: {len(gaps)}")

        win = lambda n: s.iloc[-n:].mean() * 365
        sp = {"7d": win(7), "30d": win(30), "90d": win(90), "inception": s.mean() * 365}
        dd = drawdown(s)

        bn, hn = POS[name]
        pb = pos[(pos.asset == bn) & (pos.platform == "Binance")].iloc[0] if name != "WTI" else pos[pos.asset == "CL"].iloc[0]
        ph = pos[(pos.asset == hn) & (pos.platform == "Hyperliquid")].iloc[0] if name != "WTI" else pos[pos.asset == "WTI"].iloc[0]
        n_bin, n_hl = float(pb.notional), float(ph.notional)
        hedged = min(n_bin, n_hl)
        rows.append(dict(
            arb=name,
            data_from=str(s.index.min().date()),
            first_overlap=str(first_both.date()),
            **{f"spread_{k}": v for k, v in sp.items()},
            **{f"apr_{k}": v * APR_MULT for k, v in sp.items()},
            dd_pct=dd["depth"],
            dd_from=str(dd["start"].date()),
            dd_to=str(dd["trough"].date()),
            dd_days=dd["days_peak_to_trough"],
            dd_avg_spread=dd["avg_spread_ann"],
            dd_avg_apr=dd["avg_spread_ann"] * APR_MULT,
            dd_recovered=str(dd["recovered"].date()) if dd["recovered"] is not None else None,
            dd_days_to_recover=dd["days_to_recover"],
            notional_bin=n_bin,
            notional_hl=n_hl,
            notional_hedged=hedged,
            pct_aum=hedged / aum,
            margin_5x=2 * hedged / LEVERAGE,
            margin_pct_aum=2 * hedged / LEVERAGE / aum,
            oi_bin=float(pb.oi), oi_pct_bin=n_bin / float(pb.oi),
            oi_hl=float(ph.oi), oi_pct_hl=n_hl / float(ph.oi),
            dd_pnl_current=dd["depth"] * hedged,
            dd_pct_margin=dd["depth"] * APR_MULT,
        ))

    df = pd.DataFrame(rows)
    os.makedirs(a.out, exist_ok=True)
    df.to_csv(os.path.join(a.out, "screening.csv"), index=False)
    with open(os.path.join(a.out, "numbers.json"), "w") as f:
        json.dump(dict(aum=aum, end=a.end, leverage=LEVERAGE, rows=rows), f, indent=1, default=str)
    print("AuM", aum)
    print("\n".join(checks))
    pd.set_option("display.width", 250, "display.max_columns", 50)
    print(df.T)


if __name__ == "__main__":
    main()
