// Shared multi-panel time-series chart: synced crosshair, one tooltip, keyboard support.
function makeChart(root, opts) {
  const NS = 'http://www.w3.org/2000/svg';
  const host = root.querySelector('.plot');
  const tip = root.querySelector('.tip');
  const n = opts.dates.length;
  const MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  let svg, geo, cur = null, raf = 0;

  function el(tag, attrs, parent, style) {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (style) Object.assign(e.style, style);
    if (parent) parent.appendChild(e);
    return e;
  }
  function txt(parent, x, y, s, cls, anchor) {
    const t = el('text', { x, y, class: cls, 'text-anchor': anchor || 'start' }, parent);
    t.textContent = s;
    return t;
  }
  function nice(lo, hi, count) {
    const raw = (hi - lo) / count;
    const mag = Math.pow(10, Math.floor(Math.log10(raw)));
    const r = raw / mag;
    const step = (r >= 7.5 ? 10 : r >= 3.5 ? 5 : r >= 1.5 ? 2 : 1) * mag;
    const a = Math.floor(lo / step) * step, b = Math.ceil(hi / step) * step;
    const ticks = [];
    for (let v = a; v <= b + step / 2; v += step) ticks.push(+v.toFixed(10));
    return { lo: a, hi: b, ticks };
  }
  function fmtDate(d) { return d.getUTCDate() + ' ' + MON[d.getUTCMonth()] + ' ' + d.getUTCFullYear(); }

  function draw() {
    host.querySelectorAll('svg').forEach(s => s.remove());
    const W = Math.max(300, host.clientWidth);
    const narrow = W < 520;
    const padL = 46, padR = opts.padR || 14, strip = opts.strip ? 30 : 0, labH = 18, gapP = 14, axisH = 24;
    let H = strip + axisH + 4;
    opts.panels.forEach((p, i) => { H += labH + p.h + (i ? gapP : 0); });
    svg = el('svg', { width: W, height: H, viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': opts.aria, tabindex: 0 }, host);
    const plotW = W - padL - padR, step = plotW / (n - 1);
    const X = i => padL + i * step;
    const panels = [];
    let y = strip;
    opts.panels.forEach((p, pi) => {
      if (pi) y += gapP;
      const ly = y + 12; y += labH;
      const vals = [];
      p.series.forEach(s => s.values().forEach(v => { if (v != null && isFinite(v)) vals.push(v); }));
      let lo = Math.min(...vals), hi = Math.max(...vals);
      if (p.zero) { lo = Math.min(lo, 0); hi = Math.max(hi, 0); }
      const pad = (hi - lo) * 0.05; hi += pad; if (!p.zero || lo < 0) lo -= pad;
      const t = nice(lo, hi, narrow ? 3 : (p.ticks || 4));
      const y0 = y, Y = v => y0 + p.h - (v - t.lo) / (t.hi - t.lo) * p.h;
      panels.push({ p, Y, t, ly });
      y += p.h;
    });
    const top = strip, bottom = y;
    geo = { X, panels, top, bottom, W, padL, padR, step };

    // shaded periods span every panel; their labels sit in the strip on top
    (opts.bands || []).forEach(b => {
      const x1 = X(b.i0) - step / 2, x2 = X(b.i1) + step / 2;
      if (b.i0 === b.i1) el('line', { x1: X(b.i0), x2: X(b.i0), y1: top, y2: bottom }, svg, { stroke: 'var(--ink-2)', strokeWidth: 1.5, opacity: 0.55 });
      else el('rect', { x: x1, y: top, width: Math.max(2, x2 - x1), height: bottom - top }, svg, { fill: 'var(--band)' });
      if (b.label) {
        const mid = (x1 + x2) / 2, ty = 11 + (b.row || 0) * 14;
        let anchor = 'middle', tx = mid;
        if (mid > W - padR - 70) { anchor = 'end'; tx = Math.min(x2, W - padR); }
        else if (mid < padL + 40) { anchor = 'start'; tx = Math.max(x1, 2); }
        txt(svg, tx, ty, narrow && b.short ? b.short : b.label, 'note', anchor);
      }
    });

    // grid, ticks and marks per panel
    panels.forEach(pp => {
      const { p, Y, t, ly } = pp;
      txt(svg, padL, ly, p.label, 'plabel');
      t.ticks.forEach(v => {
        const yy = Y(v);
        el('line', { x1: padL, x2: W - padR, y1: yy, y2: yy }, svg, { stroke: v === 0 && p.zero ? 'var(--axis)' : 'var(--grid)', strokeWidth: 1 });
        txt(svg, padL - 6, yy + 4, p.tick(v).replace('-', '\u2212'), 'tick', 'end');
      });
      p.series.forEach(s => {
        const arr = s.values();
        if (s.type === 'bar') {
          const bw = Math.max(1, step * 0.7);
          arr.forEach((v, i) => {
            if (v == null || v === 0) return;
            const a = Y(Math.max(v, 0)), b = Y(Math.min(v, 0));
            el('rect', { x: X(i) - bw / 2, y: a, width: bw, height: Math.max(0.75, b - a) }, svg, { fill: s.color(v) });
          });
        } else {
          let d = '';
          arr.forEach((v, i) => { if (v != null) d += (d ? 'L' : 'M') + X(i).toFixed(1) + ',' + Y(v).toFixed(1); });
          el('path', { d }, svg, { fill: 'none', stroke: s.color, strokeWidth: s.width || 2, strokeOpacity: s.opacity || 1, strokeLinejoin: 'round', strokeLinecap: 'round' });
        }
      });
      (p.marks || []).forEach(m => {
        const v = m.value(), cx = X(m.i), cy = Y(v);
        el('circle', { cx, cy, r: 4 }, svg, { fill: 'var(--ink)', stroke: 'var(--bg)', strokeWidth: 2 });
        const right = cx < W * 0.6;
        txt(svg, cx + (right ? 9 : -9), cy + (m.dy || 4), narrow && m.short ? m.short : m.label, 'note strong', right ? 'start' : 'end');
      });
    });

    // x axis: first day of each month
    const ay = bottom + 16;
    let lastX = -1e9;
    opts.dates.forEach((d, i) => {
      if (d.getUTCDate() !== 1) return;
      const x = X(i);
      el('line', { x1: x, x2: x, y1: bottom, y2: bottom + 4 }, svg, { stroke: 'var(--axis)', strokeWidth: 1 });
      if (x - lastX < (narrow ? 34 : 28)) return;
      txt(svg, x, ay, MON[d.getUTCMonth()], 'tick', 'middle'); lastX = x;
    });

    // crosshair layer
    const g = el('g', { 'pointer-events': 'none' }, svg);
    const vline = el('line', { y1: top, y2: bottom }, g, { stroke: 'var(--ink-2)', strokeWidth: 1, opacity: 0 });
    const dots = [];
    panels.forEach(({ p, Y }) => p.series.forEach(s => {
      if (s.type === 'bar') return;
      dots.push({ s, Y, c: el('circle', { r: 4 }, g, { fill: s.color, stroke: 'var(--bg)', strokeWidth: 2, opacity: 0 }) });
    }));
    geo.vline = vline; geo.dots = dots;
    const hit = el('rect', { x: padL - step / 2, y: top, width: plotW + step, height: bottom - top }, svg, { fill: 'transparent' });
    hit.addEventListener('pointermove', e => { const r = svg.getBoundingClientRect(); show(Math.round((e.clientX - r.left - padL) / step)); });
    hit.addEventListener('pointerleave', hide);
    svg.addEventListener('focus', () => show(cur == null ? n - 1 : cur));
    svg.addEventListener('blur', hide);
    svg.addEventListener('keydown', e => {
      const k = { ArrowLeft: -1, ArrowRight: 1 }[e.key];
      if (k) { e.preventDefault(); show((cur == null ? n - 1 : cur) + k * (e.shiftKey ? 7 : 1)); }
      if (e.key === 'Escape') hide();
    });
    if (cur != null && root.dataset.active === '1') show(cur);
  }

  function show(i) {
    i = Math.max(0, Math.min(n - 1, i)); cur = i; root.dataset.active = '1';
    const x = geo.X(i);
    geo.vline.setAttribute('x1', x); geo.vline.setAttribute('x2', x); geo.vline.style.opacity = 0.5;
    geo.dots.forEach(({ s, Y, c }) => {
      const v = s.values()[i];
      if (v == null) { c.style.opacity = 0; return; }
      c.setAttribute('cx', x); c.setAttribute('cy', Y(v)); c.style.opacity = 1;
    });
    tip.replaceChildren();
    const h = document.createElement('div'); h.className = 'tip-date'; h.textContent = fmtDate(opts.dates[i]); tip.appendChild(h);
    opts.tooltip(i).forEach(r => {
      const row = document.createElement('div'); row.className = 'tip-row' + (r.sep ? ' sep' : '');
      const key = document.createElement('span'); key.className = 'key' + (r.key ? '' : ' blank');
      if (r.key) key.style.background = r.key;
      const v = document.createElement('strong'); v.textContent = r.value;
      const l = document.createElement('span'); l.className = 'tip-label'; l.textContent = r.label;
      row.append(key, v, l); tip.appendChild(row);
    });
    tip.hidden = false;
    const tw = tip.offsetWidth, hw = host.clientWidth;
    let left = x + 14; if (left + tw > hw - 4) left = x - 14 - tw; if (left < 4) left = 4;
    tip.style.left = left + 'px'; tip.style.top = (geo.top + 6) + 'px';
  }
  function hide() {
    root.dataset.active = '0'; tip.hidden = true;
    if (!geo) return;
    geo.vline.style.opacity = 0; geo.dots.forEach(d => d.c.style.opacity = 0);
  }

  new ResizeObserver(() => { cancelAnimationFrame(raf); raf = requestAnimationFrame(draw); }).observe(host);
  draw();
  return { redraw: draw };
}
