import sys, json, pandas as pd
sk, bpath, opath, out = sys.argv[1:5]
b = pd.read_csv(bpath, parse_dates=['date']); o = pd.read_csv(opath, parse_dates=['date'])
d = b.merge(o, on='date', suffixes=('_b', '_o'))
assert (d.short_funding_b - d.short_funding_o).abs().max() < 1e-9  # same Hyperliquid leg
sb = (d.short_funding_b - d.long_funding_b).round(12) * 36500
so = (d.short_funding_o - d.long_funding_o).round(12) * 36500
r7 = lambda s: s.rolling(7, min_periods=1).mean()
r = lambda s: [round(float(v), 2) + 0.0 for v in s]
ab, ao = sb.mean(), so.mean()
n = len(d); better = (so > sb).mean(); pb, po = (sb > 0).mean(), (so > 0).mean()
day = lambda t: f"{t.day} {t:%b}"
data = dict(d=d.date.dt.strftime('%Y-%m-%d').tolist(), b=r(sb), o=r(so), b7=r(r7(sb)), o7=r(r7(so)), ab=round(ab, 2), ao=round(ao, 2))
css = open(f'{sk}/charts.css').read().replace('--s-strat: #2a78d6;', '--s-strat: #2a78d6; --avg: #898781;').replace('--s-strat: #3987e5;', '--s-strat: #3987e5; --avg: #898781;')
eng = open(f'{sk}/engine.js').read()
rows = '\n'.join(f'<tr><td>{t:%Y-%m-%d}</td><td>{x:.1f}%</td><td>{y:.1f}%</td><td>{y-x:+.1f}%</td></tr>'.replace('-', '−', 0) for t, x, y in zip(d.date, sb, so))
html = f'''<title>HYPE Spread: Binance vs OKX</title>
<meta name="claude:viewport-fit-sides" content="cover">
{css}
<div class="wrap" id="root">
<header>
  <h1>HYPE funding spread: long Binance vs long OKX</h1>
  <p class="sub">Funding spread of each trade, both short HYPE on Hyperliquid, annualized, over the {n} days both venues have data: {day(d.date.iloc[0])} – {day(d.date.iloc[-1])} {d.date.iloc[-1]:%Y}. Spread = Hyperliquid funding − long-venue funding.</p>
</header>
<div class="stats">
  <div class="stat"><span>Avg spread, OKX</span><b>{ao:.2f}%</b></div>
  <div class="stat"><span>Avg spread, Binance</span><b>{ab:.2f}%</b></div>
  <div class="stat"><span>APR at 5×, OKX vs Binance</span><b>{ao*2.5:.1f}% vs {ab*2.5:.1f}%</b></div>
  <div class="stat"><span>Days OKX spread was higher</span><b>{better:.0%}</b></div>
</div>
<div class="bar">
  <div class="legend">
    <span><i class="lk" style="background:var(--s-hl)"></i>Long OKX</span>
    <span><i class="lk" style="background:var(--s-bin)"></i>Long Binance</span>
    <span><i class="lk" style="background:var(--s-hl);opacity:.55;height:1px"></i>OKX average {ao:.2f}%</span>
    <span><i class="lk" style="background:var(--s-bin);opacity:.55;height:1px"></i>Binance average {ab:.2f}%</span>
  </div>
  <div class="seg" role="group" aria-label="Smoothing">
    <button type="button" id="m7" aria-pressed="true">7-day avg</button>
    <button type="button" id="m1" aria-pressed="false">Daily</button>
  </div>
</div>
<div class="plot"><div class="tip" hidden></div></div>
<p class="foot">Daily funding on each venue sums every settlement that day (Binance every 4h, OKX every 8h, Hyperliquid every 1h), then ×365. 7-day avg is trailing. Positive days: OKX {po:.0%}, Binance {pb:.0%}. Implied APR = spread × 2.5 ($500k per leg on $200k margin). Source: Grafana (bishop_daily_funding_rate_history_materialized).</p>
<details><summary>Show data table</summary><div class="tablewrap"><table><thead><tr><th>Date</th><th>Spread, long Binance</th><th>Spread, long OKX</th><th>OKX − Binance</th></tr></thead><tbody>
{rows}
</tbody></table></div></details>
</div>
<script>
{eng}
const DATA = {json.dumps(data, separators=(',', ':'))};
const DATES = DATA.d.map(s => new Date(s + 'T00:00:00Z'));
const pct = v => (v > 0 ? '+' : v < 0 ? '\\u2212' : '') + Math.abs(v).toFixed(1) + '%';
let mode = '7';
const pick = (a, b) => () => mode === '7' ? DATA[a] : DATA[b];
const flat = v => () => DATES.map(() => v);
const last = DATES.length - 1;
const chart = makeChart(document.getElementById('root'), {{
  dates: DATES, aria: 'Funding spread of the long Binance and long OKX trades over time, with period averages',
  panels: [
    {{ label: 'Funding spread, annualized', h: 280, zero: true, tick: v => v + '%',
      series: [
        {{ values: flat(DATA.ab), color: 'var(--s-bin)', width: 1.25, opacity: 0.55 }},
        {{ values: flat(DATA.ao), color: 'var(--s-hl)', width: 1.25, opacity: 0.55 }},
        {{ values: pick('b7', 'b'), color: 'var(--s-bin)' }},
        {{ values: pick('o7', 'o'), color: 'var(--s-hl)' }} ] }}
  ],
  tooltip: i => {{
    const sfx = mode === '7' ? ' (7d avg)' : '';
    const o = mode === '7' ? DATA.o7[i] : DATA.o[i], b = mode === '7' ? DATA.b7[i] : DATA.b[i];
    return [
      {{ key: 'var(--s-hl)', value: pct(o), label: 'Long OKX' + sfx }},
      {{ key: 'var(--s-bin)', value: pct(b), label: 'Long Binance' + sfx }},
      {{ sep: true, value: pct(o - b), label: 'OKX − Binance' }}
    ];
  }}
}});
for (const [id, m] of [['m7', '7'], ['m1', '1']]) document.getElementById(id).addEventListener('click', () => {{
  mode = m;
  document.getElementById('m7').setAttribute('aria-pressed', m === '7');
  document.getElementById('m1').setAttribute('aria-pressed', m === '1');
  chart.redraw();
}});
</script>
'''
open(out, 'w').write(html)
print(n, f'OKX {ao:.2f} Binance {ab:.2f} better {better:.0%} pos {po:.0%}/{pb:.0%}')
