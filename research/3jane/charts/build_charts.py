"""Builds the standalone 3Jane chart pages (one self-contained HTML per chart).

Run: python3 build_charts.py  -> writes NN-name.html next to this file.
Data is hard-coded from the 3Jane app (read 5 Nov 2026), the data room and the
Trenches LCC deal; see the `source` line on each chart.
"""
from pathlib import Path

OUT = Path(__file__).parent

CSS = r"""
:root{--bg:#ffffff;--ink:#111826;--ink-2:#4a5262;--ink-3:#737b8c;--rule:#dfe3ea;--rule-2:#eceff4;
--s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--s4:#eda100;--s5:#e87ba4;--s6:#008300;--s1-light:#86b6ef;--s2-light:#f5b394;
--f-body:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--f-mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#1a1d24;--ink:#eef0f4;--ink-2:#b9bfcc;--ink-3:#8a91a0;--rule:#2d323c;--rule-2:#262a33;
--s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--s5:#d55181;--s6:#008300;--s1-light:#1c5cab;--s2-light:#8a3a1a;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#1a1d24;--ink:#eef0f4;--ink-2:#b9bfcc;--ink-3:#8a91a0;--rule:#2d323c;--rule-2:#262a33;
--s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--s5:#d55181;--s6:#008300;--s1-light:#1c5cab;--s2-light:#8a3a1a;color-scheme:dark}
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
.tip{position:absolute;pointer-events:none;background:var(--ink);color:var(--bg);font-size:12.5px;line-height:1.4;padding:7px 9px;border-radius:4px;white-space:nowrap;z-index:3;transform:translate(-50%,calc(-100% - 10px));opacity:0;transition:opacity .08s}
@media (prefers-reduced-motion:reduce){.tip{transition:none}}
"""

LIB = r"""
const NS='http://www.w3.org/2000/svg';
const el=(t,a={},p)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e};
const txt=(svg,x,y,s,st,anchor)=>{const t=el('text',{x,y,'text-anchor':anchor||'middle',style:st},svg);t.textContent=s;return t};
const MONO='fill:var(--ink-3);font:11px var(--f-mono)';
function tipFor(c){let t=c.querySelector('.tip');if(!t){t=document.createElement('div');t.className='tip';c.appendChild(t)}
 return{show(h,x,y){t.innerHTML=h;const w=t.offsetWidth,cw=c.clientWidth;x=Math.min(Math.max(x,w/2),Math.max(w/2,cw-w/2));t.style.left=x+'px';t.style.top=y+'px';t.style.opacity=1},hide(){t.style.opacity=0}}}
function legend(items){const L=document.getElementById('lg');L.innerHTML=items.map(i=>i.dash?`<span><i style="background:none;border-top:2px dashed ${i.c};height:0;border-radius:0;width:14px"></i>${i.n}</span>`:`<span><i style="background:${i.c}"></i>${i.n}</span>`).join('')}
function niceMax(v){const p=Math.pow(10,Math.floor(Math.log10(v)));const n=v/p;return (n<=1?1:n<=2?2:n<=2.5?2.5:n<=5?5:10)*p}
function topR(x,y,w,h,r){r=Math.min(r,w/2,h);if(h<=0)return '';return `M${x},${y+h}V${y+r}Q${x},${y} ${x+r},${y}H${x+w-r}Q${x+w},${y} ${x+w},${y+r}V${y+h}Z`}
function rightR(x,y,w,h,r){r=Math.min(r,h/2,w);if(w<=0)return '';return `M${x},${y}H${x+w-r}Q${x+w},${y} ${x+w},${y+r}V${y+h-r}Q${x+w},${y+h} ${x+w-r},${y+h}H${x}Z`}
function observe(box,draw){draw();new ResizeObserver(()=>draw()).observe(box)}

/* vertical bars, grouped or stacked */
function vbar(o){const box=document.getElementById('c');observe(box,()=>{box.querySelectorAll('svg').forEach(s=>s.remove());
 const W=Math.max(300,box.clientWidth),H=o.h||260,m={l:o.ml||46,r:o.mr||12,t:18,b:(o.rot?56:30)+(o.catSub?16:0)},iw=W-m.l-m.r,ih=H-m.t-m.b;
 const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,height:H,role:'img','aria-label':document.title},box);const n=o.cats.length,S=o.series.length;
 let max=o.yMax;if(!max){max=0;o.cats.forEach((c,i)=>{if(o.stacked)max=Math.max(max,o.series.reduce((a,s)=>a+(s.v[i]||0),0));else o.series.forEach(s=>max=Math.max(max,s.v[i]||0))});(o.refs||[]).forEach(r=>max=Math.max(max,r.v));max=niceMax(max*1.1)}
 const y=v=>m.t+ih-(v/max)*ih;const ticks=o.ticks||4;
 for(let k=0;k<=ticks;k++){const v=max*k/ticks;el('line',{x1:m.l,x2:W-m.r,y1:y(v),y2:y(v),style:'stroke:var(--rule-2)'},svg);txt(svg,m.l-6,y(v)+4,o.yFmt?o.yFmt(v):v,MONO,'end')}
 const band=iw/n,inner=band*(o.barFrac||0.7),gap=2,tip=tipFor(box);
 o.cats.forEach((c,i)=>{const x0=m.l+i*band+(band-inner)/2;
  const hit=el('rect',{x:m.l+i*band,y:m.t,width:band,height:ih,style:'fill:transparent'},svg);
  if(o.stacked){let acc=0;o.series.forEach((s,j)=>{const v=s.v[i]||0;if(!v)return;const y1=y(acc+v),y0=y(acc);const top=o.series.slice(j+1).every(q=>!q.v[i]);const hh=y0-y1-(acc>0?gap:0);
    el('path',{d:top?topR(x0,y1,inner,hh,3):`M${x0},${y1}h${inner}v${hh}h${-inner}Z`,style:`fill:${s.cf?s.cf(i):s.c}`},svg);acc+=v})}
  else{const bw=(inner-gap*(S-1))/S;o.series.forEach((s,j)=>{const v=s.v[i];if(v==null)return;const hh=Math.max(v>0?1.5:0,m.t+ih-y(v));el('path',{d:topR(x0+j*(bw+gap),m.t+ih-hh,bw,hh,3),style:`fill:${s.cf?s.cf(i):s.c}`},svg)})}
  if(o.top)txt(svg,m.l+i*band+band/2,y(o.top.val(i))-6,o.top.txt(i),'fill:var(--ink-2);font:11px var(--f-mono)');
  const ev=o.labelEvery||1;if(i%ev===0){const lx=m.l+i*band+band/2,ly=m.t+ih+16;const t=txt(svg,lx,ly,o.catFmt?o.catFmt(c):c,MONO,o.rot?'end':'middle');if(o.rot)t.setAttribute('transform',`rotate(-40 ${lx} ${ly-4})`);if(o.catSub)txt(svg,lx,ly+16,o.catSub(i),'fill:var(--ink);font:600 12px var(--f-mono)')}
  hit.addEventListener('mouseenter',()=>{hit.style.fill='var(--rule-2)';const tot=o.stacked?o.series.reduce((a,s)=>a+(s.v[i]||0),0):Math.max(...o.series.map(s=>s.v[i]||0));
   tip.show(`<b>${o.tipCat?o.tipCat(c,i):c}</b><br>`+o.series.filter(s=>s.v[i]!=null&&(!o.stacked||s.v[i])).map(s=>`${s.n}: ${o.tipFmt?o.tipFmt(s.v[i]):s.v[i]}`).join('<br>')+(o.tipExtra?o.tipExtra(i):''),m.l+i*band+band/2,y(tot))});
  hit.addEventListener('mouseleave',()=>{hit.style.fill='transparent';tip.hide()})});
 el('line',{x1:m.l,x2:W-m.r,y1:m.t+ih,y2:m.t+ih,style:'stroke:var(--ink-3)'},svg);
 (o.refs||[]).forEach(r=>{el('line',{x1:m.l,x2:W-m.r,y1:y(r.v),y2:y(r.v),style:'stroke:var(--ink-2);stroke-width:1.5;stroke-dasharray:4 4'},svg);if(r.outside)txt(svg,W-m.r+6,y(r.v)+4,r.label,'fill:var(--ink-2);font:11px var(--f-mono)','start');else txt(svg,r.left?m.l+4:W-m.r,y(r.v)-6,r.label,'fill:var(--ink-2);font:11px var(--f-mono)',r.left?'start':'end')})})}

/* horizontal bars with optional range segment and vertical reference lines */
function hbars(o){const box=document.getElementById('c');observe(box,()=>{box.querySelectorAll('svg').forEach(s=>s.remove());
 const W=Math.max(300,box.clientWidth),narrow=W<600,rowH=34,lab=narrow?0:230,m={l:lab+8,r:56,t:28,b:26};const rows=o.rows.length;
 const H=m.t+rows*(rowH+(narrow?16:0))+m.b,iw=W-m.l-m.r;const x=v=>m.l+(v/o.max)*iw;
 const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,height:H,role:'img','aria-label':document.title},box);const tip=tipFor(box);
 for(let v=0;v<=o.max+1e-9;v+=o.step){el('line',{x1:x(v),x2:x(v),y1:m.t-4,y2:H-m.b,style:'stroke:var(--rule-2)'},svg);txt(svg,x(v),H-m.b+16,o.fmt(v),MONO)}
 o.rows.forEach((r,i)=>{const rh=rowH+(narrow?16:0),y0=m.t+i*rh+(narrow?16:0),bh=18,by=y0+(rowH-bh)/2-4;
  if(narrow)txt(svg,m.l,y0-2,r.n,'fill:var(--ink-2);font:12px var(--f-body)','start');else txt(svg,m.l-10,by+bh/2+4,r.n,'fill:var(--ink-2);font:12.5px var(--f-body)','end');
  const lo=r.lo,hi=r.hi==null?r.lo:r.hi;
  el('path',{d:r.hi==null?rightR(m.l,by,x(lo)-m.l,bh,3):`M${m.l},${by}H${x(lo)}V${by+bh}H${m.l}Z`,style:`fill:${r.c||'var(--s1)'}`},svg);
  if(r.hi!=null)el('path',{d:rightR(x(lo)+2,by,x(hi)-x(lo)-2,bh,3),style:`fill:${r.c2||'var(--s1-light)'}`},svg);
  txt(svg,x(hi)+6,by+bh/2+4,r.lbl,'fill:var(--ink);font:11.5px var(--f-mono)','start');
  const hit=el('rect',{x:0,y:by-6,width:W,height:bh+12,style:'fill:transparent'},svg);svg.insertBefore(hit,svg.firstChild);
  hit.addEventListener('mouseenter',()=>tip.show(`<b>${r.n}</b><br>${r.tip||r.lbl}`,x(hi),by));hit.addEventListener('mouseleave',()=>tip.hide())});
 (o.refs||[]).forEach((r,k)=>{const xx=x(r.v);el('line',{x1:xx,x2:xx,y1:m.t-10,y2:H-m.b,style:'stroke:var(--ink-2);stroke-width:1.5;stroke-dasharray:4 4'},svg);
  txt(svg,xx+(k%2?4:-4),m.t-14,r.label,'fill:var(--ink-2);font:11px var(--f-mono)',k%2?'start':'end')})})}
"""

HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>__CSS__</style></head>
<body><figure class="fig" id="fig"><h1>__TITLE__</h1><p class="cap">__CAP__</p><div class="chart" id="c"></div><div class="legend" id="lg"></div>__NOTE__<p class="src">Source: __SRC__</p></figure>
<script>__LIB__</script>
<script>
__JS__
</script></body></html>
"""

CHARTS = []
def chart(slug, title, cap, src, js, note=""):
    CHARTS.append((slug, title, cap, src, js, note))

# 01 Backing composition --------------------------------------------------------
chart("01-backing-composition", "USD3 backing by asset, $115.4M",
      "Share of pool backing on 5 Nov 2026. Hover a segment for the amount.",
      "app.3jane.xyz/info/backing (5 Nov 2026)",
      r"""
const data=[['Slope · forward flow',64.94,'var(--s1)'],['Settle · forward flow',27.45,'var(--s2)'],['Aave USDC (idle)',11.17,'var(--s3)'],['LendSwift · warehouse',6.59,'var(--s4)'],['Erebor bank cash',4.14,'var(--s5)'],['Crypto credit lines',1.08,'var(--s6)']];
const total=data.reduce((a,d)=>a+d[1],0);
legend(data.map(d=>({n:`${d[0]} · $${d[1].toFixed(1)}M · ${(100*d[1]/total).toFixed(1)}%`,c:d[2]})));
const box=document.getElementById('c');
observe(box,()=>{box.querySelectorAll('svg').forEach(s=>s.remove());const W=Math.max(300,box.clientWidth),H=78;const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,height:H,role:'img','aria-label':document.title},box);const tip=tipFor(box);
 let x=0;data.forEach((d,i)=>{const w=W*d[1]/total,g=i<data.length-1?2:0;const r=el('rect',{x,y:6,width:Math.max(1,w-g),height:42,rx:(i===0||i===data.length-1)?3:0,style:`fill:${d[2]}`},svg);
  if(w>70)txt(svg,x+6,66,`${(100*d[1]/total).toFixed(0)}%`,'fill:var(--ink-2);font:11.5px var(--f-mono)','start');
  const cx=x+w/2;r.addEventListener('mouseenter',()=>{r.style.opacity=.85;tip.show(`<b>${d[0]}</b><br>$${d[1].toFixed(2)}M · ${(100*d[1]/total).toFixed(1)}% of pool`,cx,6)});r.addEventListener('mouseleave',()=>{r.style.opacity=1;tip.hide()});x+=w})});
""", '<p class="note">80% of backing sits in two forward-flow books that 3Jane owns outright (Slope, Settle). Only LendSwift has a structural overcollateralization cushion.</p>')

# 02 Slope losses by quarter -------------------------------------------------------
chart("02-slope-losses-by-quarter", "Slope: realized net charge-offs by origination quarter",
      "% of originated principal, terminated loans only. 2026Q1 is 76% matured. “Eligible” = loans that pass 3Jane's forward-flow box.",
      "3Jane data room, Slope historical tape (5,080 loans, $260M, originations to 15 May 2026)",
      r"""
vbar({cats:['2025Q1','2025Q2','2025Q3','2025Q4','2026Q1*'],series:[{n:'All loans',v:[0,2.27,4.82,0.26,1.98],c:'var(--s1)'},{n:'Excl. 3 problem obligors',v:[0,0.07,0.38,0.27,0.52],c:'var(--s2)'},{n:'Eligible under 3Jane’s box',v:[0,0,0,0.01,0],c:'var(--s3)'}],
 yMax:6,ticks:4,yFmt:v=>v.toFixed(1)+'%',tipFmt:v=>v.toFixed(2)+'%',h:250});
legend([{n:'All loans · 1.72% lifetime',c:'var(--s1)'},{n:'Excl. 3 problem obligors · 0.27%',c:'var(--s2)'},{n:'Eligible under 3Jane’s box · 0.00%',c:'var(--s3)'}]);
""", '<p class="note">Losses were driven by a few large names: the top 20 obligors caused 81% of losses, and one manufacturer lost $2.9M (37.5% of its exposure). Recoveries were ~0%. 3Jane\'s box removes the lowest tiers and caps size by tier and merchant. Part of its zero-loss record comes from excluding early-payment defaults after the fact. The June 2026 sale agreement has no EPD putback, so that has to come from the forward-flow terms.</p>')

# 03 Slope repayment schedule --------------------------------------------------------
chart("03-slope-repayment-schedule", "Slope: scheduled cash coming back by month, $M",
      "Contractual principal and interest on the $63.5M book if 3Jane stopped buying. Label = cumulative share of principal repaid.",
      "app.3jane.xyz facility detail, Slope liquidity tab (as of 4 Nov 2026)",
      r"""
const cats=['Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul'];
const p=[22.8,22.5,10.7,4.0,1.9,0.74,0.45,0.28,0.07],f=[0.62,0.74,0.37,0.15,0.08,0.03,0.02,0.02,0.004];
let cum=0;const cp=p.map(v=>(cum+=v,cum/63.5*100));
vbar({cats,series:[{n:'Principal',v:p,c:'var(--s1)'},{n:'Interest & fees',v:f,c:'var(--s1-light)'}],stacked:true,yMax:25,ticks:5,yFmt:v=>'$'+v.toFixed(0),tipFmt:v=>'$'+v.toFixed(2)+'M',h:250,barFrac:0.6,
 top:{val:i=>p[i]+f[i],txt:i=>i<4?Math.round(cp[i])+'%':''},tipExtra:i=>`<br>Cumulative principal: ${cp[i].toFixed(0)}%`});
legend([{n:'Principal',c:'var(--s1)'},{n:'Interest & fees',c:'var(--s1-light)'}]);
""", '<p class="note">The forward flow is uncommitted, so 3Jane can stop buying at any time and the book runs off: ~42% of principal back in 30 days, 71% in 60, 89% in 90 and 99% in 180. The app currently labels the facility phase “Amortization”.</p>')

# 04 Settle loss drivers -------------------------------------------------------------
chart("04-settle-loss-drivers", "Settle: where historical losses come from",
      "Cumulative net loss, % of originated principal (obligor-size segments: 2023–25 large, 2024–25 mid-size). Lighter segment = reported range. Dashed lines = 3Jane's back-book expected loss and breakeven (% of balance).",
      "3Jane Settle back-book LP memo (21 Sep 2026), rebuilt from Settle loan-level records ($3.8B originated)",
      r"""
hbars({max:6,step:1,fmt:v=>v+'%',rows:[
 {n:'Large obligors ($10M+)',lo:0.2,hi:0.6,lbl:'0.2–0.6%'},
 {n:'2024 vintage',lo:1.45,lbl:'1.45%'},
 {n:'All originations since 2019',lo:1.5,lbl:'1.5%'},
 {n:'Never-deferred receivables',lo:1.5,lbl:'1.5%'},
 {n:'Mid-size obligors ($2–10M)',lo:4.5,hi:5.0,lbl:'4.5–5.0%',c:'var(--s2)',c2:'var(--s2-light)'},
 {n:'Receivables ever deferred',lo:5.4,lbl:'5.4%',c:'var(--s2)'}],
 refs:[{v:0.81,label:'3Jane EL 0.81%'},{v:2.3,label:'Breakeven 2.3%'}]});
legend([{n:'Loss rate',c:'var(--s1)'},{n:'High-loss segments',c:'var(--s2)'},{n:'Reference (back-book)',c:'var(--ink-2)',dash:true}]);
""", '<p class="note">Losses concentrate in mid-size obligors and anything that ever entered deferral. That\'s why 3Jane\'s purchase relies on whole-book obligor reps (no delinquency or forbearance anywhere at Settle), mandatory repurchase and an EPD putback. Per Jeremy, the largest obligors have historically performed best.</p>')

# 05 Settle repayment schedule ---------------------------------------------------------
chart("05-settle-repayment-schedule", "Settle: scheduled cash coming back by month, $M",
      "Contractual principal and interest on the $28.2M book if 3Jane stopped buying. Label = cumulative share of principal repaid.",
      "app.3jane.xyz facility detail, Settle liquidity tab (as of 27 Oct 2026)",
      r"""
const cats=['Oct*','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun'];
const p=[1.2,7.6,8.2,5.3,2.8,2.6,0.47,0.05,0.04],f=[0,0.37,0.29,0.15,0.07,0.04,0.01,0,0];
let cum=0;const cp=p.map(v=>(cum+=v,cum/28.25*100));
vbar({cats,series:[{n:'Principal',v:p,c:'var(--s2)'},{n:'Interest & fees',v:f,c:'var(--s2-light)'}],stacked:true,yMax:10,ticks:5,yFmt:v=>'$'+v.toFixed(0),tipFmt:v=>'$'+v.toFixed(2)+'M',h:250,barFrac:0.6,
 top:{val:i=>p[i]+f[i],txt:i=>(i>=1&&i<=5)?Math.round(cp[i])+'%':''},tipExtra:i=>`<br>Cumulative principal: ${cp[i].toFixed(0)}%`});
legend([{n:'Principal',c:'var(--s2)'},{n:'Interest & fees',c:'var(--s2-light)'}]);
""", '<p class="note">Longer than Slope (~70-day WAL, 109 days average remaining): ~26% of principal back in 30 days, 53% in 60, 74% in 90, ~100% in 180. *Oct = 27–31 Oct only. Also uncommitted, so 3Jane can stop buying at any time.</p>')

# 06 LendSwift borrowing base ------------------------------------------------------------
chart("06-lendswift-borrowing-base", "LendSwift: from pledged loans to 3Jane's coverage, $M",
      "Weekly borrowing-base test. Delinquent and short-paid loans are haircut out before the 33% overcollateralization (OC) test.",
      "app.3jane.xyz facility detail, LendSwift (as of 30 Oct 2026); pieces as reported and rounded",
      r"""
const steps=[{n:'Pledged loans',a:0,b:11.8,c:'var(--s1)',l:'11.8'},{n:'+ DACA cash',a:11.8,b:13.8,c:'var(--s1)',l:'2.0'},{n:'− >45 DPD (0% credit)',a:11.1,b:13.8,c:'var(--s2)',l:'2.7'},{n:'− 30–45 DPD (60% credit)',a:10.83,b:11.1,c:'var(--s2)',l:'0.27'},{n:'− Payment shortfall',a:9.4,b:10.83,c:'var(--s2)',l:'1.5'},{n:'Net collateral',a:0,b:9.4,c:'var(--s1)',l:'9.4'},{n:'Minimum at 33% OC',a:0,b:8.84,c:'var(--s1-light)',l:'8.84'},{n:'Owed to 3Jane',a:0,b:6.65,c:'var(--s3)',l:'6.65'}];
const tips=['Outstanding loan balance pledged to the SPV','Cash in the DACA-controlled collection account','Loans more than 45 days past due get zero credit','30–45 DPD loans get 60% credit','Last payment below 50% of schedule: zero credit','Eligible collateral after haircuts → OC 41.4%','1.33 × obligations; below this, all collections sweep to 3Jane','$6.56M note + $0.08M next coupon'];
const box=document.getElementById('c');
observe(box,()=>{box.querySelectorAll('svg').forEach(s=>s.remove());const W=Math.max(300,box.clientWidth),H=290,m={l:36,r:8,t:16,b:76},iw=W-m.l-m.r,ih=H-m.t-m.b,max=15,y=v=>m.t+ih-(v/max)*ih;
 const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,height:H,role:'img','aria-label':document.title},box);const tip=tipFor(box);
 [0,5,10,15].forEach(v=>{el('line',{x1:m.l,x2:W-m.r,y1:y(v),y2:y(v),style:'stroke:var(--rule-2)'},svg);txt(svg,m.l-6,y(v)+4,'$'+v,MONO,'end')});
 const band=iw/steps.length,bw=band*0.62;
 steps.forEach((s,i)=>{const x=m.l+i*band+(band-bw)/2,yt=y(s.b),hh=y(s.a)-y(s.b);
  const hit=el('rect',{x:m.l+i*band,y:m.t,width:band,height:ih,style:'fill:transparent'},svg);
  el('path',{d:s.a===0?topR(x,yt,bw,hh,3):`M${x},${yt}h${bw}v${hh}h${-bw}Z`,style:`fill:${s.c}`},svg);
  txt(svg,x+bw/2,yt-5,s.l,'fill:var(--ink-2);font:10.5px var(--f-mono)');
  const lx=x+bw/2,ly=m.t+ih+12;const t=txt(svg,lx,ly,s.n,'fill:var(--ink-3);font:10.5px var(--f-body)','end');t.setAttribute('transform',`rotate(-38 ${lx} ${ly})`);
  hit.addEventListener('mouseenter',()=>{hit.style.fill='var(--rule-2)';tip.show(`<b>${s.n}: $${s.l}M</b><br>${tips[i]}`,x+bw/2,yt)});hit.addEventListener('mouseleave',()=>{hit.style.fill='transparent';tip.hide()})});
 el('line',{x1:m.l,x2:W-m.r,y1:m.t+ih,y2:m.t+ih,style:'stroke:var(--ink-3)'},svg)});
legend([{n:'Collateral and coverage',c:'var(--s1)'},{n:'Haircuts',c:'var(--s2)'},{n:'Required minimum',c:'var(--s1-light)'},{n:'3Jane exposure',c:'var(--s3)'}]);
""", '<p class="note">3Jane loses its first dollar only after ~$7.2M of the $13.8M gross (loans + cash) is gone. Another ~$0.56M of haircuts would breach the 33% OC minimum. A breach stops new draws and sweeps all collections to 3Jane until OC is restored. A separate 3-month write-off trigger can stop funding even if the borrowing base is fine.</p>')

# 07 LendSwift DPD ----------------------------------------------------------------------------
chart("07-lendswift-delinquency", "LendSwift: days past due, share of pledged balance",
      "Current snapshot. Loans over 45 DPD already get zero borrowing-base credit.",
      "app.3jane.xyz facility detail, LendSwift performance tab (as of 30 Oct 2026)",
      r"""
const v=[59.4,9.6,16.0,13.7,0.8,0.5];
vbar({cats:['≤15','16–30','31–60','61–90','91–120','121+'],series:[{n:'Share of balance',v,c:'var(--s1)',cf:i=>i<2?'var(--s1)':'var(--s2)'}],yMax:80,ticks:4,yFmt:v=>v.toFixed(0)+'%',tipFmt:v=>v.toFixed(1)+'%',h:240,top:{val:i=>v[i],txt:i=>v[i].toFixed(1)+'%'},tipCat:c=>c+' days past due'});
legend([{n:'Current or ≤30 DPD (full credit)',c:'var(--s1)'},{n:'31+ DPD (haircut)',c:'var(--s2)'}]);
""", '<p class="note">31+ DPD has sat in a 25–33% band every week since the facility closed in May. That is normal for ~690% APR emergency loans and already priced in. Very little reaches 91+, so loans are charged off or cured around 90 days. Delinquent loans leave the borrowing base quickly through the haircuts.</p>')

# 08 LendSwift collections by vintage ------------------------------------------------------------
chart("08-lendswift-collections-by-vintage", "LendSwift: cash collected by vintage, % of loan amount",
      "Monthly origination vintages, Jan 2024 to Oct 2026. 100% = all cash lent has come back. Lighter bars are still collecting.",
      "app.3jane.xyz facility detail, LendSwift performance tab (as of 30 Oct 2026); LendSwift vintage file",
      r"""
const vals=[141.9,133.8,128.7,115.2,127.2,130.4,122.9,128.0,133.1,126.8,126.5,132.2,133.2,140.5,131.5,122.1,123.5,120.6,121.6,123.7,129.0,134.7,131.0,133.6,142.0,138.7,124.3,119.0,112.4,111.4,105.2,87.7,59.0,20.1];
const cats=[];for(let y=2024,mo=1;cats.length<vals.length;){cats.push(`${y}-${String(mo).padStart(2,'0')}`);if(++mo>12){mo=1;y++}}
const young=i=>i>=vals.length-4;
vbar({cats,series:[{n:'Collected',v:vals,c:'var(--s1)',cf:i=>young(i)?'var(--s1-light)':'var(--s1)'}],yMax:160,ticks:4,yFmt:v=>v.toFixed(0)+'%',tipFmt:v=>v.toFixed(1)+'% of loan amount',labelEvery:6,barFrac:0.78,h:250,
 catFmt:c=>c.slice(2).replace('-','/'),tipExtra:i=>young(i)?'<br>Still collecting':'',refs:[{v:100,label:'100% = cash back'}]});
legend([{n:'Seasoned vintage',c:'var(--s1)'},{n:'Still collecting (≤3 months)',c:'var(--s1-light)'},{n:'Break-even',c:'var(--ink-2)',dash:true}]);
""", '<p class="note">Seasoned vintages return 120–141% of the loan amount (~150% of new cash funded), against a 75% advance rate. That cash multiple is the metric 3Jane watches most. Apr–May 2026, the first vintages under 3Jane\'s line, project to ~117–121%: still cash-positive, but at the low end of the range.</p>')

# 09 LendSwift payoff schedule ---------------------------------------------------------------------
chart("09-lendswift-payoff-schedule", "LendSwift: pledged loans by anticipated payoff month, $M",
      "$11.8M of collateral. In normal operation collections recycle into new loans until May 2027. After a trigger, they sweep to 3Jane.",
      "app.3jane.xyz facility detail, LendSwift liquidity tab (as of 30 Oct 2026)",
      r"""
const cats=['Past due','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May+'],v=[1.0,0.09,0.57,1.2,1.7,2.4,2.5,2.2,0.11],pc=[8.7,0.8,4.8,9.9,14.4,20.1,21.5,18.9,0.9];
vbar({cats,series:[{n:'Collateral due',v,c:'var(--s4)',cf:i=>i===0?'var(--s2)':'var(--s4)'}],yMax:3,ticks:3,yFmt:v=>'$'+v.toFixed(0),tipFmt:v=>'$'+v.toFixed(2)+'M',h:240,barFrac:0.6,top:{val:i=>v[i],txt:i=>pc[i].toFixed(0)+'%'}});
legend([{n:'Scheduled payoff (Oct 2026 → 2027)',c:'var(--s4)'},{n:'Already past due',c:'var(--s2)'}]);
""", '<p class="note">If collections were swept, the $2.0M of cash plus scheduled principal alone would cover the $6.65M owed by about Feb 2027, before counting interest and fees at ~690% APR. The facility\'s own term is 12 months revolving to May 2027, then 6 months amortization to Nov 2027.</p>')

# 10 Pool liquidity ladder ------------------------------------------------------------------------------
chart("10-pool-liquidity-ladder", "USD3 pool: cumulative cash if 3Jane stops buying, $M",
      "Liquidity sleeve (Aave + Erebor) today plus scheduled principal from Slope and Settle. LendSwift excluded. Labels = % of the $115M pool.",
      "app.3jane.xyz backing and facility liquidity tabs (27 Oct to 5 Nov 2026); Re7 calculation",
      r"""
vbar({cats:['Today','30 days','60 days','90 days','180 days'],series:[{n:'Liquidity sleeve',v:[15.3,15.3,15.3,15.3,15.3],c:'var(--s3)'},{n:'Slope repaid',v:[0,26.6,45.3,56.6,62.7],c:'var(--s1)'},{n:'Settle repaid',v:[0,7.2,14.9,20.8,28.1],c:'var(--s2)'}],
 stacked:true,yMax:120,ticks:4,yFmt:v=>'$'+v.toFixed(0),tipFmt:v=>'$'+v.toFixed(1)+'M',h:260,barFrac:0.55,refs:[{v:115,label:'Pool $115M',left:true}],
 top:{val:i=>[15.3,49.2,75.6,92.7,106.1][i],txt:i=>['13%','43%','66%','80%','92%'][i]}});
legend([{n:'Liquidity sleeve (target 15%)',c:'var(--s3)'},{n:'Slope principal repaid',c:'var(--s1)'},{n:'Settle principal repaid',c:'var(--s2)'},{n:'Pool size',c:'var(--ink-2)',dash:true}]);
""", '<p class="note">Assumes borrowers pay on schedule and no redeployment. Both forward flows are uncommitted, so stopping purchases is 3Jane\'s call. The sleeve is shared by USD3 and sUSD3; sUSD3 exits through USD3. Primary redemption needs no KYC.</p>')

# 11 LCC scenarios ------------------------------------------------------------------------------------------
chart("11-lcc-private-deal-scenarios", "LCC private deal: annualized return on deployed capital",
      "Per $1M commitment ($75k margin), ~90-day term. Hard USD vs JANE. Called USD3 earns the fixed 18% for 70 days, then exits.",
      "Trenches LCC LP Deal terms; USD3 organic yield 6.3%; Aave 4%; Re7 calculation",
      r"""
const hard=[16.0,7.3,6.5,7.1],jane=[18.0,12.4,11.8,12.2],usd=[6288,21138,35988,40389],cap=['$75k for 90d','$75k→$37.5k + $500k for 70d','$75k for 21d + $1M for 70d','$75k for 84d + $1M for 70d'];
vbar({cats:['No call','50% called, window 1','Fully called, window 1','Fully called, window 4'],series:[{n:'Hard USD',v:hard,c:'var(--s1)'},{n:'JANE',v:jane,c:'var(--s4)'}],stacked:true,yMax:40,ticks:4,yFmt:v=>v.toFixed(0)+'%',tipFmt:v=>v.toFixed(1)+'%',h:300,barFrac:0.5,mr:44,
 catSub:i=>(hard[i]+jane[i]).toFixed(1)+'% total',refs:[{v:12,label:'12%',outside:true},{v:20,label:'20%',outside:true}],
 tipExtra:i=>`<br>Income: $${usd[i].toLocaleString('en-US')}<br>Capital: ${cap[i]}`});
legend([{n:'Hard USD (Aave + USDC fee, USD3 organic)',c:'var(--s1)'},{n:'JANE (valued at 3-day TWAP after TGE)',c:'var(--s4)'},{n:'Hurdles: 12% standard, 20% private deals',c:'var(--ink-2)',dash:true}]);
""", '<p class="note">Uncalled, the margin earns ~34%, of which 16% is hard USD. Once called, the position is mostly $1M of USD3 at a fixed 18% for 70 days, of which only ~6.3% is organic and the rest a JANE top-up. Calls pull the blended return toward ~18–20%, below the 20% private-deal hurdle. Halving the JANE value takes the called cases to ~12–13%.</p>')

for slug, title, cap, src, js, note in CHARTS:
    html = (HEAD.replace("__CSS__", CSS).replace("__LIB__", LIB).replace("__JS__", js)
            .replace("__TITLE__", title).replace("__CAP__", cap).replace("__SRC__", src).replace("__NOTE__", note))
    (OUT / f"{slug}.html").write_text(html)
print(len(CHARTS), "charts written to", OUT)
