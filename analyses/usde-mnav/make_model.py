"""Builds usde_mnav_model.xlsx: inputs, balance sheet, mNAV history and scenarios (all formulas)."""
import csv, json
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.chart import LineChart, Reference

HERE = Path(__file__).parent
N = json.load(open(HERE / "numbers.json"))
Q3 = "https://www.sec.gov/Archives/edgar/data/2080215/000121390026120186/ea031225601ex99-1.htm"
WAIVER = "https://www.sec.gov/Archives/edgar/data/2080215/000121390026100751/ea030568601ex10-1.htm"

F = "Arial"
BLUE, BLACK, GREEN = Font(name=F, color="0000FF"), Font(name=F), Font(name=F, color="008000")
BOLD = Font(name=F, bold=True)
H1 = Font(name=F, bold=True, size=14)
NOTE = Font(name=F, italic=True, color="666666", size=9)
YELLOW = PatternFill("solid", fgColor="FFFF00")
HEAD = PatternFill("solid", fgColor="E8E8E4")
thin = Side(style="thin", color="BBBBBB")
TOP = Border(top=thin)
USD = '$#,##0;($#,##0);"-"'
USD2 = '$#,##0.00;($#,##0.00);"-"'
USD4 = '$0.0000'
PCT = '0.0%;(0.0%);"-"'
MULT = '0.00"x"'
NUM = '#,##0'

wb = Workbook()

# ---------------- Inputs ----------------
ws = wb.active
ws.title = "Inputs"
ws.column_dimensions["A"].width = 46
ws.column_dimensions["B"].width = 18
ws.column_dimensions["C"].width = 70
ws["A1"] = "USDE mNAV trade: inputs"; ws["A1"].font = H1
ws["A2"] = "Blue = input you can change. Black = formula. Yellow = key assumption. Green = link to another sheet."; ws["A2"].font = NOTE

def row(r, label, val, fmt, font=BLACK, note="", fill=None):
    ws.cell(r, 1, label).font = Font(name=F)
    c = ws.cell(r, 2, val); c.number_format = fmt; c.font = font
    if fill: c.fill = fill
    if note: ws.cell(r, 3, note).font = NOTE
    return c

ws["A4"] = "Market (as of " + N["asof"] + (", intraday" if N["intraday"] else "") + ")"; ws["A4"].font = BOLD
row(5, "USDE share price ($)", round(N["usde"], 4), USD2, BLUE, "Nasdaq: USDE, Yahoo Finance. Update before the IC.", YELLOW)
row(6, "ENA price ($)", N["ena"], USD4, BLUE, "Hyperliquid ENA perp, " + N["ena_time_utc"] + " UTC. Update before the IC.", YELLOW)

ws["A8"] = "Company (Q3 2026 results, 8-K filed 16 Nov 2026)"; ws["A8"].font = BOLD
row(9, "Class A shares outstanding", N["shares"], NUM, BLUE, "Q3 8-K: 24,029,576 Class A shares. Class B (3.16M) has votes but no economics.")
row(10, "ENA held (tokens)", N["ena_held"], NUM, BLUE, "~$802M ÷ $0.2648 (30 Sep) = ~$576M ÷ $0.1901 (30 Oct) = 3.03B. Company says 'approximately 3.0 billion'.")
row(11, "Cash ($)", N["cash"], USD, BLUE, "Balance sheet, 30 Sep 2026")
row(12, "Other assets ($)", N["other_assets"], USD, BLUE, "Other current assets $2.42M + intangibles $0.69M, 30 Sep 2026")
row(13, "Current liabilities ($)", N["cur_liab"], USD, BLUE, "Balance sheet, 30 Sep 2026. Warrant liability ($109.6M) excluded: settled in shares, not cash.")

ws["A15"] = "Derived"; ws["A15"].font = BOLD
row(16, "Market cap ($)", "=B5*B9", USD)
row(17, "ENA value at market ($)", "=B10*B6", USD)
row(18, "Net asset value, ENA at market ($)", "=B17+B11+B12-B13", USD)
row(19, "ENA per share", "=B10/B9", '#,##0.0')
row(20, "ENA value per share ($)", "=B17/B9", USD2)
row(21, "NAV per share ($)", "=B18/B9", USD2)
c = row(22, "mNAV today (market cap ÷ ENA value)", "=B16/B17", MULT, note="The number we trade. Entry mNAV for the scenarios."); c.font = BOLD; c.fill = YELLOW
row(23, "Price ÷ NAV per share (incl. cash and liabilities)", "=B5/B21", MULT, note="Close to mNAV because cash and liabilities are small.")

ws["A25"] = "Trade"; ws["A25"].font = BOLD
row(26, "Long USDE on Interactive Brokers ($)", N["long"], USD, BLUE, "Same dollar amount on both legs, not 126 ENA per share.", YELLOW)
row(27, "Short ENA perp on Hyperliquid ($)", N["short"], USD, BLUE, "", YELLOW)
row(28, "Hyperliquid leverage (x)", N["hl_lev"], '0.0"x"', BLUE, "Keep low: ENA did +270% in Q3. At 2x a ~+45% move uses up the margin.")
row(29, "Capital needed ($)", "=B26+B27/B28", USD, note="Long fully paid on IBKR + Hyperliquid margin")
row(30, "ENA funding, annualized (short earns if positive)", round(N["funding_ann_since_listing"], 4), PCT, BLUE,
    f"Avg since listing {N['funding_ann_since_listing']:.1%}; last 30 days {N['funding_ann_30d']:.1%}. Can go negative.", YELLOW)
row(31, "Holding period (days)", 180, NUM, BLUE)
row(32, "USDE trading cost, round trip (% of long)", 0.01, PCT, BLUE, "Assumption: spread + impact on a thin stock. ~1.0M shares/day.")
row(33, "Hyperliquid fees, round trip (% of short)", 0.0009, '0.00%', BLUE, "Assumption: 0.045% taker per side.")
row(34, "Funding earned over the holding period ($)", "=B27*B30*B31/365", USD)
row(35, "Trading costs ($)", "=B26*B32+B27*B33", USD)

# ---------------- Balance sheet ----------------
bs = wb.create_sheet("Balance sheet")
bs.column_dimensions["A"].width = 48
for col in "BCD":
    bs.column_dimensions[col].width = 20
bs["A1"] = "StablecoinX balance sheet: book vs market"; bs["A1"].font = H1
bs["A2"] = "Book = 30 Sep 2026 balance sheet (Q3 results). Market = ENA marked at today's price (Inputs!B6)."; bs["A2"].font = NOTE
bs["A3"] = "Source: " + Q3; bs["A3"].font = NOTE
bs["A3"].hyperlink = Q3
for j, h in enumerate(["", "Book, 30 Sep ($)", "At market today ($)", "Note"], 1):
    c = bs.cell(5, j, h); c.font = BOLD; c.fill = HEAD
lines = [
    ("ENA tokens", 212_751_644, "=Inputs!B17", "Book is cost less impairment, not market value"),
    ("Cash", 10_352_692, "=Inputs!B11", ""),
    ("Other assets", 3_108_115, "=Inputs!B12", "Prepaids, receivables, small digital assets, intangibles"),
]
r = 6
for lab, book, mkt, note in lines:
    bs.cell(r, 1, lab).font = Font(name=F)
    bs.cell(r, 2, book).font = BLUE
    bs.cell(r, 3, mkt).font = GREEN
    bs.cell(r, 4, note).font = NOTE
    r += 1
bs.cell(r, 1, "Total assets").font = BOLD
bs.cell(r, 2, "=SUM(B6:B8)"); bs.cell(r, 3, "=SUM(C6:C8)")
r += 1  # 10
bs.cell(r, 1, "Current liabilities").font = Font(name=F); bs.cell(r, 2, 1_983_077).font = BLUE; bs.cell(r, 3, "=Inputs!B13").font = GREEN
r += 1  # 11
bs.cell(r, 1, "Warrant liabilities").font = Font(name=F); bs.cell(r, 2, 109_550_592).font = BLUE; bs.cell(r, 3, 0).font = BLUE
bs.cell(r, 4, "Excluded at market: non-cash, settled in shares. 11.5M public warrants at $11.50 (10-Q) + sponsor warrants (~7.6M at $11.50/$15 per Starkiller, unverified). Out of the money").font = NOTE
r += 1  # 12
bs.cell(r, 1, "Total liabilities").font = BOLD; bs.cell(r, 2, "=B10+B11"); bs.cell(r, 3, "=C10+C11")
r += 1  # 13
bs.cell(r, 1, "Equity (NAV)").font = BOLD; bs.cell(r, 2, "=B9-B12"); bs.cell(r, 3, "=C9-C12")
bs.cell(r, 4, "Book equity per the filing: $114,678,782").font = NOTE
r += 1  # 14
bs.cell(r, 1, "Class A shares").font = Font(name=F); bs.cell(r, 2, "=Inputs!B9").font = GREEN; bs.cell(r, 3, "=Inputs!B9").font = GREEN
r += 1  # 15
bs.cell(r, 1, "NAV per share ($)").font = BOLD; bs.cell(r, 2, "=B13/B14"); bs.cell(r, 3, "=C13/C14")
r += 1  # 16
bs.cell(r, 1, "USDE share price ($)").font = Font(name=F); bs.cell(r, 3, "=Inputs!B5").font = GREEN
r += 1  # 17
bs.cell(r, 1, "Price ÷ NAV per share").font = BOLD; bs.cell(r, 3, "=C16/C15")
for rr in range(6, 15):
    for cc in (2, 3):
        bs.cell(rr, cc).number_format = USD
bs["B14"].number_format = NUM; bs["C14"].number_format = NUM
for cc in (2, 3):
    bs.cell(15, cc).number_format = USD2
bs["C16"].number_format = USD2; bs["C17"].number_format = MULT
for rr in (9, 12, 13):
    for cc in (1, 2, 3):
        bs.cell(rr, cc).border = TOP
bs["A19"] = "Proof the ENA can be sold to buy back stock: Waiver Letter (Exhibit 10.1, 8-K of 17 Sep 2026), clauses 1.1 and 5."; bs["A19"].font = NOTE
bs["A20"] = WAIVER; bs["A20"].hyperlink = WAIVER; bs["A20"].font = NOTE

# ---------------- History ----------------
hs = wb.create_sheet("History")
cols = ["Date", "USDE close ($)", "ENA price ($)", "Market cap ($)", "ENA value ($)", "mNAV"]
for j, h in enumerate(cols, 1):
    c = hs.cell(1, j, h); c.font = BOLD; c.fill = HEAD
    hs.column_dimensions["ABCDEF"[j - 1]].width = 16
rows = list(csv.DictReader(open(HERE / "usde_mnav_daily.csv")))
for i, rw in enumerate(rows, 2):
    hs.cell(i, 1, rw["date"]).font = BLUE
    hs.cell(i, 2, float(rw["usde_close"])).font = BLUE
    hs.cell(i, 3, float(rw["ena_price_at_nasdaq_close"])).font = BLUE
    hs.cell(i, 4, f"=B{i}*Inputs!$B$9"); hs.cell(i, 5, f"=C{i}*Inputs!$B$10"); hs.cell(i, 6, f"=D{i}/E{i}")
    hs.cell(i, 2).number_format = USD2; hs.cell(i, 3).number_format = USD4
    hs.cell(i, 4).number_format = USD; hs.cell(i, 5).number_format = USD; hs.cell(i, 6).number_format = '0.000"x"'
last = len(rows) + 1
hs.cell(last, 7, "intraday" if N["intraday"] else "").font = NOTE
hs["H1"] = "Stats"; hs["H1"].font = BOLD
stats = [("Max", f"=MAX(F2:F{last})"), ("Date of max", f"=INDEX(A2:A{last},MATCH(I2,F2:F{last},0))"),
         ("Average", f"=AVERAGE(F2:F{last})"), ("Median", f"=MEDIAN(F2:F{last})"),
         ("Min", f"=MIN(F2:F{last})"), ("Date of min", f"=INDEX(A2:A{last},MATCH(I6,F2:F{last},0))"),
         ("Latest", f"=F{last}"), ("Days", f"=COUNT(F2:F{last})")]
for k, (lab, fml) in enumerate(stats, 2):
    hs.cell(k, 8, lab).font = Font(name=F); c = hs.cell(k, 9, fml)
    c.number_format = '0.000"x"' if lab in ("Max", "Average", "Median", "Min", "Latest") else "@" if "Date" in lab else NUM
hs.column_dimensions["H"].width = 14; hs.column_dimensions["I"].width = 14
hs["H11"] = "mNAV = (USDE close × Class A shares) ÷ (ENA held × ENA price). ENA price = Hyperliquid ENA perp at the 4pm New York close."; hs["H11"].font = NOTE
ch = LineChart(); ch.title = "USDE mNAV since listing"; ch.height = 8; ch.width = 18
ch.add_data(Reference(hs, min_col=6, min_row=1, max_row=last), titles_from_data=True)
ch.set_categories(Reference(hs, min_col=1, min_row=2, max_row=last))
ch.y_axis.number_format = '0.0"x"'; ch.roundedCorners = False; ch.legend = None
ch.x_axis.delete = False; ch.y_axis.delete = False
hs.add_chart(ch, "H13")

# ---------------- Scenarios ----------------
sc = wb.create_sheet("Scenarios")
sc.column_dimensions["A"].width = 30
for col in "BCDEFGHIJ":
    sc.column_dimensions[col].width = 15
sc["A1"] = "USDE mNAV trade: scenarios"; sc["A1"].font = H1
sc["A2"] = "Long USDE, short ENA, equal dollars. Entry = today's mNAV. Exit levels from the history since listing."; sc["A2"].font = NOTE
sc["A4"] = "Entry mNAV"; sc["B4"] = "=Inputs!B22"; sc["B4"].font = GREEN; sc["B4"].number_format = MULT
sc["A5"] = "ENA price move to exit"; sc["B5"] = 0; sc["B5"].font = BLUE; sc["B5"].fill = YELLOW; sc["B5"].number_format = PCT
sc["C5"] = "0% = ENA flat. Try −50% or +100%: the hedge holds, the result scales by (1 + move)."; sc["C5"].font = NOTE
hdr = ["Scenario", "Exit mNAV", "Return on long", "Long P&L ($)", "Short P&L ($)", "Funding ($)", "Costs ($)", "Net P&L ($)", "Return on capital"]
for j, h in enumerate(hdr, 1):
    c = sc.cell(7, j, h); c.font = BOLD; c.fill = HEAD; c.alignment = Alignment(wrap_text=True)
scen = [("Historical max", "=History!I2"), ("Historical average", "=History!I4"), ("Today (no change)", "=B4"),
        ("Historical min", "=History!I6"), ("Half the historical min", "=History!I6/2"), ("Zero", 0),
        ("Custom (type an mNAV)", 0.45)]
for k, (lab, m) in enumerate(scen, 8):
    sc.cell(k, 1, lab).font = Font(name=F)
    c = sc.cell(k, 2, m); c.number_format = MULT
    c.font = BLUE if isinstance(m, (int, float)) else GREEN
    if lab.startswith("Custom"):
        c.fill = YELLOW
    sc.cell(k, 3, f"=(1+$B$5)*B{k}/$B$4-1").number_format = PCT
    sc.cell(k, 4, f"=Inputs!$B$26*C{k}").number_format = USD
    sc.cell(k, 5, f"=-Inputs!$B$27*$B$5").number_format = USD
    sc.cell(k, 6, "=Inputs!$B$34").number_format = USD
    sc.cell(k, 7, "=-Inputs!$B$35").number_format = USD
    sc.cell(k, 8, f"=SUM(D{k}:G{k})").number_format = USD
    sc.cell(k, 9, f"=H{k}/Inputs!$B$29").number_format = PCT
    sc.cell(k, 8).font = BOLD
sc["A16"] = "Long P&L = long × [(1 + ENA move) × exit mNAV ÷ entry mNAV − 1]. Short P&L = −short × ENA move. Funding = short × rate × days ÷ 365."; sc["A16"].font = NOTE
sc["A17"] = "Return on capital uses Inputs!B29 (long fully paid + Hyperliquid margin). Funding and costs use the holding period in Inputs."; sc["A17"].font = NOTE

sc["A19"] = "Net P&L ($) by exit mNAV (rows) and ENA move (columns)"; sc["A19"].font = BOLD
moves = [-0.5, -0.25, 0, 0.25, 0.5, 1.0]
mn = [0.065, 0.13, 0.2, 0.25, 0.3, 0.33, 0.4, 0.5, 0.6, 0.7, 1.0]
sc.cell(20, 1, "Exit mNAV ↓ / ENA move →").font = BOLD
for j, mv in enumerate(moves, 2):
    c = sc.cell(20, j, mv); c.number_format = '+0%;-0%;0%'; c.font = BLUE; c.fill = HEAD
for i, m in enumerate(mn, 21):
    c = sc.cell(i, 1, m); c.number_format = MULT; c.font = BLUE
    for j in range(2, 2 + len(moves)):
        col = "ABCDEFGHIJ"[j - 1]
        f = (f"=Inputs!$B$26*((1+{col}$20)*$A{i}/$B$4-1)-Inputs!$B$27*{col}$20+Inputs!$B$34-Inputs!$B$35")
        sc.cell(i, j, f).number_format = USD
sc["A33"] = "Includes funding and costs from Inputs. Hyperliquid margin on big ENA up-moves is not modelled: move collateral or keep leverage low."; sc["A33"].font = NOTE
sc.freeze_panes = "A8"

for s in wb.worksheets:
    for r_ in s.iter_rows():
        for c in r_:
            if c.font and c.font.name != F:
                c.font = Font(name=F, bold=c.font.bold, italic=c.font.italic, color=c.font.color, size=c.font.size)
wb.move_sheet("Scenarios", offset=-2)
wb.active = 0
wb.save(HERE / "usde_mnav_model.xlsx")
print("saved")
