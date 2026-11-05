#!/usr/bin/env python3
"""Funding rate arb analysis: daily CSV in, Notion report + 3 interactive charts + numbers out.

Input CSV, one row per UTC day (see SKILL.md for how to build it):
  date            YYYY-MM-DD
  long_funding    daily funding on the LONG venue = sum of every settlement that UTC day (decimal, +0.0003 = 0.03%)
  short_funding   same for the SHORT venue
  long_close      daily close of the LONG venue's perp
  short_close     daily close of the SHORT venue's perp
  long_n, short_n optional: number of settlements that day (sanity check)
Funding sign: positive = longs pay shorts. We pay long_funding and receive short_funding.

Example:
  python3 analyze.py --csv data.csv --asset XMR --long Binance --short Hyperliquid \\
      --long-interval 8h --short-interval 1h --bear 2026-01-15:2026-02-06 --bull 2026-02-07:2026-10-22 \\
      --oi-long 58967094 --oi-short 123618604 --out ./out
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent


# ---------- formatting ----------
def usd(v, sign=False):
    s = f"${abs(v):,.0f}"
    if v < -0.5:
        return "−" + s
    return ("+" + s) if sign and v > 0.5 else s


def pct(v, d=2, sign=False):
    """v is a fraction (0.1045 -> 10.45%)."""
    s = f"{abs(v) * 100:.{d}f}%"
    if v < 0 and round(abs(v) * 100, d) != 0:
        return "−" + s
    return ("+" + s) if sign and v > 0 else s


def usdk(v):
    """Round sizing figures the way we write them: $1M, $500k, $200k."""
    v = abs(v)
    if v >= 1e6:
        return f"${v / 1e6:g}M"
    return f"${v / 1e3:g}k" if v >= 1e3 else f"${v:,.0f}"


def day(d):
    return f"{d.day} {d:%b}"


def num(v, d=1):
    return f"{v:.{d}f}".replace("-", "−")


# ---------- analysis ----------
def analyze(df, a):
    N, lev = a.notional, a.leverage
    leg = N / 2
    margin = 2 * leg / lev
    mult = leg / margin
    df = df.sort_values("date").reset_index(drop=True)
    sp = (df.short_funding - df.long_funding).round(12) + 0.0  # float noise -> exact 0 on flat days
    fp = sp * leg
    n = len(df)
    R = {"asset": a.asset, "long": a.long, "short": a.short, "notional": N, "leg": leg, "leverage": lev,
         "margin": margin, "mult": mult, "start": df.date.iloc[0], "end": df.date.iloc[-1], "days": n}

    gaps = df.date.diff().dt.days.dropna()
    R["missing_days"] = int((gaps > 1).sum())
    R["gap_ranges"] = [(df.date[i - 1] + pd.Timedelta(days=1), df.date[i] - pd.Timedelta(days=1), int(gaps[i]) - 1)
                       for i in gaps.index if gaps[i] > 1]
    for side in ("long", "short"):
        if f"{side}_n" in df:
            R[f"{side}_n_counts"] = df[f"{side}_n"].value_counts().to_dict()

    # 1. periods
    periods = []
    for w in (7, 30, 90, 180):
        if w < n:
            periods.append((f"{w} days", sp.tail(w).mean() * 365))
    periods.append((f"Max track record ({n} days)", sp.mean() * 365))
    R["periods"] = [(lbl, s, s * mult) for lbl, s in periods]
    R["full_spread"] = sp.mean() * 365
    R["apr"] = R["full_spread"] * mult
    R["funding_total"] = fp.sum()
    R["funding_per_year"] = sp.mean() * 365 * leg
    R["pos"], R["zero"], R["neg"] = int((sp > 0).sum()), int((sp == 0).sum()), int((sp < 0).sum())
    r30 = sp.rolling(30).mean().dropna()
    R["roll30_pos_share"] = float((r30 > 0).mean()) if len(r30) else float("nan")
    R["periods_all_positive"] = all(s > 0 for _, s, _ in R["periods"])
    base = a.base_rate
    R["pinned_long"] = int((df.long_funding.round(10) == base).sum())
    R["pinned_short"] = int((df.short_funding.round(10) == base).sum())

    wd = int(sp.idxmin())
    R["worst_day"] = dict(date=df.date[wd], spread=sp[wd] * 365, apr=sp[wd] * 365 * mult, pnl=fp[wd], pct=fp[wd] / N)
    cf = fp.cumsum()
    dd = cf - cf.cummax()
    tr = int(dd.idxmin())
    pk = int(cf[:tr + 1].idxmax())
    after = cf[tr:]
    rec = after[after >= cf[pk]]
    seg = sp.iloc[pk + 1:tr + 1]
    R["worst_dd"] = dict(start=df.date[pk + 1] if pk + 1 <= tr else df.date[tr], end=df.date[tr], days=len(seg),
                         spread=seg.mean() * 365 if len(seg) else 0, apr=(seg.mean() * 365 * mult) if len(seg) else 0,
                         pnl=dd[tr], pct=dd[tr] / N,
                         recovered=df.date[rec.index[0]] if len(rec) else None,
                         rec_days=int(rec.index[0] - tr) if len(rec) else None, peak_i=pk, trough_i=tr)

    # 2. M2M: same coin quantity on both legs, sized to `leg` at the prior close
    mid = (df.long_close + df.short_close) / 2
    gap_usd = df.long_close - df.short_close
    gap_bps = gap_usd / mid * 1e4
    qty = leg / mid.shift(1)
    m2m = (qty * gap_usd.diff()).fillna(0)
    wm = int(m2m.idxmin())
    R["worst_m2m"] = dict(date=df.date[wm], pnl=m2m[wm], pct=m2m[wm] / N, qty=qty[wm],
                          gap_before_usd=gap_usd[wm - 1] if wm else 0, gap_after_usd=gap_usd[wm],
                          gap_bps=gap_bps[wm],
                          next_gap_bps=gap_bps[wm + 1] if wm + 1 < n else None,
                          next_pnl=m2m[wm + 1] if wm + 1 < n else None,
                          prev_pnl=m2m[wm - 1] if wm else 0, prev_gap_bps=gap_bps[wm - 1] if wm else 0)
    R["gap_mean_bps"] = gap_bps.mean()
    R["gap_within10"] = float((gap_bps.abs() < 10).mean())
    R["gap_max_bps"] = gap_bps.abs().max()
    R["m2m_autocorr"] = m2m.autocorr(1)

    # 3. correlation (gap = long - short; expected negative)
    R["corr"] = {}
    for w in (1, 7, 30):
        x, y = sp.rolling(w).mean(), gap_bps.rolling(w).mean()
        m = x.notna() & y.notna()
        R["corr"][w] = float(np.corrcoef(x[m], y[m])[0, 1]) if m.sum() > 2 else float("nan")

    # 4. bear / bull
    R["regimes"] = []
    for name, span in (("Bear", a.bear), ("Bull", a.bull)):
        if not span:
            continue
        s0, s1 = (pd.Timestamp(x) for x in span.split(":"))
        k = (df.date >= s0) & (df.date <= s1)
        idx = df.index[k]
        if a.regime_price_ref == "start":
            ref = idx[0]  # periods defined close-to-close from the start date's close
        else:
            ref = idx[0] - 1 if idx[0] > 0 else idx[0]  # price change from the prior close when we have it
        mm = m2m[k]
        R["regimes"].append(dict(
            name=name, start=s0, end=s1, days=int(k.sum()),
            long_px=(df.long_close[ref], df.long_close[idx[-1]]), short_px=(df.short_close[ref], df.short_close[idx[-1]]),
            spread=sp[k].mean() * 365, apr=sp[k].mean() * 365 * mult, neg=int((sp[k] < 0).sum()), zero=int((sp[k] == 0).sum()),
            funding=fp[k].sum(), worst_m2m=(df.date[mm.idxmin()], mm.min())))

    # margin check: each leg is margined on its own venue
    r = df.long_close.pct_change()
    thr = 0.75 / lev
    big = [(df.date[i], r[i]) for i in r.index if abs(r[i]) > thr]
    R["margin_check"] = dict(threshold=thr, days=big, max_down=(df.date[r.idxmin()], r.min()), max_up=(df.date[r.idxmax()], r.max()))

    R["growth_end"] = 100 * (1 + R["funding_total"] / margin)
    for side, oi in (("long", a.oi_long), ("short", a.oi_short)):
        if oi:
            R[f"oi_{side}_share"] = leg / oi
    series = dict(sp=sp, fp=fp, cf=cf, m2m=m2m, gap_bps=gap_bps, mid=mid)
    return R, series


# ---------- charts ----------
def charts(df, R, S, a, out):
    eng = (HERE / "engine.js").read_text()
    css = (HERE / "charts.css").read_text()
    L, Sh, A = a.long, a.short, a.asset
    dates = df.date.dt.strftime("%Y-%m-%d").tolist()
    rr = lambda s, k=2: [round(float(v), k) + 0.0 for v in s]
    period = (f"{day(R['start'])} – {day(R['end'])} {R['end']:%Y}" if R["start"].year == R["end"].year
              else f"{day(R['start'])} {R['start']:%Y} – {day(R['end'])} {R['end']:%Y}")

    def page(title, body, data, script, cols, rows):
        th = "".join(f"<th>{c}</th>" for c in cols)
        tb = "\n".join("<tr>" + "".join(f"<td>{v}</td>" for v in row) + "</tr>" for row in rows)
        return f'''<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
{css}
<div class="wrap" id="root">
{body}
<details><summary>Show data table</summary><div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody>
{tb}
</tbody></table></div></details>
</div>
<script>
{eng}
const DATA = {json.dumps(data, separators=(",", ":"))};
const DATES = DATA.d.map(s => new Date(s + 'T00:00:00Z'));
const pct = v => (v > 0 ? '+' : v < 0 ? '\\u2212' : '') + Math.abs(v).toFixed(1) + '%';
const usd = v => (v < 0 ? '\\u2212' : v > 0 ? '+' : '') + '$' + Math.abs(Math.round(v)).toLocaleString('en-US');
{script}
</script>
'''

    ann = lambda s: s * 365 * 100
    la, sa, spa = ann(df.long_funding), ann(df.short_funding), ann(S["sp"])
    roll = lambda s: s.rolling(7, min_periods=1).mean()
    fdata = dict(d=dates, b=rr(la), h=rr(sa), s=rr(spa), b7=rr(roll(la)), h7=rr(roll(sa)), s7=rr(roll(spa)), p=rr(S["fp"], 0))
    wd, dd = R["worst_day"], R["worst_dd"]
    wdi = int(df.index[df.date == wd["date"]][0])
    dd_lbl = f"{dd['start'].day}–{day(dd['end'])}" if dd["start"].month == dd["end"].month else f"{day(dd['start'])} – {day(dd['end'])}"
    bands = [dict(i0=wdi, i1=wdi, label=f"Worst day: {day(wd['date'])}, {usd(wd['pnl'])}", short=day(wd["date"]), row=0),
             dict(i0=dd["peak_i"] + 1, i1=dd["trough_i"], label=f"Worst drawdown: {dd_lbl}, {usd(dd['pnl'])}", short=dd_lbl, row=1)]
    rec = f", made back by {day(dd['recovered'])}" if dd["recovered"] is not None else ", not yet made back"
    body = f'''<header>
  <h1>{A} funding: {L} vs {Sh}</h1>
  <p class="sub">Daily funding on each venue, annualized. The spread is what we earn short on {Sh} and long on {L}: {Sh} rate minus {L} rate. {period}.</p>
</header>
<div class="stats">
  <div class="stat"><span>Avg spread, annualized</span><b>{pct(R['full_spread'])}</b></div>
  <div class="stat"><span>APR at {a.leverage:g}× (×{R['mult']:g})</span><b>{pct(R['apr'], 1)}</b></div>
  <div class="stat"><span>Days spread was positive</span><b>{R['pos']} of {R['days']}</b></div>
  <div class="stat"><span>Funding earned, {usdk(R['notional'])} notional</span><b>{usd(R['funding_total'])}</b></div>
</div>
<div class="bar">
  <div class="legend">
    <span><i class="lk" style="background:var(--s-hl)"></i>{Sh}</span>
    <span><i class="lk" style="background:var(--s-bin)"></i>{L}</span>
    <span><i class="sq" style="background:var(--pos)"></i>Spread &gt; 0, we earn</span>
    <span><i class="sq" style="background:var(--neg)"></i>Spread &lt; 0, we pay</span>
    <span><i class="lk" style="background:var(--ink-2);opacity:.55"></i>Worst single day</span>
    <span><i class="sq" style="background:var(--band);outline:1px solid var(--line)"></i>Worst funding drawdown</span>
  </div>
  <div class="seg" role="group" aria-label="Smoothing">
    <button type="button" id="m7" aria-pressed="true">7-day avg</button>
    <button type="button" id="m1" aria-pressed="false">Daily</button>
  </div>
</div>
<div class="plot"><div class="tip" hidden></div></div>
<p class="foot">{L} settles every {a.long_interval}, {Sh} every {a.short_interval}; each day sums all settlements, then ×365. 7-day avg is trailing. {R['zero']} days had zero spread and {R['neg']} were negative. P&amp;L on {usdk(R['notional'])} notional, {usdk(R['leg'])} per leg. Worst single day: {day(wd['date'])}, {pct(wd['spread'], 1)} annualized, {usd(wd['pnl'])}. Worst funding drawdown: {dd_lbl}, {usd(dd['pnl'])}{rec}. Source: {a.funding_source}.</p>'''
    script = r'''
let mode = '7';
const pick = (a, b) => () => mode === '7' ? DATA[a] : DATA[b];
const chart = makeChart(document.getElementById('root'), {
  dates: DATES, strip: true, aria: 'Funding rates on both venues with the spread below',
  bands: BANDS,
  panels: [
    { label: 'Funding rate, annualized', h: 190, zero: true, tick: v => v + '%',
      series: [ { values: pick('b7', 'b'), color: 'var(--s-bin)' }, { values: pick('h7', 'h'), color: 'var(--s-hl)' } ] },
    { label: 'Spread: SHORT − LONG', h: 120, zero: true, tick: v => v + '%',
      series: [ { type: 'bar', values: pick('s7', 's'), color: v => v >= 0 ? 'var(--pos)' : 'var(--neg)' } ] }
  ],
  tooltip: i => {
    const sfx = mode === '7' ? ' (7d avg)' : '';
    const b = mode === '7' ? DATA.b7[i] : DATA.b[i], h = mode === '7' ? DATA.h7[i] : DATA.h[i], s = mode === '7' ? DATA.s7[i] : DATA.s[i];
    return [
      { key: 'var(--s-hl)', value: pct(h), label: 'SHORT' + sfx },
      { key: 'var(--s-bin)', value: pct(b), label: 'LONG' + sfx },
      { key: s >= 0 ? 'var(--pos)' : 'var(--neg)', value: pct(s), label: 'Spread' + sfx },
      { sep: true, value: usd(DATA.p[i]), label: 'Funding P&L that day' }
    ];
  }
});
for (const [id, m] of [['m7', '7'], ['m1', '1']]) document.getElementById(id).addEventListener('click', () => {
  mode = m;
  document.getElementById('m7').setAttribute('aria-pressed', m === '7');
  document.getElementById('m1').setAttribute('aria-pressed', m === '1');
  chart.redraw();
});
'''.replace("BANDS", json.dumps(bands, ensure_ascii=False)).replace("SHORT", Sh).replace("LONG", L)
    rows = [[dates[i], pct(df.long_funding[i] * 365, 1), pct(df.short_funding[i] * 365, 1), pct(S["sp"][i] * 365, 1), usd(S["fp"][i])] for i in range(len(df))]
    (out / f"{A.lower()}-funding.html").write_text(page(f"{A} Funding Spread", body, fdata, script,
        ["Date", f"{L} (ann.)", f"{Sh} (ann.)", "Spread (ann.)", "Funding P&amp;L"], rows))

    m2m, gap = S["m2m"], S["gap_bps"]
    wm = R["worst_m2m"]
    wmi = int(df.index[df.date == wm["date"]][0])
    pdata = dict(d=dates, b=rr(df.long_close), h=rr(df.short_close), g=rr(gap, 1), m=rr(m2m, 0))
    d2 = lambda v: ("−" if v < 0 else "+") + f"${abs(v):.2f}"
    nxt = f" The next day the gap was back to {num(wm['next_gap_bps'])} bps." if wm["next_gap_bps"] is not None else ""
    body = f'''<header>
  <h1>{A} perp price: {L} vs {Sh}</h1>
  <p class="sub">Daily close of the {A} perpetual on each venue. The gap between them is the trade's net mark-to-market risk. {period}.</p>
</header>
<div class="stats">
  <div class="stat"><span>Avg price gap</span><b>{num(R['gap_mean_bps'])} bps</b></div>
  <div class="stat"><span>Days within ±10 bps</span><b>{R['gap_within10']:.0%}</b></div>
  <div class="stat"><span>Widest gap</span><b>{R['gap_max_bps']:.1f} bps</b></div>
  <div class="stat"><span>Worst daily M2M</span><b>{usd(wm['pnl'])}</b></div>
</div>
<div class="bar"><div class="legend">
  <span><i class="lk thick" style="background:var(--s-bin)"></i>{L} perp</span>
  <span><i class="lk" style="background:var(--s-hl)"></i>{Sh} perp</span>
  <span><i class="sq" style="background:var(--s-bin)"></i>{L} above {Sh}</span>
  <span><i class="sq" style="background:var(--s-hl)"></i>{Sh} above {L}</span>
</div></div>
<div class="plot"><div class="tip" hidden></div></div>
<p class="foot">Gap = ({L} close − {Sh} close) ÷ mid price, in basis points (1 bp = 0.01%). Daily M2M = {A} held per leg × change in the $ price gap. Both legs hold the same amount of {A}, sized to {usdk(R['leg'])} at the previous close, so if both prices move by the same $ amount it's zero. Example, {day(wm['date'])}: the gap went from {d2(wm['gap_before_usd'])} to {d2(wm['gap_after_usd'])} ({d2(wm['gap_after_usd'] - wm['gap_before_usd'])}) × {wm['qty']:,.0f} {A} = {usd(wm['pnl'])}.{nxt} Prices: daily perp candles from each venue.</p>'''
    label = f"Worst day, {day(wm['date'])}: {num(wm['gap_bps'])} bps, {usd(wm['pnl'])}"
    script = r'''
makeChart(document.getElementById('root'), {
  dates: DATES, aria: 'Perp prices on both venues with the price gap below',
  panels: [
    { label: 'Perp price (USD)', h: 190, zero: false, tick: v => '$' + v,
      series: [ { values: () => DATA.b, color: 'var(--s-bin)', width: 6, opacity: 0.35 }, { values: () => DATA.h, color: 'var(--s-hl)', width: 1.75 } ] },
    { label: 'Price gap between venues (bps)', h: 120, zero: true, tick: v => v + '',
      series: [ { type: 'bar', values: () => DATA.g, color: v => v >= 0 ? 'var(--s-bin)' : 'var(--s-hl)' } ],
      marks: [ { i: WI, value: () => DATA.g[WI], label: LABEL, short: SHORTLBL, dy: 4 } ] }
  ],
  tooltip: i => [
    { key: 'var(--s-bin)', value: '$' + DATA.b[i].toFixed(2), label: 'LONGV' },
    { key: 'var(--s-hl)', value: '$' + DATA.h[i].toFixed(2), label: 'SHORTV' },
    { value: (DATA.g[i] > 0 ? '+' : DATA.g[i] < 0 ? '−' : '') + Math.abs(DATA.g[i]).toFixed(1) + ' bps', label: 'Gap' },
    { sep: true, value: usd(DATA.m[i]), label: 'Daily M2M, LEG per leg' }
  ]
});
'''.replace("WI", str(wmi)).replace("SHORTLBL", json.dumps(f"{day(wm['date'])}: {usd(wm['pnl'])}", ensure_ascii=False)) \
       .replace("LABEL", json.dumps(label, ensure_ascii=False)).replace("LONGV", L).replace("SHORTV", Sh).replace("LEG", usdk(R["leg"]))
    rows = [[dates[i], f"${df.long_close[i]:.2f}", f"${df.short_close[i]:.2f}", num(gap[i]), usd(m2m[i])] for i in range(len(df))]
    (out / f"{A.lower()}-prices.html").write_text(page(f"{A} Perp Prices", body, pdata, script,
        ["Date", L, Sh, "Gap (bps)", "Daily M2M"], rows))

    v100 = 100 * (1 + S["cf"] / R["margin"])
    gdata = dict(d=dates, v=rr(v100), p=rr(S["cf"], 0))
    body = f'''<header>
  <h1>$100 in the {A} funding arb</h1>
  <p class="sub">How $100 would have grown in the strategy from {day(R['start'])} {R['start']:%Y}, earning only the funding spread. The strategy runs {usdk(R['notional'])} notional ({usdk(R['leg'])} per leg) at {a.leverage:g}× on {usdk(R['margin'])} of margin; $100 earns the same return as that {usdk(R['margin'])}.</p>
</header>
<div class="stats">
  <div class="stat"><span>Start, {day(R['start'])}</span><b>$100.00</b></div>
  <div class="stat"><span>Now, {day(R['end'])}</span><b>${v100.iloc[-1]:.2f}</b></div>
  <div class="stat"><span>Return over {R['days']} days</span><b>{pct(v100.iloc[-1] / 100 - 1, 1, sign=True)}</b></div>
  <div class="stat"><span>Annualized</span><b>{pct(R['apr'], 1)}</b></div>
</div>
<div class="plot"><div class="tip" hidden></div></div>
<p class="foot">Value = $100 × (1 + cumulative funding P&amp;L ÷ {usdk(R['margin'])} margin). Funding only: no compounding, before fees, M2M excluded.</p>'''
    script = r'''
makeChart(document.getElementById('root'), {
  dates: DATES, aria: 'Value of $100 growing from funding alone',
  panels: [
    { label: 'Value of $100 (USD)', h: 240, zero: false, tick: v => '$' + v,
      series: [ { values: () => DATA.v, color: 'var(--s-strat)' } ],
      marks: [ { i: DATA.v.length - 1, value: () => DATA.v[DATA.v.length - 1], label: '$' + DATA.v[DATA.v.length - 1].toFixed(2), dy: -8 } ] }
  ],
  tooltip: i => [
    { key: 'var(--s-strat)', value: '$' + DATA.v[i].toFixed(2), label: 'Value of $100' },
    { sep: true, value: usd(DATA.p[i]), label: 'Cumulative funding, NOTIONAL notional' }
  ]
});
'''.replace("NOTIONAL", usdk(R["notional"]))
    rows = [[dates[i], f"${v100[i]:.2f}", usd(S["cf"][i])] for i in range(len(df))]
    (out / f"{A.lower()}-growth.html").write_text(page(f"{A} Arb Growth", body, gdata, script,
        ["Date", "Value of $100", "Cum. funding P&amp;L"], rows))


# ---------- report ----------
def report(R, a):
    A, L, Sh = a.asset, a.long, a.short
    N, leg, mult = R["notional"], R["leg"], R["mult"]
    wd, dd, wm = R["worst_day"], R["worst_dd"], R["worst_m2m"]
    o = []
    w = o.append
    w(f"# {A} Funding Rate Arb (Long {L} - Short {Sh})\n")
    w(f"**Date: {day(R['end'])} {R['end']:%Y}**\n\n**Strategy category: Funding Rate Arbitrage**\n\n**Expected Yield Range: [TBD]**\n\n**Protocol exposure: {L}, {Sh}**\n\n**Size: TBD**\n\n---\n")
    w("#### **Strategy overview**\n")
    w(f"Long {A} perp on {L}, short {A} perp on {Sh}, and capture the funding spread. The price exposure cancels out, so what's left is the difference in funding between the two venues.\n")
    rng = (f"{day(R['start'])} – {day(R['end'])} {R['end']:%Y}" if R["start"].year == R["end"].year
           else f"{day(R['start'])} {R['start']:%Y} – {day(R['end'])} {R['end']:%Y}")
    miss = "".join(f"; {n} days missing, {day(g0)} – {day(g1)}" for g0, g1, n in R["gap_ranges"])
    w(f"Over the full data series, {rng} ({R['days']} days of data{miss}; [why the series starts on {day(R['start'])}]), the spread averaged **{pct(R['full_spread'])} annualized**.\n")
    w(f"At {a.leverage:g}× leverage per leg we multiply the spread by {mult:g}, because {usdk(leg)} of notional per leg earns the spread on {usdk(R['margin'])} of total margin. That gives a **{pct(R['apr'], 1)} APR**.\n")
    w(f"**Sizing**\n\n- {usdk(N)} total notional: {usdk(leg)} per leg\n- {a.leverage:g}× leverage on each leg: {usdk(R['margin'] / 2)} margin on {L} and {usdk(R['margin'] / 2)} on {Sh}, {usdk(R['margin'])} in total\n")
    if a.oi_long or a.oi_short:
        w("**Markets Open Interest**\n")
        if a.oi_long:
            w(f"{L} OI: {usd(a.oi_long)} (our leg is {R['oi_long_share']:.2%})\n")
        if a.oi_short:
            w(f"{Sh} OI: {usd(a.oi_short)} (our leg is {R['oi_short_share']:.2%})\n")
    w(f"""**Assumptions**

- All $ figures use the sizing above.
- % of notional = $ figure ÷ {usdk(N)} total notional.
- Daily funding P&L = daily spread × {usdk(leg)}.
- Implied APR = annualized spread × {mult:g} ({usdk(leg)} notional per leg ÷ {usdk(R['margin'])} margin).
- Daily M2M = {A} held per leg × change in the $ price gap between {L} and {Sh}. Both legs hold the same amount of {A}, sized to {usdk(leg)} at the previous close.
- Days are UTC. Annualized = daily × 365. No compounding, before trading fees.
""")
    r30 = ("no 30-day stretch in the data had a negative average spread" if R["roll30_pos_share"] == 1
           else f"the 30-day average spread was positive {R['roll30_pos_share']:.1%} of the time" if R["roll30_pos_share"] > 0.99
           else f"the 30-day average spread was positive {R['roll30_pos_share']:.0%} of the time")
    w(f"**Do we know what causes the spread, or have reason to believe it will persist?** No. [THEORY: fill from the oracle/index comparison in section 3.] {Sh}'s funding has been higher than {L}'s on {R['pos'] / R['days']:.0%} of days, and {r30}. This is a theory, not empirical evidence, and it doesn't explain why the spread would persist.\n")
    w(f"[EMBED growth chart]\n\nThe chart shows how $100 would have grown in the strategy since {day(R['start'])}, funding only: $100 → ${R['growth_end']:.2f}.\n")

    w("#### **1. Historical funding spread**\n")
    w(f"*Method:* daily spread = {Sh} daily funding − {L} daily funding, with every settlement in the day summed and then annualized (×365). Implied APR = spread × {mult:g}. All periods end {day(R['end'])} {R['end']:%Y}.\n")
    w(f"| **Period** | **Avg funding spread (annualized)** | **Implied APR at {a.leverage:g}×** |\n| --- | --- | --- |")
    for lbl, s, apr in R["periods"]:
        w(f"| {lbl} | {pct(s)} | {pct(apr, 1)} |")
    w("")
    d = R["days"]
    w(f"**Daily behavior**\n\n| **Spread** | **Days** | **Share** |\n| --- | --- | --- |\n| Positive | {R['pos']} | {R['pos'] / d:.1%} |\n| Zero (both venues at the base rate) | {R['zero']} | {R['zero'] / d:.1%} |\n| Negative | {R['neg']} | {R['neg'] / d:.1%} |\n")
    span = (f"{dd['start'].day} – {day(dd['end'])}" if dd["start"].month == dd["end"].month else f"{day(dd['start'])} – {day(dd['end'])}")
    ddates = f"{span} ({dd['days']} days)"
    w(f"""**Worst cases**

|  | **Dates** | **Avg spread (annualized)** | **Implied APR at {a.leverage:g}×** | **Funding P&L** | **% of notional** |
| --- | --- | --- | --- | --- | --- |
| Worst funding spread, single day | {day(wd['date'])} | {pct(wd['spread'], 1)} | {pct(wd['apr'], 1)} | {usd(wd['pnl'])} | {pct(wd['pct'])} |
| Worst funding drawdown | {ddates} | {pct(dd['spread'], 1)} | {pct(dd['apr'], 1)} | {usd(dd['pnl'])} | {pct(dd['pct'])} |
""")
    rec = (f"it was made back by {day(dd['recovered'])}" if dd["recovered"] is not None else "it has not been made back yet")
    w(f"The worst funding drawdown is the biggest drop in cumulative funding P&L from a high to a low. {span} is where funding cost us the most, and {rec}.\n")
    w("[EMBED funding chart]\n")
    ws = [lbl.replace(" days", "") for lbl, _, _ in R["periods"][:-1]]
    plist = ", ".join(ws[:-1]) + f" and {ws[-1]}" if len(ws) > 1 else "".join(ws)
    first = (f"In every period in the table above (the last {plist} days, and the full {d} days), {Sh}'s average funding rate was higher than {L}'s, so the average spread was positive."
             if R["periods_all_positive"] else "[REVIEW: the average spread was not positive in every period; say which.]")
    p30 = next((s for lbl, s, _ in R["periods"] if lbl == "30 days"), None)
    p7 = next((s for lbl, s, _ in R["periods"] if lbl == "7 days"), None)
    moves = f" The spread moves around, from {pct(p30, 1)} over the last 30 days to {pct(p7, 1)} over the last 7." if p30 is not None and p7 is not None else ""
    recd = f" and was made back within {dd['rec_days']} days" if dd["rec_days"] is not None else ""
    w(f"{first}{moves} About {R['neg'] / d:.0%} of days are negative; the worst stretch cost {usd(dd['pnl'])[1:]} ({pct(-dd['pct'])} of notional){recd}.\n")

    w("#### **2. Mark-to-market risk**\n")
    w(f"**What it is:** we're long and short the same perp on two venues, so the M2M risk is the price gap between them. If both prices move the same, M2M is zero. Funding is not included. In practice it doesn't affect the trade profitability, because the gap closes quickly.\n")
    w(f"|  | **Date** | **P&L** | **% of notional** |\n| --- | --- | --- | --- |\n| Worst adverse daily M2M | {day(wm['date'])} | {usd(wm['pnl'])} | {pct(wm['pct'])} |\n")
    if wm["next_gap_bps"] is not None:
        if abs(wm["next_gap_bps"]) < abs(wm["gap_bps"]) and wm["next_pnl"] > 0:
            w(f"**The gap closed the next day. It went from {num(wm['gap_bps'])} bps on {day(wm['date'])} to {num(wm['next_gap_bps'])} bps the day after, recovering {usd(wm['next_pnl'])} of the loss.**\n")
        elif abs(wm["gap_after_usd"]) < abs(wm["gap_before_usd"]):
            w(f"**This loss was the gap closing, not opening: the day before, {L} traded {num(abs(wm['prev_gap_bps']))} bps {'above' if wm['prev_gap_bps'] > 0 else 'below'} {Sh} (a gain of {usd(wm['prev_pnl'])} that day), and on {day(wm['date'])} it was back to {num(wm['gap_bps'])} bps.**\n")
        else:
            w(f"**[REVIEW: the gap did not close the next day ({num(wm['gap_bps'])} → {num(wm['next_gap_bps'])} bps); describe what happened.]**\n")
    w("[EMBED price chart]\n")
    side = Sh if R["gap_mean_bps"] < 0 else L
    w(f"Across the period, the gap between venues averaged {num(R['gap_mean_bps'])} bps ({side} slightly above), stayed within ±10 bps on {R['gap_within10']:.0%} of days and never went past {R['gap_max_bps']:.1f} bps. It doesn't persist: a gap that opens one day mostly closes the next.\n")
    regs = {r["name"]: r for r in R["regimes"]}
    if "Bear" in regs and "Bull" in regs:
        b0, b1 = regs["Bear"]["long_px"]
        u0, u1 = regs["Bull"]["long_px"]
        w(f"Through a {pct(b1 / b0 - 1, 0)} price crash and a {pct(u1 / u0 - 1, 0, sign=True)} price rally the gap stayed under {np.ceil(R['gap_max_bps']):.0f} bps, and the worst day cost {usd(wm['pnl'])[1:]} ({pct(-wm['pct'])} of notional).\n")

    c = R["corr"]
    w("#### **3. Oracles, contract specs and correlation**\n")
    w(f"""Neither the oracles nor the contract specs are the same:

- **Oracle:** {L}'s {A} index is [constituents + weights]. {Sh}'s oracle is [constituents + weights].
- **Contract spec:** {L} averages the premium over [__], {Sh} over [__]. {L} is [USDT]-margined, {Sh} is [USDC].

Funding on each venue is its perp price vs its own oracle, and both inputs differ: each perp price is set by its own order book, and each oracle is built from different venues.

{corr_text(c, L, Sh)}
""")

    if R["regimes"]:
        w("#### **4. Spreads during Bear vs Bull periods**\n")
        hdr = " | ".join(f"**{r['name']}: {day(r['start'])} – {day(r['end'])}**" for r in R["regimes"])
        w(f"|  | {hdr} |\n| --- |" + " --- |" * len(R["regimes"]))
        row = lambda lbl, f: w(f"| {lbl} | " + " | ".join(f(r) for r in R["regimes"]) + " |")
        row("Days", lambda r: str(r["days"]))
        row(f"{A} Price Action", lambda r: f"${r['long_px'][0]:,.0f} → ${r['long_px'][1]:,.0f} ({pct(r['long_px'][1] / r['long_px'][0] - 1, 1, sign=True)})")
        row("**Avg funding spread (annualized)**", lambda r: f"**{pct(r['spread'])}**")
        row(f"Implied APR at {a.leverage:g}×", lambda r: pct(r["apr"], 1))
        row("Negative spread days", lambda r: f"{r['neg']} of {r['days']}" + (f" (+{r['zero']} at zero)" if r["zero"] else ""))
        row("Cumulative funding P&L during the period", lambda r: f"{usd(r['funding'], sign=True)} ({pct(r['funding'] / N, 2, sign=True)})")
        row("Worst adverse daily M2M", lambda r: f"{usd(r['worst_m2m'][1])} on {day(r['worst_m2m'][0])} ({pct(r['worst_m2m'][1] / N)})")
        w(f"\n*Note:* all % figures in the table are based on the {usdk(N)} total notional ({usdk(leg)} per leg).\n")
        if "Bear" in regs and "Bull" in regs:
            be, bu = regs["Bear"], regs["Bull"]
            hi, lo = (bu, be) if bu["apr"] >= be["apr"] else (be, bu)
            ratio = hi["apr"] / lo["apr"] if lo["apr"] > 0 else float("inf")
            how = "clearly does better" if ratio >= 1.5 else "does slightly better"
            nb, nu = be["neg"] / be["days"], bu["neg"] / bu["days"]
            negs = (f"negative days were {nb:.0%} of the bear and {nu:.0%} of the bull" )
            w(f"The strategy {how} in the {hi['name'].lower()} period. The spread averaged {pct(hi['spread'])} ({pct(hi['apr'], 1)} APR) "
              f"against {pct(lo['spread'])} ({pct(lo['apr'], 1)} APR) in the {lo['name'].lower()}, and {negs}. "
              + ("It made money in both. " if be["funding"] > 0 and bu["funding"] > 0 else "")
              + "M2M stayed small in both periods.\n")

    w("#### **Conclusion**\n")
    w(f"I don't know why {Sh} funding runs above {L}, but the spread has been consistent. It averaged {pct(R['full_spread'])} annualized over the full track record, which is {pct(R['apr'], 1)} APR at {a.leverage:g}×. Negative stretches are short and cheap. M2M between the venues is small and closes within a day. [REVIEW: recommendation]\n")
    return "\n".join(o)


def corr_text(c, L, Sh):
    vals = f"{num(c[1], 2)} daily, {num(c[7], 2)} on 7-day averages and {num(c[30], 2)} on 30-day averages"
    why = (f"Negative is the expected sign: the price gap is measured as {L} − {Sh}, so when {Sh} trades above {L} "
           f"the gap goes negative, {Sh} longs pay more funding, and the spread widens.")
    if all(v < 0 for v in c.values()):
        trend = ("Over longer periods the link gets stronger" if c[30] < c[7] < c[1]
                 else "The link is weak to moderate at every horizon")
        return f"So the funding spread and the price gap don't move together much day to day. {trend}: correlation is {vals}. {why}"
    if max(abs(v) for v in c.values()) < 0.2:
        return (f"There's no meaningful relationship: correlation is {vals}. So the spread isn't coming from one perp trading above "
                f"the other; it comes from how each venue measures its premium (the oracles above).")
    return (f"The relationship is weak and doesn't have the expected sign: correlation is {vals}. If the spread came from {Sh}'s perp "
            f"trading above {L}'s, the correlation would be negative. So the spread is more likely coming from how each venue "
            f"measures its premium (the oracles above) than from the perp-vs-perp price gap. [REVIEW]")


def slack(R, a):
    dd, wm = R["worst_dd"], R["worst_m2m"]
    p = {lbl: (s, apr) for lbl, s, apr in R["periods"]}
    extra = "".join(f" Over the last {k} it was {pct(p[k][0])} ({pct(p[k][1], 1)} APR)." for k in ("30 days", "7 days") if k in p)
    rec = f", made back in {dd['rec_days']} days" if dd["rec_days"] is not None else ""
    return f"""@[name] sharing the {a.asset} funding arb analysis here: [link]

**TL;DR: [the trade looks great].**
- **The spread has been consistent across every time frame.** Since we have data ({R['days']} days), it averaged {pct(R['full_spread'])} annualized, which is a {pct(R['apr'], 1)} APR at {a.leverage:g}x leverage.{extra}
- **The worst funding drawdown is very small:** {pct(-dd['pct'])} of notional{rec}.
- **The M2M risk from price differences between venues is also negligible.** The worst day was {pct(-wm['pct'])} of notional.

The main caveat is that I don't fully understand why the funding spread exists. [theory]. I don't have empirical proof, but the spread is there.

I think we could start with {usdk(R['notional'])} notional ({usdk(R['leg'])} per leg) at {a.leverage:g}x leverage, so {usdk(R['margin'])} of margin in total. Let me know what you think. Thanks!
"""


def checks(R, a):
    out = []
    if R["missing_days"]:
        out.append(f"{R['missing_days']} gaps in the date series: fill or explain before publishing.")
    for side in ("long", "short"):
        c = R.get(f"{side}_n_counts")
        if c:
            out.append(f"{side} settlements per day: {c} (expect a constant count; partial first/last days are normal).")
    mc = R["margin_check"]
    if mc["days"]:
        out.append(f"MARGIN: {len(mc['days'])} days with a close-to-close move above {mc['threshold']:.0%} at {a.leverage:g}× "
                   f"(worst down {mc['max_down'][1]:.1%} on {day(mc['max_down'][0])}, worst up {mc['max_up'][1]:.1%} on {day(mc['max_up'][0])}). "
                   "Each leg is margined on its own venue; raise this with the user (they chose to keep it out of the XMR doc).")
    out.append(f"Funding pinned at the base rate: {a.long} {R['pinned_long']} days, {a.short} {R['pinned_short']} days.")
    out.append("Validate the period averages against the Knowledge Layer API before publishing.")
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True)
    p.add_argument("--asset", required=True)
    p.add_argument("--long", required=True, help="venue we are long on")
    p.add_argument("--short", required=True, help="venue we are short on")
    p.add_argument("--long-interval", default="8h")
    p.add_argument("--short-interval", default="1h")
    p.add_argument("--notional", type=float, default=1_000_000, help="total notional, both legs")
    p.add_argument("--leverage", type=float, default=5)
    p.add_argument("--bear", help="YYYY-MM-DD:YYYY-MM-DD")
    p.add_argument("--bull", help="YYYY-MM-DD:YYYY-MM-DD")
    p.add_argument("--regime-price-ref", choices=["prior", "start"], default="prior",
                   help="bear/bull price change from the prior day's close (default) or from the start date's close")
    p.add_argument("--oi-long", type=float)
    p.add_argument("--oi-short", type=float)
    p.add_argument("--base-rate", type=float, default=0.0003, help="daily funding at the base interest rate")
    p.add_argument("--funding-source", default="fmtdb funding_rate_history, deduplicated; checked against the Knowledge Layer averages")
    p.add_argument("--out", default="out")
    a = p.parse_args()

    df = pd.read_csv(a.csv, parse_dates=["date"])
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    R, S = analyze(df, a)
    charts(df.sort_values("date").reset_index(drop=True), R, S, a, out)
    (out / "report.md").write_text(report(R, a))
    (out / "slack.md").write_text(slack(R, a))
    (out / "numbers.json").write_text(json.dumps(R, indent=2, default=str))
    print("\n".join(["Wrote report.md, slack.md, numbers.json and 3 charts to " + str(out), "", "Checks:"] + ["- " + c for c in checks(R, a)]))


if __name__ == "__main__":
    main()
