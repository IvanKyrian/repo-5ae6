"""Loss ladder, Slope full-history case: same 3Jane model, Slope base loss = 1.72% per loan
x 365/55.6-day WAL = 11.3%/yr (vs 3Jane's 3.57%); Settle unchanged at 4.63%.
Today's yields still price only 3Jane's $4.16M base, so the extra loss eats yield first."""
import importlib.util, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location('v2', Path(__file__).parent.parent / 'charts-v2' / 'build.py')
v2 = importlib.util.module_from_spec(spec); sys.modules['v2'] = v2; spec.loader.exec_module(v2)
M = v2.M
SLOPE, SETTLE = 57177180.22, 45656690.4
SLOPE_RATE = 0.0172 * 365 / 55.6
BASE = SLOPE * SLOPE_RATE + SETTLE * 0.04631108661910292
BOOK = SLOPE + SETTLE
def ladder(m):
    extra = m * BASE - M['base']
    if extra <= M['G']:
        f = 1 - max(extra, 0) / M['G']; return M['yU'] * f, M['yS'] * f
    burn = extra - M['G']
    return -max(0.0, burn - M['s']) / M['senior'], -min(1.0, burn / M['s'])
mults = [1, 1.25, 1.5, 2, 2.5, 3, 4, 5]
rows = ",".join(f"{{lab:'{m:g}×',rate:'{m*BASE/BOOK*100:.0f}%',u:{ladder(m)[0]:.5f},s:{ladder(m)[1]:.5f}}}" for m in mults)
yz = (M['G'] + M['base']) / BASE; uh = (M['G'] + M['s'] + M['base']) / BASE
OUT = Path(__file__).parent
v2.OUT = OUT
v2.page("03-loss-ladder-slope-full-history", "Loss ladder: Slope at its full historical loss rate",
    f"Same 3Jane model, but Slope's expected loss set to its full history (~11.3% a year, incl. the three large defaults) instead of 3.6%. Settle unchanged at 4.6%. Labels: multiple and annual loss rate on the $103M book.",
    f"At 1× ({BASE/1e6:.1f}M a year, {100*BASE/BOOK:.1f}% of the book) yields already fall to ~{ladder(1)[0]*100:.1f}% (USD3) and ~{ladder(1)[1]*100:.1f}% (sUSD3). "
    f"Yields reach zero at {yz:.2f}× and USD3 principal is first hit at {uh:.2f}× ({uh*BASE/BOOK*100:.0f}% of the book lost in a year).",
    "3Jane USD3/sUSD3 stress model (16 Nov 2026) with Slope's loss rate from the Slope data room (1.72% per loan, ~55-day loans); Re7 calculation",
    f"ladderChart({{rows:[{rows}],xTitle:'Multiple of the full-history loss rate · annual loss rate on the book'}});")
if __name__ == '__main__':
    print('Slope rate %.2f%%, base $%.2fM = %.2f%% of book' % (SLOPE_RATE*100, BASE/1e6, BASE/BOOK*100))
    print('yields zero at %.2fx, USD3 hit at %.2fx (%.1f%% of book)' % (yz, uh, uh*BASE/BOOK*100))
    for m in mults:
        u, s = ladder(m); print('%gx  %.1f%%  USD3 %+.1f%%  sUSD3 %+.1f%%' % (m, m*BASE/BOOK*100, u*100, s*100))
