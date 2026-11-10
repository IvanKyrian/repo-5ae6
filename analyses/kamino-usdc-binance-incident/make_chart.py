"""Kamino Main Market USDC reserve: supply APY spike after the 29 Oct 2026 Binance incident.
Data: api.kamino.finance reserve metrics history (hourly), saved in raw_kamino_usdc_hourly.json.
"""
import json, datetime as dt
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

HERE = Path(__file__).parent
LINE, INK, INK2, MUTED, GRID, EVENT = "#eb6834", "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0", "#e34948"
START, END = dt.datetime(2026, 10, 29), dt.datetime(2026, 10, 31)
EVENT_T = dt.datetime(2026, 10, 29, 21, 30)          # rates jump at the 22:00 UTC print
SPIKE = (dt.datetime(2026, 10, 29, 22), dt.datetime(2026, 10, 30, 20))  # elevated-rate window

pts = []
for x in json.load(open(HERE / "raw_kamino_usdc_hourly.json"))["history"]:
    t = dt.datetime.fromisoformat(x["timestamp"].replace("Z", "")).replace(second=0, microsecond=0)
    if START <= t <= END:
        pts.append((t, 100 * x["metrics"]["supplyInterestAPY"]))
t, y = zip(*pts)
spike = [v for ti, v in pts if SPIKE[0] <= ti <= SPIKE[1]]
peak_i = max(range(len(y)), key=y.__getitem__)
avg = sum(spike) / len(spike)
print(f"max {y[peak_i]:.1f}% at {t[peak_i]}, avg {avg:.1f}% over {len(spike)}h, pre-event {y[0]:.1f}%")

fig, ax = plt.subplots(figsize=(10, 5.4), dpi=200)
ax.plot(t, y, color=LINE, lw=2.2)
ax.hlines(avg, *SPIKE, color=INK2, lw=1.2, ls=":")
ax.text(SPIKE[1], avg, f"  Avg {avg:.1f}%", color=INK2, fontsize=11, va="center")
ax.annotate(f"Max {y[peak_i]:.1f}%", (t[peak_i], y[peak_i]), xytext=(8, 4),
            textcoords="offset points", fontsize=11, color=INK, fontweight="bold")
ax.text(START + dt.timedelta(hours=1), y[0] + 1.5, f"Pre-event ~{y[0]:.1f}%", color=INK2, fontsize=11)
ax.axvline(EVENT_T, color=EVENT, lw=1.5, ls="--")
ax.text(EVENT_T, 47, "Binance incident  \n29 Oct  ", color=EVENT, fontsize=11,
        fontweight="bold", va="top", ha="right", multialignment="right")

ax.set_title("Kamino USDC (Main Market) supply APY after the Binance incident",
             loc="left", fontsize=14, color=INK, fontweight="bold", pad=12)
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(MUTED)
ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
ax.tick_params(colors=INK2, labelsize=10, length=0)
ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
ax.set_ylim(0, 50); ax.set_xlim(START, END)
ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 6, 12, 18]))
ax.xaxis.set_major_formatter(lambda v, _: mdates.num2date(v).strftime("%d Oct %H:%M"))
fig.text(0.01, 0.01, f"Hourly data, UTC. Avg = mean supply APY over the elevated window "
         f"(29 Oct 22:00 – 30 Oct 20:00). Source: Kamino API.", fontsize=8.5, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(HERE / "kamino_usdc_supply_apy_binance_incident.png")
