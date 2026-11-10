"""Kamino Main Market USDC reserve: rate spike after the 29 Oct 2026 Binance incident.
Data: api.kamino.finance reserve metrics history (hourly), saved in raw_kamino_usdc_hourly.json.
"""
import json, collections, datetime as dt
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

HERE = Path(__file__).parent
BORROW, SUPPLY = "#2a78d6", "#eb6834"
INK, INK2, MUTED, GRID, EVENT = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0", "#e34948"
EVENT_T = dt.datetime(2026, 10, 29, 21, 30)  # rates jump at the 22:00 UTC print

rows = []
for x in json.load(open(HERE / "raw_kamino_usdc_hourly.json"))["history"]:
    t = dt.datetime.fromisoformat(x["timestamp"].replace("Z", "")).replace(second=0, microsecond=0)
    m = x["metrics"]
    rows.append((t, 100 * m["borrowInterestAPY"], 100 * m["supplyInterestAPY"]))

def style(ax, title):
    ax.set_title(title, loc="left", fontsize=13, color=INK, fontweight="bold", pad=10)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    ax.tick_params(colors=INK2, labelsize=10, length=0)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.set_ylim(0, 50)

def event(ax, ytxt=47, side="right"):
    ax.axvline(EVENT_T, color=EVENT, lw=1.5, ls="--")
    txt = "  Binance incident\n  29 oct" if side == "right" else "Binance incident  \n29 oct  "
    ax.text(EVENT_T, ytxt, txt, color=EVENT, fontsize=10, fontweight="bold", va="top",
            ha="left" if side == "right" else "right", multialignment="left" if side == "right" else "right")

def daily(ax):
    d = collections.defaultdict(list)
    for t, b, s in rows:
        if dt.datetime(2026, 10, 1) <= t < dt.datetime(2026, 11, 1): d[t.date()].append((b, s))
    days = sorted(d)
    x = [dt.datetime.combine(k, dt.time(12)) for k in days]
    b = [sum(v[0] for v in d[k]) / len(d[k]) for k in days]
    s = [sum(v[1] for v in d[k]) / len(d[k]) for k in days]
    ax.plot(x, b, color=BORROW, lw=2, marker="o", ms=3.5, label="Borrow APY")
    ax.plot(x, s, color=SUPPLY, lw=2, marker="o", ms=3.5, label="Supply APY")
    i = max(range(len(b)), key=b.__getitem__)
    ax.annotate(f"{b[i]:.1f}%", (x[i], b[i]), xytext=(-8, 6), textcoords="offset points",
                ha="right", fontsize=10, color=INK, fontweight="bold")
    ax.annotate(f"{s[i]:.1f}%", (x[i], s[i]), xytext=(-8, -4), textcoords="offset points",
                ha="right", va="top", fontsize=10, color=INK2)
    style(ax, "Diario · media diaria, 1–31 oct 2026")
    ax.set_xlim(dt.datetime(2026, 10, 1), dt.datetime(2026, 11, 1))
    ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=[1, 8, 15, 22, 29]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d oct"))
    event(ax)

def week(ax):
    sel = [r for r in rows if dt.datetime(2026, 10, 25) <= r[0] < dt.datetime(2026, 11, 1)]
    x = [r[0] for r in sel]; b = [r[1] for r in sel]; s = [r[2] for r in sel]
    ax.plot(x, b, color=BORROW, lw=2, label="Borrow APY")
    ax.plot(x, s, color=SUPPLY, lw=2, label="Supply APY")
    i = max(range(len(b)), key=b.__getitem__)
    ax.annotate(f"Pico {b[i]:.1f}%", (x[i], b[i]), xytext=(8, 2), textcoords="offset points",
                fontsize=10, color=INK, fontweight="bold")
    ax.annotate(f"{s[i]:.1f}%", (x[i], s[i]), xytext=(8, -10), textcoords="offset points",
                fontsize=10, color=INK2)
    ax.annotate("Pre-evento ~6%", (dt.datetime(2026, 10, 29, 2), b[98]), xytext=(0, 26),
                textcoords="offset points", ha="center", fontsize=10, color=INK2)
    style(ax, "7 días · horario, 25–31 oct 2026")
    ax.set_xlim(dt.datetime(2026, 10, 25), dt.datetime(2026, 11, 1))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d oct"))
    event(ax, side="left")

def finish(fig, ax_legend):
    ax_legend.legend(loc="upper left", bbox_to_anchor=(0, 0.86), frameon=False, fontsize=10,
                     labelcolor=INK2)
    fig.text(0.01, 0.01, "Fuente: Kamino API · Main Market, reserve USDC (D6q6…gJ59). Horas en UTC.",
             fontsize=8.5, color=MUTED)

SUP = "Kamino USDC (Main Market): los tipos se disparan tras el Binance incident"
fig, axes = plt.subplots(1, 2, figsize=(14, 5.6), dpi=200)
fig.suptitle(SUP, x=0.01, ha="left", fontsize=15, color=INK, fontweight="bold")
daily(axes[0]); week(axes[1]); finish(fig, axes[0])
fig.tight_layout(rect=(0, 0.03, 1, 0.95)); fig.savefig(HERE / "kamino_usdc_binance_incident.png")

for name, fn in (("daily", daily), ("7d", week)):
    f, a = plt.subplots(figsize=(9, 5.2), dpi=200)
    f.suptitle(SUP, x=0.01, ha="left", fontsize=12.5, color=INK, fontweight="bold")
    fn(a); finish(f, a)
    f.tight_layout(rect=(0, 0.03, 1, 0.95)); f.savefig(HERE / f"kamino_usdc_binance_incident_{name}.png")
