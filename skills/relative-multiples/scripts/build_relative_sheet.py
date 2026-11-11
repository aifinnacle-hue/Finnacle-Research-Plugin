#!/usr/bin/env python3
# Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.
# Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.
# Keep this notice intact in any copy or modified version of this file.
"""
build_relative_sheet.py — Peer relative (trading) multiples sheet builder.

Given a JSON of the subject company + peers, with per-year fundamentals, builds a
self-contained Excel "Peer - Relative Valuation" sheet: a two-panel block per company
(multiples + median | underlying data), a summary median table, and a FY-base-year
snapshot table. Every multiple is a LIVE formula over the data cells, so the ONE
uncertain input per year — the FY-end share price (a blue input cell) — can be
overwritten and the sheet recomputes.

Usage:
    python build_relative_sheet.py data.json output.xlsx
    python <xlsx-skill>/scripts/recalc.py output.xlsx 60   # verify 0 errors

Multiple convention:
    Market Cap = Share Price × Shares Outstanding / 1e7   (₹ Crore)
    EV         = Market Cap + Debt − Cash & Investments
    EV multiples  = EV / {Revenue, Gross Profit, EBITDA, EBIT, CFO, FCFF, <KPIs>}
    Equity mult   = P/E = MktCap / PAT ;  P/B = MktCap / Book Value of Equity
    Median column = MEDIAN across the years that have data.

DATA SCHEMA (data.json)
-----------------------
{
  "title": "Peer - Group Valuation | Relative Multiples | FY2021-FY2026",
  "subtitle": "one-line basis note",
  "years": [2021,2022,2023,2024,2025,2026],
  "base_year": 2026,
  "kpi_multiples": [ {"name":"EV / Sample","denom":"Sample"},
                     {"name":"EV / Patient","denom":"Patient"} ],
  "companies": [
    {"name":"Dr LalPath Labs",
     "data": {
        "Revenue":[...], "Gross Profit":[...], "EBITDA":[...], "EBIT":[...],
        "CFO":[...], "FCFF":[...], "PAT":[...],
        "Sample":[...], "Patient":[...],           # KPI rows (match kpi_multiples denoms)
        "Share Price":[...], "Shares Outstanding":[...],
        "Enterprise Value":[...],                   # optional; null years computed from Debt/Cash
        "Debt":[...], "Cash & Investments":[...], "Book Value of Equity":[...]
     },
     "note": "optional italic footnote under the block"}
  ],
  "subject": "Thyrocare",                # optional: the subject company
  "subject_medians": { "EV / Revenue": 6.65, ... }   # optional cached medians if subject has no per-year build
}
Use null for any value not available (blank cell, never 0). Arrays must be len(years).
"""
import json, sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

HDR_FILL=PatternFill("solid",fgColor="8EA9DB"); CO_FILL=PatternFill("solid",fgColor="D9E1F2")
IN_BLUE="0000FF"; BLK="000000"; FONT="Calibri"
thin=Side(style="thin",color="B9B9B9"); BORD=Border(left=thin,right=thin,top=thin,bottom=thin)
MULT_FMT="0.0"; NUM_FMT="#,##0.0"

STD_MULTS=[("EV / Revenue","EV","Revenue"),("EV / Gross Profit","EV","Gross Profit"),
 ("EV / EBITDA","EV","EBITDA"),("EV / EBIT","EV","EBIT"),("EV / CFO","EV","CFO"),
 ("EV / FCFF","EV","FCFF")]
TAIL_MULTS=[("P/E","MktCap","PAT"),("P/B","MktCap","Book Value of Equity")]
INPUT_ROWS={"Share Price","Shares Outstanding","Debt","Cash & Investments"}

def build(cfg, out):
    years=cfg["years"]; nY=len(years); base=cfg.get("base_year",years[-1])
    kpis=cfg.get("kpi_multiples",[])
    MULTS=STD_MULTS+[(k["name"],"EV",k["denom"]) for k in kpis]+TAIL_MULTS
    DATA_ORDER=["Revenue","Gross Profit","EBITDA","EBIT","CFO","FCFF","PAT"]+\
        [k["denom"] for k in kpis]+["Share Price","Shares Outstanding","Market Capitalisation",
        "Enterprise Value","Debt","Cash & Investments","Book Value of Equity"]
    MCOL0=3; MEDCOL=3+nY; DLAB=MEDCOL+2; DCOL0=DLAB+1
    def mcol(i): return MCOL0+i
    def dcol(i): return DCOL0+i
    wb=openpyxl.Workbook(); ws=wb.active; ws.title="Peer - Relative Valuation"
    ws.sheet_view.showGridLines=False
    def hdr(cell,text,fill=HDR_FILL,size=11,bold=True,color="000000"):
        cell.value=text; cell.fill=fill; cell.font=Font(name=FONT,size=size,bold=bold,color=color)
        cell.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True); cell.border=BORD
    med_cells={}
    def block(start,name,D,note=None):
        c=ws.cell(start,2); c.value=name; c.font=Font(name=FONT,size=12,bold=True); c.fill=CO_FILL
        for cc in range(2,DCOL0+nY): ws.cell(start,cc).fill=CO_FILL
        yr=start+1; hdr(ws.cell(yr,2),"Years")
        for i,y in enumerate(years):
            hdr(ws.cell(yr,mcol(i)),y)
            if y==base: ws.cell(yr,mcol(i)).font=Font(name=FONT,size=11,bold=True,color="C00000")
        hdr(ws.cell(yr,MEDCOL),"Median"); hdr(ws.cell(yr,DLAB),"Data")
        for i,y in enumerate(years):
            hdr(ws.cell(yr,dcol(i)),y)
            if y==base: ws.cell(yr,dcol(i)).font=Font(name=FONT,size=11,bold=True,color="C00000")
        ds=yr+1; rowof={n:ds+ix for ix,n in enumerate(DATA_ORDER)}
        def has(metric,i):
            arr=D.get(metric); return arr is not None and i<len(arr) and arr[i] is not None
        for n in DATA_ORDER:
            r=rowof[n]; lc=ws.cell(r,DLAB); lc.value=n; lc.font=Font(name=FONT,size=10)
            lc.border=BORD; lc.alignment=Alignment(horizontal="left",vertical="center")
            for i in range(nY):
                cell=ws.cell(r,dcol(i)); cell.border=BORD
                cell.alignment=Alignment(horizontal="right",vertical="center")
                L=get_column_letter(dcol(i))
                if n=="Market Capitalisation":
                    if has("Share Price",i) and has("Shares Outstanding",i):
                        cell.value=f"=({L}{rowof['Share Price']}*{L}{rowof['Shares Outstanding']})/10000000"
                        cell.font=Font(name=FONT,size=10,color=BLK); cell.number_format=NUM_FMT
                    continue
                if n=="Enterprise Value":
                    ev=D.get("Enterprise Value")
                    if ev and i<len(ev) and ev[i] is not None:
                        cell.value=ev[i]; cell.font=Font(name=FONT,size=10,color=IN_BLUE); cell.number_format=NUM_FMT
                    elif has("Debt",i) and has("Cash & Investments",i) and has("Share Price",i):
                        cell.value=f"={L}{rowof['Market Capitalisation']}+{L}{rowof['Debt']}-{L}{rowof['Cash & Investments']}"
                        cell.font=Font(name=FONT,size=10,color=BLK); cell.number_format=NUM_FMT
                    continue
                if has(n,i):
                    cell.value=D[n][i]; cell.number_format=NUM_FMT
                    cell.font=Font(name=FONT,size=10,color=IN_BLUE)
        for j,(mn,num,den) in enumerate(MULTS):
            r=ds+j; lc=ws.cell(r,2); lc.value=mn; lc.font=Font(name=FONT,size=10); lc.border=BORD
            lc.alignment=Alignment(horizontal="left",vertical="center")
            numrow=rowof["Market Capitalisation"] if num=="MktCap" else rowof["Enterprise Value"]
            denrow=rowof[den]; present=[]
            for i in range(nY):
                cell=ws.cell(r,mcol(i)); cell.border=BORD
                cell.alignment=Alignment(horizontal="right",vertical="center")
                L=get_column_letter(dcol(i))
                den_ok=has(den,i)
                num_ok=(D.get("Enterprise Value") and i<len(D["Enterprise Value"]) and D["Enterprise Value"][i] is not None) \
                    or (num=="MktCap" and has("Share Price",i) and has("Shares Outstanding",i)) \
                    or (num=="EV" and has("Debt",i) and has("Cash & Investments",i) and has("Share Price",i))
                if den_ok and num_ok:
                    cell.value=f"={L}{numrow}/{L}{denrow}"; cell.font=Font(name=FONT,size=10,color=BLK)
                    cell.number_format=MULT_FMT; present.append(f"{get_column_letter(mcol(i))}{r}")
            mc=ws.cell(r,MEDCOL); mc.border=BORD; mc.alignment=Alignment(horizontal="right",vertical="center")
            if present:
                mc.value=f"=MEDIAN({','.join(present)})"; mc.font=Font(name=FONT,size=10,bold=True,color=BLK)
                mc.number_format=MULT_FMT
            med_cells[(name,mn)]=f"{get_column_letter(MEDCOL)}{r}"
        end=ds+len(DATA_ORDER)
        if note:
            nc=ws.cell(end,2); nc.value=note; nc.font=Font(name=FONT,size=8,italic=True,color="808080")
            ws.merge_cells(start_row=end,start_column=2,end_row=end,end_column=DCOL0+nY-1); end+=1
        return end+1
    # title
    ws.cell(2,2).value=cfg.get("title","Peer - Relative Valuation")
    ws.cell(2,2).font=Font(name=FONT,size=13,bold=True,color="1F4978")
    if cfg.get("subtitle"):
        ws.cell(3,2).value=cfg["subtitle"]; ws.cell(3,2).font=Font(name=FONT,size=8,italic=True,color="808080")
    mult_names=[m[0] for m in MULTS]
    SUMHDR=["Index","Company Names"]+mult_names
    sr=5
    for i,h in enumerate(SUMHDR): hdr(ws.cell(sr,2+i),h)
    cur=11; starts={}
    for co in cfg["companies"]:
        starts[co["name"]]=cur; cur=block(cur,co["name"],co["data"],co.get("note"))
    # summary median table
    subj=cfg.get("subject"); subj_med=cfg.get("subject_medians",{})
    for k,co in enumerate(cfg["companies"]):
        rr=sr+1+k; ws.cell(rr,2).value=k+1; ws.cell(rr,2).font=Font(name=FONT,size=10)
        ws.cell(rr,3).value=co["name"]; ws.cell(rr,3).font=Font(name=FONT,size=10,bold=True)
        for mi,mn in enumerate(mult_names):
            cell=ws.cell(rr,4+mi); cell.border=BORD; cell.number_format=MULT_FMT
            cell.alignment=Alignment(horizontal="right",vertical="center")
            # Subject's through-cycle median comes from its own linked model (cached),
            # not from the lone base-year point gathered here. Peers use their series median.
            if co["name"]==subj and mn in subj_med:
                cell.value=subj_med[mn]; cell.font=Font(name=FONT,size=10,italic=True,color="808080")
            else:
                cell.value=f"={med_cells[(co['name'],mn)]}"; cell.font=Font(name=FONT,size=10,color=BLK)
        for cc in range(2,4+len(mult_names)): ws.cell(rr,cc).border=BORD
    # base-year snapshot table (below blocks)
    s2=cur+1; ws.cell(s2,2).value=f"FY{base} snapshot (at FY{base}-end price) — the base-year comparison"
    ws.cell(s2,2).font=Font(name=FONT,size=10,bold=True,color="1F4978"); s2+=1
    for i,h in enumerate(SUMHDR): hdr(ws.cell(s2,2+i),h)
    base_i=years.index(base)
    for k,co in enumerate(cfg["companies"]):
        rr=s2+1+k; ws.cell(rr,2).value=k+1; ws.cell(rr,3).value=co["name"]
        ws.cell(rr,3).font=Font(name=FONT,size=10,bold=True)
        ds=starts[co["name"]]+2
        for mi,mn in enumerate(mult_names):
            cell=ws.cell(rr,4+mi); cell.border=BORD; cell.number_format=MULT_FMT
            cell.alignment=Alignment(horizontal="right",vertical="center")
            den=MULTS[mi][2]; arr=co["data"].get(den)
            if arr and base_i<len(arr) and arr[base_i] is not None:
                cell.value=f"={get_column_letter(mcol(base_i))}{ds+mi}"; cell.font=Font(name=FONT,size=10,color=BLK)
        for cc in range(2,4+len(mult_names)): ws.cell(rr,cc).border=BORD
    ws.column_dimensions['B'].width=22
    for c in range(3,MEDCOL+1): ws.column_dimensions[get_column_letter(c)].width=9
    ws.column_dimensions[get_column_letter(DLAB)].width=20
    for c in range(DCOL0,DCOL0+nY): ws.column_dimensions[get_column_letter(c)].width=11
    wb.save(out); print("saved",out)

if __name__=="__main__":
    if len(sys.argv)<3: print(__doc__); sys.exit(1)
    build(json.load(open(sys.argv[1])), sys.argv[2])
