import sys, openpyxl, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

src, out = sys.argv[1], sys.argv[2]
ws = openpyxl.load_workbook(src)["Sheet1"]
rows = [r for r in ws.iter_rows(min_row=3, max_row=23, values_only=True)]
q = [r[1] for r in rows]
m = np.array([[r[2], r[3], r[4]] for r in rows], float)
btc = np.array([r[5] for r in rows], float)
t3 = np.array([r[6] for r in rows], float)
t10 = np.array([r[7] for r in rows], float)

fund = (np.prod(1 + m, axis=1) ** 4 - 1)[1:] * 100     # % annualized
btc_chg = (btc[1:] / btc[:-1] - 1) * 100               # %
t3_chg = (t3[1:] - t3[:-1]) * 100                      # pp
t10_chg = (t10[1:] - t10[:-1]) * 100                   # pp
labels = q[1:]

FUND, OTHER, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#1a1a19", "#6b6a63", "#e6e5e0"

def chart(y, name, unit_fmt, fname, note):
    r = np.corrcoef(fund, y)[0, 1]
    fig, ax = plt.subplots(figsize=(11, 5.2), dpi=200)
    x = np.arange(len(labels))
    ax.plot(x, fund, color=FUND, lw=2, marker="o", ms=4, label="Fund return (annualized, %)")
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.set_ylabel("Fund return, annualized (%)", color=INK)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax2 = ax.twinx()
    ax2.plot(x, y, color=OTHER, lw=2, marker="o", ms=4, label=name)
    ax2.set_ylabel(name, color=INK)
    ax2.yaxis.set_major_formatter(FuncFormatter(unit_fmt))
    # align zero on both axes
    for a, d in ((ax, fund), (ax2, y)):
        lo, hi = min(d.min(), 0), max(d.max(), 0)
        pad = (hi - lo) * 0.08
        a.set_ylim(lo - pad, hi + pad)
    l1, h1 = ax.get_ylim(); l2, h2 = ax2.get_ylim()
    f = max(-l1 / (h1 - l1), -l2 / (h2 - l2))
    ax.set_ylim(*( (-f * h1 / (1 - f), h1) if -l1/(h1-l1) < f else (l1, h1) ))
    ax2.set_ylim(*( (-f * h2 / (1 - f), h2) if -l2/(h2-l2) < f else (l2, h2) ))
    ax.set_xticks(x); ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
    ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    for a in (ax, ax2):
        for s in ("top",): a.spines[s].set_visible(False)
        a.spines["left"].set_color(MUTED); a.spines["right"].set_color(MUTED); a.spines["bottom"].set_color(MUTED)
        a.tick_params(colors=MUTED, labelsize=8)
    ax.set_title(f"Fund return vs {name}    |    Correlation: {r:+.2f}", loc="left", fontsize=12, color=INK, pad=12)
    h = ax.get_legend_handles_labels(); h2_ = ax2.get_legend_handles_labels()
    ax.legend(h[0] + h2_[0], h[1] + h2_[1], loc="upper right", frameon=False, fontsize=9)
    fig.text(0.01, 0.01, "Quarterly, Q4 2021 – Q3 2026 (20 obs.). Fund: ((1+m1)(1+m2)(1+m3))^4 − 1. " + note, fontsize=7, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(f"{out}/{fname}", facecolor="white")
    print(fname, f"r={r:+.4f}", "right-axis range", y.min().round(2), y.max().round(2))

pct = lambda v, _: f"{v:+.0f}%"
pp = lambda v, _: f"{v:+.2f} pp"
chart(btc_chg, "BTC price change QoQ (%)", pct, "1_fund_vs_btc.png", "BTC: change in quarterly average price.")
chart(t3_chg, "US 3M Treasury change (pp)", pp, "2_fund_vs_ust3m.png", "Treasury: change in quarterly average yield, in percentage points.")
chart(t10_chg, "US 10Y Treasury change (pp)", pp, "3_fund_vs_ust10y.png", "Treasury: change in quarterly average yield, in percentage points.")
