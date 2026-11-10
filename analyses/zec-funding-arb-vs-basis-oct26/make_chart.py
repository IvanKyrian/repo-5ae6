"""ZEC funding arb (short Hyperliquid / long Binance) vs BTC price, October 2026.
Funding: ../zec-binance-hyperliquid/zec_daily.csv (daily funding, annualized x365).
BTC: Hyperliquid BTC perp daily closes (btc_daily_hl.json).
"""
import csv, json, datetime as dt
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

HERE = Path(__file__).parent
HL, BIN, SPREAD = "#2a78d6", "#eb6834", "#1baf7a"
BTC, INK, INK2, MUTED, GRID = "#8a8984", "#0b0b0b", "#52514e", "#a9a8a2", "#e6e5e0"

rows = [r for r in csv.DictReader(open(HERE / "../zec-binance-hyperliquid/zec_daily.csv"))
        if r["date"].startswith("2026-10")]
days = [dt.datetime.fromisoformat(r["date"]) for r in rows]
hl = [float(r["short_funding"]) * 36500 for r in rows]
bn = [float(r["long_funding"]) * 36500 for r in rows]
sp = [a - b for a, b in zip(hl, bn)]
btc = {dt.datetime.fromtimestamp(k["t"] / 1000, dt.UTC).replace(tzinfo=None): float(k["c"]) for k in json.load(open(HERE / "btc_daily_hl.json"))}
px = [btc[d] for d in days]

def avg(v): return sum(v) / len(v)
pre, sel = slice(0, 15), slice(15, 31)
print(f"BTC {px[0]:,.0f} -> {px[-1]:,.0f} ({px[-1]/px[0]-1:+.1%})")
print(f"spread pre {avg(sp[pre]):.1f}% sell {avg(sp[sel]):.1f}% | HL {avg(hl[pre]):.1f}->{avg(hl[sel]):.1f} | BN {avg(bn[pre]):.1f}->{avg(bn[sel]):.1f}")

fig, ax = plt.subplots(figsize=(12, 6), dpi=200)
ax2 = ax.twinx()
ax.set_zorder(ax2.get_zorder() + 1); ax.patch.set_visible(False)  # BTC line on top of the fill

ax.plot(days, [p / 1000 for p in px], color=BTC, lw=2, ls="--", label="BTC price (left)")
ax2.fill_between(days, bn, hl, where=[s >= 0 for s in sp], interpolate=True,
                 color=SPREAD, alpha=0.18, lw=0, label="Spread (HL − Binance)")
ax2.fill_between(days, bn, hl, where=[s < 0 for s in sp], interpolate=True, color="#e34948", alpha=0.25, lw=0)
ax2.plot(days, hl, color=HL, lw=2, label="ZEC funding · Hyperliquid (right)")
ax2.plot(days, bn, color=BIN, lw=2, label="ZEC funding · Binance (right)")

# selloff window + period averages
ax2.axvspan(days[15] - dt.timedelta(hours=12), days[-1] + dt.timedelta(hours=12), color="#f3f2ee", zorder=0, lw=0)
ax2.text(days[7], 0.97, f"Oct 1–15 · avg spread {avg(sp[pre]):.1f}%", transform=ax2.get_xaxis_transform(),
         ha="center", va="top", fontsize=11, color=INK2)
ax2.text(days[23], 0.97, f"Oct 16–31 selloff · avg spread {avg(sp[sel]):.1f}%",
         transform=ax2.get_xaxis_transform(), ha="center", va="top", fontsize=11, color=INK, fontweight="bold")
ax.annotate(f"${px[0]/1000:.1f}K", (days[0], px[0] / 1000), xytext=(4, 6), textcoords="offset points", fontsize=10, color=INK2)
ax.text(days[-1], 71.2, f"BTC Oct 31: ${px[-1]/1000:.1f}K ({px[-1]/px[0]-1:+.1%})",
        ha="right", va="bottom", fontsize=10.5, color=INK2, fontweight="bold")

ax.set_title("ZEC funding arb vs BTC, October 2026: rates fall, the spread holds",
             loc="left", fontsize=15, color=INK, fontweight="bold", pad=14)
for a in (ax, ax2):
    for s in ("top", "left", "right"): a.spines[s].set_visible(False)
    a.tick_params(colors=INK2, labelsize=10, length=0)
ax.spines["bottom"].set_color(MUTED); ax2.spines["bottom"].set_visible(False)
ax2.grid(axis="y", color=GRID, lw=0.8); ax2.set_axisbelow(True)
ax.set_ylabel("BTC price ($K)", color=INK2, fontsize=10)
ax2.set_ylabel("ZEC funding, annualized", color=INK2, fontsize=10)
ax.yaxis.set_major_formatter(lambda v, _: f"${v:.0f}K")
ax2.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
ax.set_ylim(70, 95)
lo = min(min(bn), min(hl)); hi = max(max(bn), max(hl))
ax2.set_ylim(min(-5, lo - 2), hi + 8)
ax.set_xlim(days[0] - dt.timedelta(hours=12), days[-1] + dt.timedelta(hours=12))
ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=[1, 5, 10, 15, 20, 25, 31]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h2[1:] + h2[:1] + h1, l2[1:] + l2[:1] + l1, loc="upper center", bbox_to_anchor=(0.5, -0.08),
          ncol=4, frameon=False, fontsize=10, labelcolor=INK2)
fig.text(0.01, 0.01, "Daily funding annualized (×365). Spread = Hyperliquid − Binance (short HL / long Binance). "
         "BTC = Hyperliquid perp daily close. Shaded: Oct 16–31 selloff.", fontsize=8.5, color=MUTED)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(HERE / "zec_funding_arb_vs_btc_oct26.png")
