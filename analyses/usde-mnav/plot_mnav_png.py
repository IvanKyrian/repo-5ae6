"""Static PNG of the USDE mNAV history with the Friday 20 Nov 2026 sell-off highlighted."""
import csv, datetime as dt
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

HERE = Path(__file__).parent
rows = list(csv.DictReader(open(HERE / "usde_mnav_daily.csv")))
d = [dt.date.fromisoformat(r["date"]) for r in rows]
m = [float(r["mnav"]) for r in rows]
px = {r["date"]: float(r["usde_close"]) for r in rows}
ena = {r["date"]: float(r["ena_price_at_nasdaq_close"]) for r in rows}
avg = sum(m) / len(m)

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, RED = "#2a78d6", "#e34948"
FRI, THU = "2026-11-20", "2026-11-19"
i_f, i_t = d.index(dt.date.fromisoformat(FRI)), d.index(dt.date.fromisoformat(THU))
i_max, i_min, last = m.index(max(m)), m.index(min(m)), len(m) - 1

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
fig, ax = plt.subplots(figsize=(11, 5.6), dpi=200)
fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)

# Friday highlight band (Thursday close -> Friday close)
ax.axvspan(d[i_t] + dt.timedelta(hours=12), d[i_f] + dt.timedelta(hours=12), color=RED, alpha=0.14, lw=0, zorder=0)
ax.axvline(dt.date(2026, 10, 5), color=INK2, lw=1, alpha=0.5, zorder=1)
ax.text(dt.date(2026, 10, 5), 0.585, " Lock-ups off (5 Oct)", color=INK2, fontsize=9, va="center")
ax.axhline(avg, color=INK2, lw=1, ls=(0, (4, 3)), alpha=0.6, zorder=1)
ax.text(d[0], avg + 0.008, f"Average since listing {avg:.2f}x", color=INK2, fontsize=9)

ax.plot(d, m, color=BLUE, lw=2, solid_joinstyle="round", zorder=3)
ax.plot([d[i_t], d[i_f]], [m[i_t], m[i_f]], color=RED, lw=2.6, zorder=4)

def dot(i, color):
    ax.scatter([d[i]], [m[i]], s=46, color=color, edgecolor=SURF, linewidth=2, zorder=5)

for i in (i_max, i_min, last):
    dot(i, INK)
dot(i_f, RED)
ax.annotate(f"Max {m[i_max]:.2f}x", (d[i_max], m[i_max]), xytext=(6, 8), textcoords="offset points", fontsize=9, color=INK, weight="bold")
ax.annotate(f"Min {m[i_min]:.2f}x", (d[i_min], m[i_min]), xytext=(6, -14), textcoords="offset points", fontsize=9, color=INK, weight="bold")
ax.annotate(f"Today\n{m[last]:.2f}x", (d[last], m[last]), xytext=(8, -4), textcoords="offset points", fontsize=9, color=INK, weight="bold", ha="left", va="center")

pu = px[FRI] / px[THU] - 1; pe = ena[FRI] / ena[THU] - 1
ax.annotate(f"Fri 20 Nov sell-off\nUSDE {pu:+.0%} (\\${px[THU]:.2f} → \\${px[FRI]:.2f})\nENA {pe:+.0%}\nmNAV {m[i_t]:.2f}x → {m[i_f]:.2f}x",
            (d[i_f], m[i_f]), xytext=(-150, -78), textcoords="offset points", fontsize=9, color=INK,
            arrowprops=dict(arrowstyle="-", color=RED, lw=1),
            bbox=dict(boxstyle="round,pad=0.4", fc=SURF, ec=RED, lw=1))

ax.set_ylim(0, 0.62)
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.1f}x"))
ax.xaxis.set_major_locator(mdates.MonthLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.set_xlim(d[0] - dt.timedelta(days=2), d[-1] + dt.timedelta(days=9))
ax.grid(axis="y", color=GRID, lw=1); ax.set_axisbelow(True)
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#c3c2b7")
ax.tick_params(colors=MUTED, length=0, labelsize=9)

fig.text(0.06, 0.95, "USDE mNAV since listing", fontsize=15, weight="bold", color=INK)
fig.text(0.06, 0.905, f"mNAV = (USDE price × 24,029,576 shares) ÷ (3,031,404,421 ENA × ENA price), daily at the Nasdaq close. "
         f"26 Jun – {d[-1].day} {d[-1]:%b} 2026, last point intraday.", fontsize=9, color=INK2)
fig.text(0.06, 0.02, "Sources: Nasdaq daily close via Yahoo Finance; ENA = Hyperliquid perp at 4pm New York; share count and ENA held from the Q3 2026 results and Q2 10-Q.",
         fontsize=8, color=MUTED)
fig.subplots_adjust(left=0.06, right=0.98, top=0.86, bottom=0.1)
out = HERE / "charts" / "usde-mnav-friday-selloff.png"
fig.savefig(out, facecolor=SURF)
print(out)
