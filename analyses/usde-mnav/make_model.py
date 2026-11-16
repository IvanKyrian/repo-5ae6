"""Simple USDE mNAV scenario model: inputs, a step-by-step scenario table and an ENA move x exit mNAV grid.
All cells are formulas off the Inputs block, so changing an input updates everything."""
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule

HERE = Path(__file__).parent
F = "Arial"
BLUE = Font(name=F, color="0000FF")
BLACK = Font(name=F)
BOLD = Font(name=F, bold=True)
H1 = Font(name=F, bold=True, size=14)
H2 = Font(name=F, bold=True, size=12)
NOTE = Font(name=F, italic=True, color="666666", size=9)
HEAD = PatternFill("solid", fgColor="E8E8E4")
YELLOW = PatternFill("solid", fgColor="FFFF00")
GREEN_F = PatternFill("solid", fgColor="D9F2E3")
RED_F = PatternFill("solid", fgColor="F9DEDC")
thin = Side(style="thin", color="BBBBBB")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
USD = '$#,##0;-$#,##0;$0'
USD2 = '$0.00'
USD4 = '$0.0000'
PCT = '+0%;-0%;0%'
PCT1 = '+0.0%;-0.0%;0.0%'
MULT = '0.00"x"'
NUM = '#,##0'

wb = Workbook()
ws = wb.active
ws.title = "Model"
ws.column_dimensions["A"].width = 34
for c in "BCDEFGHIJKL":
    ws.column_dimensions[c].width = 14

ws["A1"] = "USDE mNAV trade: scenarios"; ws["A1"].font = H1
ws["A2"] = "Blue cells are inputs. Everything else is a formula. Long USDE and short ENA, same dollar amount, no rebalancing, before fees and funding."
ws["A2"].font = NOTE

# ---------- Inputs ----------
ws["A4"] = "Inputs"; ws["A4"].font = H2
inputs = [
    ("Class A shares", 24_029_576, NUM, "Q3 2026 results (8-K, 16 Nov 2026)"),
    ("ENA held", 3_031_404_421, NUM, "Q2 10-Q, Note 3: 284,954,407 + 1,405,754,436 + 1,340,695,578"),
    ("ENA price ($)", 0.1169, USD4, "Hyperliquid, 16 Nov 2026"),
    ("USDE price ($)", 4.35, USD2, "Nasdaq, 16 Nov 2026"),
    ("Long USDE ($)", 1_000_000, USD, "Interactive Brokers"),
    ("Short ENA ($)", 1_000_000, USD, "Hyperliquid perp"),
]
for i, (lab, v, fmt, src) in enumerate(inputs, 5):
    ws.cell(i, 1, lab).font = BLACK
    c = ws.cell(i, 2, v); c.font = BLUE; c.number_format = fmt; c.fill = YELLOW; c.border = BOX
    ws.cell(i, 3, src).font = NOTE
# B5 shares, B6 ENA held, B7 ENA price, B8 USDE price, B9 long, B10 short

ws["A12"] = "Today"; ws["A12"].font = H2
derived = [
    ("ENA per share", "=B6/B5", '#,##0.0'),
    ("ENA value per share ($)", "=B13*B7", USD2),
    ("Market cap ($)", "=B8*B5", USD),
    ("ENA value ($)", "=B6*B7", USD),
    ("mNAV = market cap ÷ ENA value", "=B15/B16", MULT),
    ("Discount", "=1-B17", '0%'),
    ("USDE shares we buy", "=B9/B8", NUM),
    ("ENA we short", "=B10/B7", NUM),
]
for i, (lab, f, fmt) in enumerate(derived, 13):
    ws.cell(i, 1, lab).font = BLACK
    c = ws.cell(i, 2, f); c.number_format = fmt
ws["B17"].font = BOLD
# B13 ENA/share, B14 ENA value/share, B15 mcap, B16 ENA value, B17 mNAV, B18 discount, B19 shares, B20 ENA shorted

# ---------- Scenario table ----------
r0 = 23
ws.cell(r0 - 1, 1, "Scenarios, step by step").font = H2
hdr = ["Scenario", "ENA move", "Exit mNAV", "New ENA price", "New USDE price", "Long P&L", "Short P&L", "Net P&L", "Net % of long"]
for j, h in enumerate(hdr, 1):
    c = ws.cell(r0, j, h); c.font = BOLD; c.fill = HEAD; c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = BOX
ws.row_dimensions[r0].height = 30
scen = [
    ("Nothing moves", 0, "=$B$17"),
    ("ENA +50%, mNAV flat", 0.5, "=$B$17"),
    ("ENA −50%, mNAV flat", -0.5, "=$B$17"),
    ("ENA flat, mNAV up to 0.40x", 0, 0.40),
    ("ENA flat, mNAV down to 0.20x", 0, 0.20),
    ("ENA +50%, mNAV up to 0.40x", 0.5, 0.40),
    ("ENA −50%, mNAV up to 0.40x", -0.5, 0.40),
    ("ENA +50%, mNAV down to 0.20x", 0.5, 0.20),
    ("ENA −50%, mNAV down to 0.20x", -0.5, 0.20),
    ("ENA flat, back to waiver day (0.48x)", 0, 0.48),
    ("ENA flat, historical max (0.52x)", 0, 0.52),
    ("ENA flat, historical min (0.13x)", 0, 0.13),
    ("ENA flat, mNAV to zero", 0, 0),
]
for k, (lab, mv, m) in enumerate(scen, r0 + 1):
    ws.cell(k, 1, lab).font = BLACK
    c = ws.cell(k, 2, mv); c.font = BLUE; c.number_format = PCT
    c = ws.cell(k, 3, m); c.number_format = MULT; c.font = BLACK if isinstance(m, str) else BLUE
    ws.cell(k, 4, f"=$B$7*(1+B{k})").number_format = USD4
    ws.cell(k, 5, f"=D{k}*$B$13*C{k}").number_format = USD2
    ws.cell(k, 6, f"=$B$19*E{k}-$B$9").number_format = USD
    ws.cell(k, 7, f"=-$B$20*(D{k}-$B$7)").number_format = USD
    c = ws.cell(k, 8, f"=F{k}+G{k}"); c.number_format = USD; c.font = BOLD
    ws.cell(k, 9, f"=H{k}/$B$9").number_format = PCT1
    for j in range(1, 10):
        ws.cell(k, j).border = BOX
r_end = r0 + len(scen)
ws.cell(r_end + 1, 1, "New USDE price = new ENA price × ENA per share × exit mNAV. Long P&L = shares × new price − long. Short P&L = −ENA shorted × change in ENA price.").font = NOTE
ws.cell(r_end + 2, 1, "Blue cells in the table (ENA move, exit mNAV) can be changed to test any scenario.").font = NOTE

# ---------- Grid ----------
g0 = r_end + 5
ws.cell(g0 - 1, 1, "Net P&L ($): exit mNAV (rows) × ENA move (columns)").font = H2
moves = [-0.5, -0.25, 0, 0.25, 0.5, 1.0]
levels = [("Zero", 0), ("Half the min", 0.065), ("Historical min", 0.13), ("", 0.20), ("", 0.25), ("Today", "=$B$17"),
          ("Average", 0.33), ("", 0.40), ("Waiver day", 0.48), ("Historical max", 0.52), ("", 0.70), ("Parity", 1.0)]
c = ws.cell(g0, 1, "Exit mNAV ↓   ENA move →"); c.font = BOLD; c.fill = HEAD; c.border = BOX
c = ws.cell(g0, 2, ""); c.fill = HEAD; c.border = BOX
for j, mv in enumerate(moves, 3):
    c = ws.cell(g0, j, mv); c.font = Font(name=F, bold=True, color="0000FF"); c.fill = HEAD; c.number_format = PCT; c.border = BOX
    c.alignment = Alignment(horizontal="center")
for i, (lab, m) in enumerate(levels, g0 + 1):
    ws.cell(i, 1, lab).font = BLACK
    c = ws.cell(i, 2, m); c.number_format = MULT; c.font = BLACK if isinstance(m, str) else BLUE
    if lab == "Today":
        ws.cell(i, 1).font = BOLD; c.font = BOLD
    for j in range(3, 3 + len(moves)):
        col = "ABCDEFGHIJKL"[j - 1]
        f = f"=$B$19*($B$7*(1+{col}${g0})*$B$13*$B{i})-$B$9-$B$20*($B$7*{col}${g0})"
        cc = ws.cell(i, j, f); cc.number_format = USD; cc.border = BOX
    ws.cell(i, 1).border = BOX; ws.cell(i, 2).border = BOX
g_end = g0 + len(levels)
rng = f"C{g0+1}:H{g_end}"
ws.conditional_formatting.add(rng, CellIsRule(operator="greaterThan", formula=["0.5"], fill=GREEN_F))
ws.conditional_formatting.add(rng, CellIsRule(operator="lessThan", formula=["-0.5"], fill=RED_F))
ws.conditional_formatting.add(f"H{r0+1}:H{r_end}", CellIsRule(operator="greaterThan", formula=["0.5"], fill=GREEN_F))
ws.conditional_formatting.add(f"H{r0+1}:H{r_end}", CellIsRule(operator="lessThan", formula=["-0.5"], fill=RED_F))
ws.cell(g_end + 1, 1, "Read it like this: the row (mNAV) decides if we win or lose. The column (ENA) only makes the result bigger or smaller.").font = NOTE
ws.cell(g_end + 2, 1, "Same formula as the table: Net = long × [(1 + ENA move) × exit mNAV ÷ today's mNAV − 1] − short × ENA move.").font = NOTE

ws.freeze_panes = "A4"
wb.save(HERE / "usde_mnav_model.xlsx")
print("saved", g0, g_end)
