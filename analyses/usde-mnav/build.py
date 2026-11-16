"""USDE mNAV trade: daily mNAV history, funding, scenarios and charts.

Inputs (data/): usde_daily.json (Yahoo daily chart), ena_1h.json (Hyperliquid ENA 1h candles),
hl_funding.json (Hyperliquid ENA hourly funding). Outputs: usde_mnav_daily.csv, numbers.json, charts/*.html.

mNAV = market cap / market value of ENA held
     = (USDE price x Class A shares) / (ENA held x ENA price)
"""
import csv, json, math, statistics as st, datetime as dt
from pathlib import Path

HERE = Path(__file__).parent
SKILL = HERE.parent.parent / ".claude/skills/funding-arb-analysis"
DATA, OUT = HERE / "data", HERE / "charts"

# --- company facts (Q3 2026 results, 8-K filed 16 Nov 2026) ---
SHARES = 24_029_576          # Class A shares outstanding (only class with economics)
ENA_HELD = 3.029e9           # ~$802M / $0.2648 (30 Sep) and ~$576M / $0.1901 (30 Oct)
CASH = 10_352_692
OTHER_ASSETS = 12_771_432 - 10_352_692 + 689_375   # other current assets + intangibles
CUR_LIAB = 1_983_077
WAIVER_SIGNED, WAIVER_EFFECTIVE = "2026-09-14", "2026-10-05"

# --- trade sizing used in the report ---
LONG = 500_000
SHORT = 500_000
HL_LEV = 2


def load():
    y = json.load(open(DATA / "usde_daily.json"))["chart"]["result"][0]
    q = y["indicators"]["quote"][0]
    ena = {c["t"] // 1000: float(c["c"]) for c in json.load(open(DATA / "ena_1h.json"))}
    last_t = max(ena)
    rows = []
    for t, c, v in zip(y["timestamp"], q["close"], q["volume"]):
        if c is None:
            continue
        d = dt.datetime.fromtimestamp(t, dt.UTC).date()
        # ENA at the Nasdaq close: 16:00 New York = 20:00 UTC (EDT) / 21:00 UTC (EST, from 1 Nov).
        # The 1h candle that opens one hour earlier closes exactly at the bell.
        close_utc = 20 if d < dt.date(2026, 11, 1) else 21
        k = int(dt.datetime(d.year, d.month, d.day, close_utc - 1, tzinfo=dt.UTC).timestamp())
        intraday = k not in ena
        e = ena[last_t] if intraday else ena[k]
        rows.append(dict(date=str(d), usde=round(c, 4), volume=v or 0, ena=e, intraday=intraday))
    fund = {}
    for f in json.load(open(DATA / "hl_funding.json")):
        d = str(dt.datetime.fromtimestamp(f["time"] / 1000, dt.UTC).date())
        fund.setdefault(d, []).append(float(f["fundingRate"]))
    for r in rows:
        r["ena_per_share"] = ENA_HELD / SHARES
        r["nav_ps"] = ENA_HELD * r["ena"] / SHARES
        r["mcap"] = r["usde"] * SHARES
        r["ena_value"] = ENA_HELD * r["ena"]
        r["mnav"] = r["mcap"] / r["ena_value"]
    return rows, fund, y["meta"], last_t


def main():
    rows, fund, meta, last_t = load()
    ms = [r["mnav"] for r in rows]
    cur = rows[-1]
    i_min, i_max = ms.index(min(ms)), ms.index(max(ms))
    avg = st.mean(ms)
    m0 = cur["mnav"]

    # funding (calendar days since listing, full UTC days only for averages)
    fdays = sorted(d for d in fund if d >= rows[0]["date"])
    full = [d for d in fdays if len(fund[d]) == 24]
    hourly = [x for d in full for x in fund[d]]
    ann = lambda xs: sum(xs) / len(xs) * 24 * 365
    f_all, f_30 = ann(hourly), ann([x for d in full[-30:] for x in fund[d]])
    f_pos_hours = sum(1 for x in hourly if x > 0) / len(hourly)
    f_neg_days = sum(1 for d in full if sum(fund[d]) < 0)
    monthly = {}
    for d in full:
        monthly.setdefault(d[:7], []).extend(fund[d])

    # balance sheet at market, today
    ena_val = cur["ena_value"]
    nav = ena_val + CASH + OTHER_ASSETS - CUR_LIAB
    adv20_sh = st.mean(r["volume"] for r in rows[-21:-1])

    scen = [("Historical max", ms[i_max], rows[i_max]["date"]),
            ("Historical average", avg, None),
            ("Today (entry)", m0, cur["date"]),
            ("Historical min", ms[i_min], rows[i_min]["date"]),
            ("Half the historical min", ms[i_min] / 2, None),
            ("Zero", 0.0, None)]
    scen_out = [dict(name=n, mnav=m, date=d, ret=m / m0 - 1, pnl=LONG * (m / m0 - 1)) for n, m, d in scen]

    # waiver dates in the series
    idx = {r["date"]: i for i, r in enumerate(rows)}
    i_eff = idx[WAIVER_EFFECTIVE]
    i_sig = idx.get(WAIVER_SIGNED) or idx["2026-09-15"]

    N = dict(
        asof=cur["date"], intraday=cur["intraday"], ena_time_utc=dt.datetime.fromtimestamp(last_t + 3600, dt.UTC).strftime("%Y-%m-%d %H:%M"),
        usde=cur["usde"], ena=cur["ena"], shares=SHARES, ena_held=ENA_HELD, ena_per_share=ENA_HELD / SHARES,
        mcap=cur["mcap"], ena_value=ena_val, cash=CASH, other_assets=OTHER_ASSETS, cur_liab=CUR_LIAB,
        nav=nav, nav_ps=nav / SHARES, ena_ps=cur["nav_ps"], mnav=m0, p_nav=cur["usde"] / (nav / SHARES),
        days=len(rows), start=rows[0]["date"], mnav_start=ms[0],
        min=ms[i_min], min_date=rows[i_min]["date"], max=ms[i_max], max_date=rows[i_max]["date"], avg=avg,
        median=st.median(ms), mnav_waiver_eff=ms[i_eff], usde_waiver_eff=rows[i_eff]["usde"],
        mnav_waiver_signed=ms[i_sig], waiver_signed_row=rows[i_sig]["date"],
        funding_ann_since_listing=f_all, funding_ann_30d=f_30, funding_pos_hours=f_pos_hours,
        funding_neg_days=f_neg_days, funding_full_days=len(full),
        funding_monthly={k: ann(v) for k, v in sorted(monthly.items())},
        adv20_shares=adv20_sh, adv20_usd_at_today=adv20_sh * cur["usde"],
        long=LONG, short=SHORT, hl_lev=HL_LEV, scenarios=scen_out,
    )
    (HERE / "numbers.json").write_text(json.dumps(N, indent=2))

    with open(HERE / "usde_mnav_daily.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "usde_close", "usde_volume", "ena_price_at_nasdaq_close", "ena_per_share",
                    "ena_value_per_share", "market_cap", "ena_value", "mnav", "hl_ena_funding_day", "note"])
        for r in rows:
            fd = sum(fund[r["date"]]) if r["date"] in fund else ""
            w.writerow([r["date"], r["usde"], r["volume"], round(r["ena"], 6), round(r["ena_per_share"], 2),
                        round(r["nav_ps"], 4), round(r["mcap"]), round(r["ena_value"]), round(r["mnav"], 4),
                        fd if fd == "" else round(fd, 8), "intraday" if r["intraday"] else ""])
    charts(rows, fund, fdays, N, i_min, i_max, i_eff, i_sig)
    print(json.dumps({k: v for k, v in N.items() if k not in ("funding_monthly",)}, indent=1, default=str))


# ---------------- charts ----------------
def page(title, body, data, script, cols, rows):
    eng = (SKILL / "engine.js").read_text()
    css = (SKILL / "charts.css").read_text()
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


def dlabel(s):
    d = dt.date.fromisoformat(s)
    return f"{d.day} {d:%b}"


def money(v, sign=True):
    s = "−" if v < 0 else ("+" if sign and v > 0 else "")
    return f"{s}${abs(v):,.0f}"


def charts(rows, fund, fdays, N, i_min, i_max, i_eff, i_sig):
    OUT.mkdir(exist_ok=True)
    dates = [r["date"] for r in rows]
    asof = dlabel(N["asof"]) + (" (intraday)" if N["intraday"] else "")
    last = len(rows) - 1

    # 1. mNAV history
    data = dict(d=dates, m=[round(r["mnav"], 4) for r in rows], a=[round(N["avg"], 4)] * len(rows))
    bands = [dict(i0=i_sig, i1=i_sig, label="Waiver signed (14 Sep)", short="Signed", row=0),
             dict(i0=i_eff, i1=i_eff, label="Lock-ups off (5 Oct)", short="Unlocked", row=1)]
    body = f'''<header>
  <h1>USDE mNAV since listing</h1>
  <p class="sub">What the market pays for each $1 of ENA that StablecoinX holds. mNAV = market cap ÷ value of the ENA held. 1.0x would mean the stock trades at the value of its tokens. {dlabel(N['start'])} – {asof} 2026.</p>
</header>
<div class="stats">
  <div class="stat"><span>Today</span><b>{N['mnav']:.2f}x</b></div>
  <div class="stat"><span>Average</span><b>{N['avg']:.2f}x</b></div>
  <div class="stat"><span>Max, {dlabel(N['max_date'])}</span><b>{N['max']:.2f}x</b></div>
  <div class="stat"><span>Min, {dlabel(N['min_date'])}</span><b>{N['min']:.2f}x</b></div>
</div>
<div class="bar"><div class="legend">
  <span><i class="lk" style="background:var(--s-strat)"></i>mNAV, daily close</span>
  <span><i class="lk" style="background:var(--ink-2);opacity:.5"></i>Average since listing</span>
  <span><i class="lk" style="background:var(--ink-2);opacity:.55"></i>Waiver dates</span>
</div></div>
<div class="plot"><div class="tip" hidden></div></div>
<p class="foot">mNAV = (USDE close × {N['shares']:,} Class A shares) ÷ ({N['ena_held']/1e9:.3f}B ENA × ENA price at the Nasdaq close). ENA held and share count from the Q3 2026 results (8-K, 16 Nov 2026); both were the same at the end of Q2. ENA price: Hyperliquid ENA perp, hourly candle closing at 4pm New York. USDE: Nasdaq daily close (Yahoo Finance). The last point is intraday. The waiver was signed on 14 Sep (a Monday) and the 8-K was filed on 17 Sep.</p>'''
    script = r'''
makeChart(document.getElementById('root'), {
  dates: DATES, strip: true, aria: 'USDE mNAV since listing, with the waiver dates marked',
  bands: BANDS,
  panels: [
    { label: 'mNAV (market cap ÷ ENA value)', h: 250, zero: true, tick: v => v.toFixed(1) + 'x',
      series: [ { values: () => DATA.a, color: 'var(--ink-2)', width: 1.25, opacity: 0.5 },
                { values: () => DATA.m, color: 'var(--s-strat)' } ],
      marks: [ { i: IMAX, value: () => DATA.m[IMAX], label: 'Max ' + DATA.m[IMAX].toFixed(2) + 'x', dy: -8 },
               { i: IMIN, value: () => DATA.m[IMIN], label: 'Min ' + DATA.m[IMIN].toFixed(2) + 'x', dy: 16 },
               { i: LAST, value: () => DATA.m[LAST], label: 'Today ' + DATA.m[LAST].toFixed(2) + 'x', dy: 16 } ] }
  ],
  tooltip: i => [
    { key: 'var(--s-strat)', value: DATA.m[i].toFixed(2) + 'x', label: 'mNAV' },
    { key: 'var(--ink-2)', value: DATA.a[i].toFixed(2) + 'x', label: 'Average since listing' }
  ]
});
'''.replace("BANDS", json.dumps(bands)).replace("IMAX", str(i_max)).replace("IMIN", str(i_min)).replace("LAST", str(last))
    tab = [[r["date"], f"${r['usde']:.2f}", f"${r['ena']:.4f}", f"${r['nav_ps']:.2f}", f"{r['mnav']:.3f}x"] for r in rows]
    (OUT / "usde-mnav.html").write_text(page("USDE mNAV History", body, data, script,
        ["Date", "USDE close", "ENA price", "ENA per share ($)", "mNAV"], tab))

    # 2. Share price vs ENA value per share
    data = dict(d=dates, p=[round(r["usde"], 2) for r in rows], n=[round(r["nav_ps"], 2) for r in rows],
                m=[round(r["mnav"], 4) for r in rows])
    body = f'''<header>
  <h1>USDE share price vs the ENA behind each share</h1>
  <p class="sub">Each share is backed by {N['ena_per_share']:.1f} ENA. The grey line is what those tokens are worth; the blue line is what the stock trades at. The gap between them is the discount we want to own. {dlabel(N['start'])} – {asof} 2026.</p>
</header>
<div class="stats">
  <div class="stat"><span>USDE price</span><b>${N['usde']:.2f}</b></div>
  <div class="stat"><span>ENA per share, at ${N['ena']:.4f}</span><b>${N['ena_ps']:.2f}</b></div>
  <div class="stat"><span>Paid per $1 of ENA</span><b>${N['mnav']:.2f}</b></div>
</div>
<div class="bar"><div class="legend">
  <span><i class="lk" style="background:var(--ink-2)"></i>ENA value per share</span>
  <span><i class="lk" style="background:var(--s-strat)"></i>USDE share price</span>
  <span><i class="lk" style="background:var(--ink-2);opacity:.55"></i>Lock-ups off (5 Oct)</span>
</div></div>
<div class="plot"><div class="tip" hidden></div></div>
<p class="foot">ENA value per share = ENA price × {N['ena_held']/1e9:.3f}B ENA ÷ {N['shares']:,} shares. Daily closes; the last point is intraday. Sources as in the mNAV chart.</p>'''
    script = r'''
makeChart(document.getElementById('root'), {
  dates: DATES, strip: true, aria: 'USDE share price against the value of ENA per share',
  bands: [ { i0: IEFF, i1: IEFF, label: 'Lock-ups off (5 Oct)', short: 'Unlocked', row: 0 } ],
  panels: [
    { label: 'USD per share', h: 250, zero: true, tick: v => '$' + v,
      series: [ { values: () => DATA.n, color: 'var(--ink-2)' }, { values: () => DATA.p, color: 'var(--s-strat)' } ] }
  ],
  tooltip: i => [
    { key: 'var(--ink-2)', value: '$' + DATA.n[i].toFixed(2), label: 'ENA value per share' },
    { key: 'var(--s-strat)', value: '$' + DATA.p[i].toFixed(2), label: 'USDE share price' },
    { sep: true, value: DATA.m[i].toFixed(2) + 'x', label: 'mNAV' }
  ]
});
'''.replace("IEFF", str(i_eff))
    tab = [[r["date"], f"${r['usde']:.2f}", f"${r['nav_ps']:.2f}", f"{r['mnav']:.3f}x"] for r in rows]
    (OUT / "usde-price-vs-ena.html").write_text(page("USDE Price vs ENA", body, data, script,
        ["Date", "USDE close", "ENA value per share", "mNAV"], tab))

    # 3. ENA funding on Hyperliquid
    full = [d for d in fdays if len(fund[d]) == 24]
    fa = [sum(fund[d]) * 365 * 100 for d in full]
    f7 = [sum(fa[max(0, i - 6):i + 1]) / len(fa[max(0, i - 6):i + 1]) for i in range(len(fa))]
    data = dict(d=full, f=[round(x, 2) for x in fa], f7=[round(x, 2) for x in f7])
    body = f'''<header>
  <h1>ENA funding on Hyperliquid</h1>
  <p class="sub">Funding on the ENA perp, annualized. Positive means longs pay shorts, so our short leg earns it. {dlabel(full[0])} – {dlabel(full[-1])} 2026.</p>
</header>
<div class="stats">
  <div class="stat"><span>Avg since listing</span><b>{N['funding_ann_since_listing']*100:.1f}%</b></div>
  <div class="stat"><span>Last 30 days</span><b>{N['funding_ann_30d']*100:.1f}%</b></div>
  <div class="stat"><span>Hours positive</span><b>{N['funding_pos_hours']:.0%}</b></div>
  <div class="stat"><span>Negative days</span><b>{N['funding_neg_days']} of {N['funding_full_days']}</b></div>
</div>
<div class="bar">
  <div class="legend">
    <span><i class="sq" style="background:var(--pos)"></i>Positive, our short earns</span>
    <span><i class="sq" style="background:var(--neg)"></i>Negative, our short pays</span>
  </div>
  <div class="seg" role="group" aria-label="Smoothing">
    <button type="button" id="m7" aria-pressed="true">7-day avg</button>
    <button type="button" id="m1" aria-pressed="false">Daily</button>
  </div>
</div>
<div class="plot"><div class="tip" hidden></div></div>
<p class="foot">Hyperliquid settles funding every hour. Each day sums its 24 settlements, then ×365. Full UTC days only. Source: Hyperliquid API (fundingHistory, ENA).</p>'''
    script = r'''
let mode = '7';
const chart = makeChart(document.getElementById('root'), {
  dates: DATES, aria: 'ENA funding rate on Hyperliquid, annualized',
  panels: [
    { label: 'Funding, annualized', h: 220, zero: true, tick: v => v + '%',
      series: [ { type: 'bar', values: () => mode === '7' ? DATA.f7 : DATA.f, color: v => v >= 0 ? 'var(--pos)' : 'var(--neg)' } ] }
  ],
  tooltip: i => [
    { key: (mode === '7' ? DATA.f7[i] : DATA.f[i]) >= 0 ? 'var(--pos)' : 'var(--neg)', value: pct(mode === '7' ? DATA.f7[i] : DATA.f[i]), label: mode === '7' ? 'Funding (7d avg)' : 'Funding that day' }
  ]
});
for (const [id, m] of [['m7', '7'], ['m1', '1']]) document.getElementById(id).addEventListener('click', () => {
  mode = m;
  document.getElementById('m7').setAttribute('aria-pressed', m === '7');
  document.getElementById('m1').setAttribute('aria-pressed', m === '1');
  chart.redraw();
});
'''
    tab = [[d, f"{fa[i]:+.1f}%", f"{f7[i]:+.1f}%"] for i, d in enumerate(full)]
    (OUT / "ena-funding.html").write_text(page("ENA Funding Hyperliquid", body, data, script,
        ["Date", "Funding (ann.)", "7-day avg"], tab))

    # 4. Scenarios: P&L on the long leg by exit mNAV (static SVG bars)
    sc = N["scenarios"]
    items = [s for s in sc if s["name"] != "Today (entry)"]
    sdata = [dict(n=s["name"], m=round(s["mnav"], 3), d=s["date"], r=round(s["ret"] * 100, 1), p=round(s["pnl"])) for s in items]
    body = f'''<header>
  <h1>USDE trade: P&amp;L by exit mNAV</h1>
  <p class="sub">Entry at today's {N['mnav']:.2f}x. ${N['long']/1e3:,.0f}k long USDE, ${N['short']/1e3:,.0f}k short ENA. ENA price flat, before funding and costs. Exit levels come from the mNAV history since listing.</p>
</header>
<div class="plot" id="sc"></div>
<p class="foot">Return on the long = exit mNAV ÷ entry mNAV − 1. The ENA short hedges the token price, so with equal dollars on each side what is left is the change in the multiple. If ENA moves, the result scales by (1 + ENA move). Funding on the short adds about {N['funding_ann_since_listing']*100:.0f}% a year on ${N['short']/1e3:,.0f}k at the average rate since listing.</p>'''
    script = r'''
const SC = SCDATA;
function drawSc() {
  const host = document.getElementById('sc'); host.replaceChildren();
  const NS = 'http://www.w3.org/2000/svg';
  const W = Math.max(300, host.clientWidth), narrow = W < 560;
  const labW = narrow ? 112 : 190, valW = narrow ? 92 : 150, rowH = 44, top = 8;
  const H = top + SC.length * rowH + 8;
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('width', W); svg.setAttribute('height', H); svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', 'P&L by exit mNAV scenario');
  host.appendChild(svg);
  const lo = Math.min(...SC.map(s => s.r), 0), hi = Math.max(...SC.map(s => s.r), 0);
  const x0 = labW, x1 = W - valW, X = v => x0 + (v - lo) / (hi - lo) * (x1 - x0);
  const mk = (tag, a, st) => { const e = document.createElementNS(NS, tag); for (const k in a) e.setAttribute(k, a[k]); if (st) Object.assign(e.style, st); svg.appendChild(e); return e; };
  const tx = (x, y, s, cls, anchor) => { const t = mk('text', { x, y, class: cls, 'text-anchor': anchor || 'start' }); t.textContent = s; return t; };
  mk('line', { x1: X(0), x2: X(0), y1: top - 4, y2: H - 4 }, { stroke: 'var(--axis)', strokeWidth: 1 });
  SC.forEach((s, i) => {
    const y = top + i * rowH, cy = y + rowH / 2;
    tx(0, cy - 3, s.n, 'plabel');
    tx(0, cy + 12, s.m.toFixed(2) + 'x' + (s.d ? ' · ' + (d => d.getUTCDate() + ' ' + ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][d.getUTCMonth()])(new Date(s.d + 'T00:00:00Z')) : ''), 'tick');
    const a = X(Math.min(0, s.r)), b = X(Math.max(0, s.r));
    mk('rect', { x: a, y: cy - 9, width: Math.max(1, b - a), height: 18, rx: 2 }, { fill: s.r >= 0 ? 'var(--pos)' : 'var(--neg)' });
    tx(W, cy - 3, usd(s.p), 'note strong', 'end');
    tx(W, cy + 12, pct(s.r) + ' on the long', 'tick', 'end');
  });
}
new ResizeObserver(() => requestAnimationFrame(drawSc)).observe(document.getElementById('sc'));
drawSc();
'''.replace("SCDATA", json.dumps(sdata))
    tab = [[s["name"], f"{s['mnav']:.3f}x", s["date"] or "", f"{s['ret']*100:+.1f}%", money(s["pnl"])] for s in sc]
    (OUT / "usde-scenarios.html").write_text(page("USDE Trade Scenarios", body, dict(d=[]), script,
        ["Scenario", "Exit mNAV", "Date seen", "Return on long", f"P&amp;L on ${N['long']/1e3:,.0f}k"], tab))


if __name__ == "__main__":
    main()
