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
# ENA received at closing (Q2 10-Q, Note 3): Ethena contribution 284,954,407.29 + PIPE 1,405,754,435.84
# + additional PIPE 1,340,695,577.81. Q3 8-K values ($802M at $0.2648, $576M at $0.1901) reconcile within 0.1%.
ENA_HELD = 284_954_407.29 + 1_405_754_435.84 + 1_340_695_577.81
CASH = 10_352_692
OTHER_ASSETS = 12_771_432 - 10_352_692 + 689_375   # other current assets + intangibles
CUR_LIAB = 1_983_077
WAIVER_SIGNED, WAIVER_EFFECTIVE = "2026-09-14", "2026-10-05"

# --- trade sizing used in the report ---
LONG = 1_000_000
SHORT = 1_000_000
HL_LEV = 5


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


def short_usd(v):
    return f"${v/1e6:g}M" if v >= 1e6 else f"${v/1e3:,.0f}k"


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
  <p class="sub">mNAV = (USDE price × shares) ÷ (ENA held × ENA price). 1.0x would mean the stock trades at the value of its ENA. {dlabel(N['start'])} – {asof} 2026.</p>
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
<p class="foot">mNAV = (USDE price × {N['shares']:,} Class A shares) ÷ ({N['ena_held']:,.0f} ENA × ENA price), daily at the Nasdaq close. Share count from the Q3 2026 results (8-K, 16 Nov 2026). ENA held = tokens received at closing per the Q2 10-Q (Note 3); the Q3 values reconcile within 0.1%. ENA price: Hyperliquid ENA perp, hourly candle closing at 4pm New York. USDE: Nasdaq daily close (Yahoo Finance). The last point is intraday. The waiver was signed on 14 Sep (a Monday) and the 8-K was filed on 17 Sep.</p>'''
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
  <h1>USDE share price vs ENA value per share</h1>
  <p class="sub">Grey: what the ENA behind each share is worth ({N['ena_per_share']:.1f} ENA × ENA price). Blue: the USDE share price. The gap between the two lines is the discount. {dlabel(N['start'])} – {asof} 2026.</p>
</header>
<div class="stats">
  <div class="stat"><span>USDE share price</span><b>${N['usde']:.2f}</b></div>
  <div class="stat"><span>ENA value per share</span><b>${N['ena_ps']:.2f}</b></div>
  <div class="stat"><span>Discount today</span><b>{1 - N['mnav']:.0%}</b></div>
  <div class="stat"><span>Average discount since listing</span><b>{1 - N['avg']:.0%}</b></div>
</div>
<div class="bar"><div class="legend">
  <span><i class="lk" style="background:var(--ink-2)"></i>ENA value per share</span>
  <span><i class="lk" style="background:var(--s-strat)"></i>USDE share price</span>
  <span><i class="lk" style="background:var(--ink-2);opacity:.55"></i>Lock-ups off (5 Oct)</span>
</div></div>
<div class="plot"><div class="tip" hidden></div></div>
<p class="foot">ENA value per share = ENA price × {N['ena_held']:,.0f} ENA ÷ {N['shares']:,} shares. Discount = 1 − USDE price ÷ ENA value per share. Average discount = average of the daily discounts since listing. Daily closes; the last point is intraday. Sources as in the mNAV chart.</p>'''
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
    { sep: true, value: Math.round((1 - DATA.m[i]) * 100) + '%', label: 'Discount' }
  ]
});
'''.replace("IEFF", str(i_eff))
    tab = [[r["date"], f"${r['usde']:.2f}", f"${r['nav_ps']:.2f}", f"{1 - r['mnav']:.0%}"] for r in rows]
    (OUT / "usde-price-vs-ena.html").write_text(page("USDE Price vs ENA", body, data, script,
        ["Date", "USDE close", "ENA value per share", "Discount"], tab))

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

    # 4. Scenarios: net P&L grid, exit mNAV x ENA move (same inputs and formula as usde_mnav_model.xlsx)
    M_USDE, M_ENA, M_LONG, M_SHORT = 4.35, 0.1169, 1_000_000, 1_000_000
    m0 = (M_USDE * N["shares"]) / (N["ena_held"] * M_ENA)
    moves = [-0.9, -0.5, -0.25, 0, 0.25, 0.5, 1.0]
    rows_m = [(1.0, ""), (0.9, ""), (0.8, ""), (0.7, ""), (0.6, ""), (round(N["max"], 2), "Max"), (0.5, ""), (0.4, ""),
              (round(N["avg"], 2), "Avg"), (0.3, ""), (m0, "Entry"), (0.2, ""), (round(N["min"], 2), "Min"), (0.1, ""), (0.0, "")]
    pnl = lambda m, e: M_LONG * ((1 + e) * m / m0 - 1) - M_SHORT * e
    grid = [dict(m=m, l=l, v=[round(pnl(m, e)) for e in moves]) for m, l in rows_m]
    vmax = max(abs(x) for g in grid for x in g["v"])
    body = f"""<header>
  <h1>USDE trade: P&amp;L by mNAV and ENA price</h1>
  <p class="sub">Net P&amp;L on $1M long USDE and $1M short ENA, entering at {m0:.3f}x (USDE ${M_USDE:.2f}, ENA ${M_ENA:.4f}). Rows: mNAV at exit. Columns: ENA price move. No rebalancing, before fees and funding.</p>
</header>
<div class="bar"><div class="legend">
  <span><i class="sq" style="background:var(--pos)"></i>We make money</span>
  <span><i class="sq" style="background:var(--neg)"></i>We lose money</span>
  <span>Darker = bigger</span>
</div></div>
<div class="hm-wrap"><table class="hm" id="hm"></table></div>
<p class="foot">Net P&amp;L = long × [(1 + ENA move) × exit mNAV ÷ entry mNAV − 1] − short × ENA move. The mNAV decides whether we make or lose money; ENA's move only changes how much. Max, Avg and Min are the mNAV's highest, average and lowest daily close since the 26 Jun 2026 listing. Above $11.50 per share the warrants dilute, so the top rows overstate the gains.</p>
<style>
.hm-wrap {{ overflow-x: auto; }}
.hm {{ border-collapse: separate; border-spacing: 2px; width: 100%; min-width: 560px; font-variant-numeric: tabular-nums; font-size: 12px; }}
.hm th, .hm td {{ padding: 6px 8px; text-align: right; white-space: nowrap; border: 0; position: static; }}
.hm thead th {{ color: var(--ink-2); font-weight: 600; background: transparent; }}
.hm th.rl {{ text-align: left; color: var(--muted); font-weight: 500; width: 1%; }}
.hm th.rm {{ color: var(--ink); font-weight: 600; text-align: right; width: 1%; }}
.hm td {{ border-radius: 3px; color: var(--ink); }}
.hm tr.entry th, .hm tr.entry td {{ font-weight: 700; }}
.hm tr.entry td {{ outline: 1.5px solid var(--ink-2); outline-offset: -1.5px; }}
</style>"""
    script = r"""
const G = GRID, MOVES = MOVESJS, VMAX = VMAXJS;
const fmt = v => (v < 0 ? '−' : v > 0 ? '+' : '') + '$' + Math.abs(v).toLocaleString('en-US');
const tbl = document.getElementById('hm');
const th = document.createElement('thead'), hr = document.createElement('tr');
hr.innerHTML = '<th class="rl"></th><th class="rm">mNAV ↓ / ENA →</th>' + MOVES.map(m => '<th>' + (m > 0 ? '+' : m < 0 ? '−' : '') + Math.abs(Math.round(m * 100)) + '%</th>').join('');
th.appendChild(hr); tbl.appendChild(th);
const tb = document.createElement('tbody');
G.forEach(r => {
  const tr = document.createElement('tr'); if (r.l === 'Entry') tr.className = 'entry';
  const l = document.createElement('th'); l.className = 'rl'; l.textContent = r.l; tr.appendChild(l);
  const m = document.createElement('th'); m.className = 'rm'; m.textContent = r.m.toFixed(r.l === 'Entry' ? 3 : 2) + 'x'; tr.appendChild(m);
  r.v.forEach(v => {
    const td = document.createElement('td');
    const k = Math.round(10 + 60 * Math.sqrt(Math.min(1, Math.abs(v) / VMAX)));
    td.style.background = Math.abs(v) < 1 ? 'transparent' : 'color-mix(in srgb, ' + (v > 0 ? 'var(--pos)' : 'var(--neg)') + ' ' + k + '%, var(--bg))';
    td.textContent = Math.abs(v) < 1 ? '$0' : fmt(v);
    tr.appendChild(td);
  });
  tb.appendChild(tr);
});
tbl.appendChild(tb);
""".replace("GRID", json.dumps(grid)).replace("MOVESJS", json.dumps(moves)).replace("VMAXJS", str(vmax))
    tab = [[f"{g['m']:.3f}x" + (f" ({g['l']})" if g['l'] else "")] + [money(x) for x in g["v"]] for g in grid]
    (OUT / "usde-scenarios.html").write_text(page("USDE Trade Scenarios", body, dict(d=[]), script,
        ["Exit mNAV"] + [f"ENA {e*100:+.0f}%" for e in moves], tab))


if __name__ == "__main__":
    main()
