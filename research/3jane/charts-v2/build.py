"""Builds the three standalone charts for the short 3Jane DD (19 Nov 2026).

python3 build.py  -> writes 01-liquidity-run.html, 02-loss-ladder-3jane.html,
03-loss-ladder-2x.html next to this file and prints the numbers used in the text.

Loss ladder = 3Jane's own model (USD3_sUSD3_stress_scenarios.xlsx, inputs as of
16 Nov 2026), reproduced exactly; chart 03 doubles its base loss rates.
Liquidity = live 3Jane app figures read 19 Nov 2026 plus Curve pool depth.
"""
from pathlib import Path

OUT = Path(__file__).parent

# ---- 3Jane loss model inputs (unrounded, from the workbook) ----
M = dict(base=4157237.238756125, G=9962002.27139385, s=8726897.0, senior=121273097.054332,
         yU=0.07088348094222274, yS=0.15649812385075468, rate=0.04042673113140205)

def ladder(k, m):
    """1-year return of USD3 and sUSD3 when the forward-flow books lose m*k times
    3Jane's assumed annual loss rate (the x1 loss is already inside today's yields)."""
    extra = (m * k - 1) * M['base']
    if extra <= M['G']:
        f = 1 - max(extra, 0) / M['G']
        return M['yU'] * f, M['yS'] * f
    burn = extra - M['G']
    return -max(0.0, burn - M['s']) / M['senior'], -min(1.0, burn / M['s'])

# ---- liquidity inputs (19 Nov 2026) ----
L = dict(tvl=130.07, aave=14.00, erebor=6.22, curve=1.27, undrawn=3.44 + 4.90,
         slope=53.5, settle=42.9,
         slope_curve=[(0, 0), (30, .449), (60, .744), (90, .890), (180, .986)],
         settle_curve=[(0, 0), (30, .259), (60, .506), (90, .714), (180, .983)])

def runoff(d):
    def f(curve, bal):
        for (d0, v0), (d1, v1) in zip(curve, curve[1:]):
            if d <= d1:
                return bal * (v0 + (v1 - v0) * (d - d0) / (d1 - d0))
        return bal * curve[-1][1]
    return f(L['slope_curve'], L['slope']) + f(L['settle_curve'], L['settle'])

def days_to_clear(pct, conservative):
    instant = L['aave'] + L['curve'] + (0 if conservative else L['erebor'])
    short = L['tvl'] * pct / 100 - instant + (L['undrawn'] if conservative else 0)
    if short <= 0:
        return 0
    for d in range(0, 181):
        if runoff(d) >= short:
            return d
    return None

CSS = r"""
:root{--bg:#ffffff;--ink:#111826;--ink-2:#4a5262;--ink-3:#737b8c;--rule:#dfe3ea;--rule-2:#eceff4;
--s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--zone:#e9f6ef;--bad:#fbeaea;
--f-body:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--f-mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#1a1d24;--ink:#eef0f4;--ink-2:#b9bfcc;--ink-3:#8a91a0;--rule:#2d323c;--rule-2:#262a33;
--s1:#3987e5;--s2:#d95926;--s3:#199e70;--zone:#16291f;--bad:#2f1a1a;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#1a1d24;--ink:#eef0f4;--ink-2:#b9bfcc;--ink-3:#8a91a0;--rule:#2d323c;--rule-2:#262a33;
--s1:#3987e5;--s2:#d95926;--s3:#199e70;--zone:#16291f;--bad:#2f1a1a;color-scheme:dark}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--f-body)}
body{padding:16px max(16px,env(safe-area-inset-right,0px)) 16px max(16px,env(safe-area-inset-left,0px))}
.fig{max-width:960px;margin:0 auto}
h1{font-size:16px;font-weight:600;margin:0;line-height:1.3;text-wrap:balance}
.cap{font-size:12.5px;color:var(--ink-3);margin:3px 0 0}
.chart{position:relative;margin-top:12px;width:100%}
.chart svg{display:block;width:100%;overflow:visible}
.chart svg path,.chart svg text,.chart svg line,.chart svg circle{pointer-events:none}
.legend{display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:10px;font-size:12.5px;color:var(--ink-2)}
.legend span{display:inline-flex;align-items:center;gap:6px}
.legend i{width:10px;height:10px;border-radius:2px;display:inline-block}
.note{font-size:12.5px;color:var(--ink-2);margin:10px 0 0;line-height:1.5;max-width:80ch}
.src{font-size:11.5px;color:var(--ink-3);margin:6px 0 0;font-family:var(--f-mono)}
.tip{position:absolute;pointer-events:none;background:var(--ink);color:var(--bg);font-size:12.5px;line-height:1.45;padding:7px 9px;border-radius:4px;white-space:nowrap;z-index:3;transform:translate(-50%,calc(-100% - 10px));opacity:0;transition:opacity .08s}
@media (prefers-reduced-motion:reduce){.tip{transition:none}}
"""

LIB = r"""
const NS='http://www.w3.org/2000/svg';
const el=(t,a={},p)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e};
const txt=(svg,x,y,s,st,anchor)=>{const t=el('text',{x,y,'text-anchor':anchor||'middle',style:st},svg);t.textContent=s;return t};
const MONO='fill:var(--ink-3);font:11px var(--f-mono)';
function tipFor(c){let t=c.querySelector('.tip');if(!t){t=document.createElement('div');t.className='tip';c.appendChild(t)}
 return{show(h,x,y){t.innerHTML=h;const w=t.offsetWidth,cw=c.clientWidth;x=Math.min(Math.max(x,w/2),Math.max(w/2,cw-w/2));t.style.left=x+'px';t.style.top=Math.max(y,40)+'px';t.style.opacity=1},hide(){t.style.opacity=0}}}
function legend(items){document.getElementById('lg').innerHTML=items.map(i=>i.dash?`<span><i style="background:none;border-top:2px dashed ${i.c};height:0;border-radius:0;width:14px"></i>${i.n}</span>`:`<span><i style="background:${i.c}"></i>${i.n}</span>`).join('')}
function observe(box,draw){draw();new ResizeObserver(()=>draw()).observe(box)}
const pct=v=>(v>=0?'+':'')+(v*100).toFixed(1)+'%';

/* Diverging grouped bars: 1-year return of USD3 and sUSD3 per loss multiple */
function ladderChart(o){const box=document.getElementById('c');observe(box,()=>{box.querySelectorAll('svg').forEach(s=>s.remove());
 const W=Math.max(300,box.clientWidth),H=330,m={l:50,r:10,t:16,b:52},iw=W-m.l-m.r,ih=H-m.t-m.b;
 const lo=-1,hi=0.2,y=v=>m.t+(hi-v)/(hi-lo)*ih;
 const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,height:H,role:'img','aria-label':document.title},box);const tip=tipFor(box);
 // zones: where USD3 principal is hit
 const bi=o.rows.findIndex(r=>r.u<0);
 [-1,-0.75,-0.5,-0.25,0,0.2].forEach(v=>{el('line',{x1:m.l,x2:W-m.r,y1:y(v),y2:y(v),style:`stroke:${v===0?'var(--ink-3)':'var(--rule-2)'}`},svg);txt(svg,m.l-6,y(v)+4,(v>0?'+':'')+Math.round(v*100)+'%',MONO,'end')});
 const n=o.rows.length,band=iw/n,bw=Math.min(26,band*0.32),gap=2;
 if(bi>=0){el('rect',{x:m.l+bi*band,y:m.t,width:iw-bi*band,height:ih,style:'fill:var(--bad)'},svg);txt(svg,W-m.r-6,m.t+14,'USD3 principal hit',"fill:var(--ink-2);font:600 11.5px var(--f-body)",'end')}
 o.rows.forEach((r,i)=>{const cx=m.l+i*band+band/2;
  const hit=el('rect',{x:m.l+i*band,y:m.t,width:band,height:ih,style:'fill:transparent'},svg);
  [[r.u,'var(--s1)',-bw-gap/2],[r.s,'var(--s2)',gap/2]].forEach(([v,c,dx])=>{if(Math.abs(v)<0.0005){txt(svg,cx+dx+bw/2,y(0)-5,'0','fill:var(--ink-3);font:10px var(--f-mono)');return}const y0=y(0),y1=y(v);el('rect',{x:cx+dx,y:Math.min(y0,y1),width:bw,height:Math.max(1.5,Math.abs(y1-y0)),rx:2,style:`fill:${c};pointer-events:none`},svg)});
  txt(svg,cx,m.t+ih+16,r.lab,MONO);txt(svg,cx,m.t+ih+31,r.rate,'fill:var(--ink-2);font:11px var(--f-mono)');
  hit.addEventListener('mouseenter',()=>{hit.style.fill='var(--rule-2)';hit.style.fillOpacity=.6;tip.show(`<b>${r.lab} expected loss · ${r.rate} a year</b><br>USD3: ${r.u>=0?pct(r.u)+' yield':pct(r.u)+' principal'}<br>sUSD3: ${r.s>=0?pct(r.s)+' yield':pct(r.s)+' principal'}`,cx,y(Math.max(r.u,r.s,0)))});
  hit.addEventListener('mouseleave',()=>{hit.style.fill='transparent';tip.hide()})});
 txt(svg,m.l+iw/2,H-4,o.xTitle,'fill:var(--ink-3);font:11px var(--f-body)')});
 legend([{n:'USD3 (senior) 1-year return',c:'var(--s1)'},{n:'sUSD3 (junior, first loss) 1-year return',c:'var(--s2)'},{n:'USD3 principal loss zone',c:'var(--bad)'}])}

/* Liquidity: days until all redemptions are paid vs redemption size */
function liqChart(o){const box=document.getElementById('c');observe(box,()=>{box.querySelectorAll('svg').forEach(s=>s.remove());
 const W=Math.max(300,box.clientWidth),H=320,m={l:46,r:16,t:16,b:44},iw=W-m.l-m.r,ih=H-m.t-m.b;
 const x=v=>m.l+v/80*iw,y=v=>m.t+ih-(v/180)*ih;
 const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,height:H,role:'img','aria-label':document.title},box);const tip=tipFor(box);
 el('rect',{x:m.l,y:m.t,width:x(o.instant)-m.l,height:ih,style:'fill:var(--zone)'},svg);
 txt(svg,m.l+6,m.t+14,'Paid instantly','fill:var(--ink-2);font:600 11.5px var(--f-body)','start');
 [0,30,60,90,120,150,180].forEach(v=>{el('line',{x1:m.l,x2:W-m.r,y1:y(v),y2:y(v),style:'stroke:var(--rule-2)'},svg);txt(svg,m.l-6,y(v)+4,v+'d',MONO,'end')});
 [0,10,20,30,40,50,60,70,80].forEach(v=>txt(svg,x(v),m.t+ih+16,v+'%',MONO));
 txt(svg,m.l+iw/2,H-6,'Redemption requests, % of TVL ($130M)','fill:var(--ink-3);font:11px var(--f-body)');
 el('line',{x1:m.l,x2:W-m.r,y1:m.t+ih,y2:m.t+ih,style:'stroke:var(--ink-3)'},svg);
 const lx=x(o.loopPct);el('line',{x1:lx,x2:lx,y1:m.t,y2:m.t+ih,style:'stroke:var(--ink-2);stroke-width:1.5;stroke-dasharray:4 4'},svg);
 txt(svg,lx+4,m.t+30,'All loops unwind (~48%)','fill:var(--ink-2);font:11px var(--f-mono)','start');
 o.series.forEach(s=>{const pts=s.v.map(([p,d])=>[x(p),y(Math.min(d,180))]);
  el('path',{d:'M'+pts.map(q=>q.join(',')).join('L'),style:`fill:none;stroke:${s.c};stroke-width:2`},svg);
  s.v.forEach(([p,d],i)=>{if(p%10)return;el('circle',{cx:pts[i][0],cy:pts[i][1],r:4,style:`fill:${s.c};stroke:var(--bg);stroke-width:2`},svg)})});
 const hit=el('rect',{x:m.l,y:m.t,width:iw,height:ih,style:'fill:transparent'},svg);
 hit.addEventListener('mousemove',e=>{const r=svg.getBoundingClientRect();const px=(e.clientX-r.left)*W/r.width;const p=Math.max(0,Math.min(80,Math.round((px-m.l)/iw*80/5)*5));
  const rows=o.series.map(s=>{const d=s.v.find(q=>q[0]===p);return `${s.n}: <b>${d[1]===0?'paid now':(d[1]>180?'>180':d[1])+' days'}</b>`});
  tip.show(`<b>${p}% of TVL = $${(o.tvl*p/100).toFixed(0)}M</b><br>`+rows.join('<br>'),x(p),y(60))});
 hit.addEventListener('mouseleave',()=>tip.hide())});
 legend(o.series.map(s=>({n:s.n,c:s.c})).concat([{n:'Covered by cash on hand',c:'var(--zone)'}]))}
"""

HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>__CSS__</style></head>
<body><figure class="fig" id="fig"><h1>__TITLE__</h1><p class="cap">__CAP__</p><div class="chart" id="c"></div><div class="legend" id="lg"></div><p class="note">__NOTE__</p><p class="src">Source: __SRC__</p></figure>
<script>__LIB__</script>
<script>
__JS__
</script></body></html>
"""

def page(slug, title, cap, note, src, js):
    html = HEAD
    for k, v in (("__CSS__", CSS), ("__LIB__", LIB), ("__JS__", js), ("__TITLE__", title),
                 ("__CAP__", cap), ("__NOTE__", note), ("__SRC__", src)):
        html = html.replace(k, v)
    (OUT / f"{slug}.html").write_text(html)

def rows_js(k, mults):
    rows = []
    for m in mults:
        u, s = ladder(k, m)
        rows.append(f"{{lab:'{m:g}×',rate:'{m*k*M['rate']*100:.0f}%',u:{u:.5f},s:{s:.5f}}}")
    return "[" + ",".join(rows) + "]"

# 01 liquidity ---------------------------------------------------------------
grid = list(range(0, 81, 5))
base = [(p, days_to_clear(p, False)) for p in grid]
cons = [(p, days_to_clear(p, True)) for p in grid]
to_js = lambda v: "[" + ",".join(f"[{p},{d if d is not None else 999}]" for p, d in v) + "]"
instant_pct = 100 * (L['aave'] + L['erebor'] + L['curve']) / L['tvl']
page("01-liquidity-run", "If holders rush for the exit: how long until everyone is paid",
     "Days until all redemption requests are paid, by size of the run. Cash on hand pays first, then 3Jane stops buying new loans and waits for Slope and Settle to repay.",
     f"Cash on hand (Aave ${L['aave']:.1f}M + bank ${L['erebor']:.1f}M + ~${L['curve']:.1f}M of Curve depth) covers a run of up to ~{instant_pct:.0f}% of TVL. "
     "Beyond that, holders wait for loans to repay: ~2 weeks for a 30% run, ~6 weeks for 50%. "
     "Conservative = bank cash already committed to new loans, and 3Jane still funds the undrawn LendSwift and GigFi lines ($8.3M). "
     "Assumes borrowers pay on schedule; principal only.",
     "3Jane app (backing, Slope and Settle liquidity tabs), 19 Nov 2026; Curve USD3/frxUSD pool on-chain; Re7 calculation",
     f"liqChart({{tvl:{L['tvl']},instant:{instant_pct:.2f},loopPct:{100*62.2/L['tvl']:.1f},series:["
     f"{{n:'Base case',c:'var(--s1)',v:{to_js(base)}}},{{n:'Conservative case',c:'var(--s2)',v:{to_js(cons)}}}]}});")

# 02 / 03 loss ladders --------------------------------------------------------
page("02-loss-ladder-3jane", "Loss ladder: 3Jane's scenarios",
     "1-year return of each tranche if Slope and Settle lose a multiple of 3Jane's assumed annual loss rate (Slope 3.6%, Settle 4.6%; blended 4.0%). Labels: multiple and annual loss rate on the $103M book.",
     "Today's expected loss (1×) is already inside the yields. Extra losses first reduce both yields, which reach zero at 3.4× (13.7% a year). "
     "sUSD3 is then wiped out and USD3 principal is first hit at 5.5× (22% a year). Losses are assumed to arrive evenly over the year.",
     "3Jane USD3/sUSD3 stress model (inputs as of 16 Nov 2026), reproduced",
     f"ladderChart({{rows:{rows_js(1,[1,2,3,4,5,6,8,10])},xTitle:'Multiple of 3Jane\\'s assumed loss rate · annual loss rate on the book'}});")

page("03-loss-ladder-2x", "Loss ladder: Re7 stress, base loss rates doubled",
     "Same model with base loss rates doubled (Slope 7.1%, Settle 9.3%; blended 8.1%), roughly Slope's full historical loss rate. 1× here = 2× in 3Jane's model.",
     "At 1× yields are already cut to ~4.1% (USD3) and ~9.1% (sUSD3). Yields reach zero at 1.7× (13.7% a year). "
     "USD3 principal is first hit at 2.75× (22% a year), and a 4× year (32%, like repeating Slope's worst quarter all year) costs USD3 holders ~8.6%.",
     "3Jane USD3/sUSD3 stress model (inputs as of 16 Nov 2026), base loss rates ×2; Re7 calculation",
     f"ladderChart({{rows:{rows_js(2,[1,1.5,2,2.5,3,4,5])},xTitle:'Multiple of the doubled loss rate · annual loss rate on the book'}});")

if __name__ == "__main__":
    print("instant liquidity %.1f%% of TVL" % instant_pct)
    for p in (10, 20, 30, 40, 50, 60, 75):
        print("run %d%%: base %s days, conservative %s days" % (p, days_to_clear(p, False), days_to_clear(p, True)))
    for k, ms in ((1, [1, 2, 3, 4, 5, 6, 8, 10]), (2, [1, 1.5, 2, 2.5, 3, 4, 5])):
        for m in ms:
            u, s = ladder(k, m)
            print("k=%d m=%g rate=%.1f%% USD3 %+.1f%% sUSD3 %+.1f%%" % (k, m, m * k * M['rate'] * 100, u * 100, s * 100))
