# -*- coding: utf-8 -*-
"""
Generator jurnal trading 1 bulan -> .xlsx, dioptimalkan untuk Google Sheets.
Jalankan:  venv/bin/python build_journal.py
Ubah YEAR/MONTH di bawah untuk bulan lain.
"""
import datetime as dt, calendar
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

YEAR, MONTH = 2026, 8
NDAYS = calendar.monthrange(YEAR, MONTH)[1]
OUT = f"/Users/wahyusetiawan/Documents/tradingview/snd/trading-journal-{YEAR}-{MONTH:02d}.xlsx"
GS  = "/Users/wahyusetiawan/Documents/tradingview/snd/journal-charts.gs"
FIRST, LAST = 3, 152

G="📋 Panduan"; S="⚙️ Setelan"; J="📒 Jurnal"; H="📅 Harian"
C="📈 Data Chart"; D="📊 Dashboard"; R="🔍 Review"
qJ,qS,qH,qD,qC = f"'{J}'", f"'{S}'", f"'{H}'", f"'{D}'", f"'{C}'"

INK="1F2937"; INK2="374151"; GREY="F3F4F6"
WIN="D1FAE5"; LOSS="FEE2E2"; WARN="FEF3C7"; NEUT="E5E7EB"
def fill(c): return PatternFill("solid", fgColor=c)
thin=Side(style="thin",color="D1D5DB"); BOX=Border(left=thin,right=thin,top=thin,bottom=thin)
def hdr(ws,cell,text,bg=INK,fg="FFFFFF",size=10):
    c=ws[cell]; c.value=text; c.font=Font(bold=True,color=fg,size=size); c.fill=fill(bg)
    c.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True); c.border=BOX; return c
def title(ws,cell,text,size=14):
    c=ws[cell]; c.value=text; c.font=Font(bold=True,size=size,color=INK); return c
def band(ws,row,text,span="A:F",bg=INK2):
    a,b=span.split(":"); ws.merge_cells(f"{a}{row}:{b}{row}")
    c=ws[f"{a}{row}"]; c.value=text; c.font=Font(bold=True,size=11,color="FFFFFF"); c.fill=fill(bg); return c

wb=Workbook()

# ───────────────────────────── PANDUAN ─────────────────────────────
g=wb.active; g.title=G
g.column_dimensions["A"].width=4; g.column_dimensions["B"].width=118
g.sheet_view.showGridLines=False
title(g,"B2","📋 JURNAL TRADING — PANDUAN PAKAI",16)
guide=[("",""),
 ("h","① IMPORT KE GOOGLE SHEETS"),
 ("t","sheets.google.com → File → Import → Upload → pilih \"Create new spreadsheet\"."),
 ("t","Lalu set File → Settings → Locale ke Indonesia (biar tanggal dd/mm terbaca benar)."),
 ("t","File ini dioptimalkan untuk Google Sheets. Di Excel, SPARKLINE/IMAGE/REGEXEXTRACT error #NAME?."),
 ("",""),
 ("h","② PASANG GRAFIK (sekali saja, ~2 menit)"),
 ("t","Grafik native tidak bisa ikut lewat file .xlsx, jadi dipasang lewat skrip kecil:"),
 ("t","   1. Extensions → Apps Script"),
 ("t","   2. Hapus isi editor, paste seluruh isi file journal-charts.gs"),
 ("t","   3. Simpan (💾) → pilih fungsi buatGrafik → Run → Authorize akses"),
 ("t","   4. Balik ke tab 📊 Dashboard — 6 grafik sudah terpasang"),
 ("t","Grafik update otomatis tiap kamu isi trade. Jalankan ulang buatGrafik kalau mau reset posisi."),
 ("",""),
 ("h","③ ISI TAB SETELAN DULU"),
 ("t","Modal, risiko per trade, batas rugi harian, target bulanan, kurs USD→IDR."),
 ("t","Cek tabel instrumen. Kolom \"Pembagi Konversi\" USDJPY = harga USDJPY sekarang (default 155)."),
 ("",""),
 ("h","④ ALUR ISI 1 TRADE — target di bawah 60 detik"),
 ("t","Dari 43 kolom, cuma 12 yang perlu ketik. Sisanya dropdown atau otomatis."),
 ("t","   Ketik   : Tanggal, Jam Masuk, Jam Keluar, Entry, SL, TP, Exit, Lot, Harga Terburuk/Terbaik"),
 ("t","   Dropdown: Instrumen, Arah, Setup, TF, Bias M15, Bias EMA200, SVP, News, Emosi, Fisik,"),
 ("t","             Keyakinan, Checklist, Kesalahan"),
 ("t","   Otomatis: Sesi, Lot Saran, Risiko $, RR, PnL, Biaya, R Hasil, Hasil, Durasi, MAE, MFE"),
 ("",""),
 ("h","⑤ SCREENSHOT"),
 ("t","Di TradingView tekan Alt+S → link tersalin. Paste ke kolom \"Link Sebelum\"/\"Link Sesudah\"."),
 ("t","Gambar muncul sendiri di kolom sebelahnya. Link .png/.jpg biasa juga diterima."),
 ("",""),
 ("h","⑥ FILTER INTERAKTIF DI DASHBOARD"),
 ("t","Di atas Dashboard ada 6 dropdown: Instrumen, Setup, Sesi, Emosi, Kondisi Fisik, Bias EMA200."),
 ("t","Ubah salah satu → SEMUA metrik, tabel, dan grafik ikut menyesuaikan. Pilih \"(Semua)\" untuk reset."),
 ("t","Contoh: set Emosi = FOMO, lihat win rate & expectancy kamu khusus saat FOMO."),
 ("",""),
 ("h","⑦ KOLOM YANG PALING SERING DILEWATI — padahal paling berharga"),
 ("t","• Harga Terburuk/Terbaik → hitung MAE/MFE. Ini yang ngasih tau SL kesempitan atau TP kecepetan."),
 ("t","• Emosi + Kondisi Fisik → setelah ~30 trade, kelihatan win rate saat FOMO vs tenang."),
 ("t","• Bias EMA200 Searah → bikin kamu bisa buktiin sendiri filter EMA200 berguna atau tidak."),
 ("",""),
 ("w","⚠️ PERINGATAN JUMLAH SAMPEL"),
 ("t","Satu bulan scalping ≈ 40–100 trade. Itu BELUM cukup untuk kesimpulan statistik."),
 ("t","Beda win rate 10% pada 40 trade masih sangat mungkin kebetulan. Baca angka Dashboard sebagai"),
 ("t","PETUNJUK ARAH. Kumpulkan 3–6 bulan sebelum membuang satu jenis setup."),
]
r=3
for kind,txt in guide:
    c=g.cell(row=r,column=2,value=txt)
    if kind=="h": c.font=Font(bold=True,size=11,color="FFFFFF"); c.fill=fill(INK2)
    elif kind=="w": c.font=Font(bold=True,size=11,color="7C2D12"); c.fill=fill(WARN)
    else: c.font=Font(size=10,color=INK)
    c.alignment=Alignment(vertical="center"); r+=1

# ───────────────────────────── SETELAN ─────────────────────────────
s=wb.create_sheet(S)
s.column_dimensions["A"].width=34
for col,w in zip("BCDEF",(16,18,26,20,10)): s.column_dimensions[col].width=w
s.sheet_view.showGridLines=False
title(s,"A1","⚙️ SETELAN — isi sekali di awal bulan",14)
for i,(label,val,fmt) in enumerate([
    ("Modal Awal (USD)",1000,"$#,##0"),("Risiko per Trade (%)",1.0,"0.0"),
    ("Batas Rugi Harian (USD)",30,"$#,##0"),("Max Trade per Malam",5,"0"),
    ("Target Profit Bulanan (USD)",1000,"$#,##0"),("Kurs USD → IDR",16000,"#,##0"),
    ("Jeda Min Setelah Loss (menit)",10,"0")]):
    rr=3+i
    c=s.cell(row=rr,column=1,value=label); c.font=Font(bold=True,size=10); c.fill=fill(GREY); c.border=BOX
    v=s.cell(row=rr,column=2,value=val); v.number_format=fmt; v.border=BOX
    v.font=Font(bold=True,color="065F46"); v.fill=fill("ECFDF5"); v.alignment=Alignment(horizontal="center")
s["C3"]="← ubah angka di kolom hijau sesuai akunmu"; s["C3"].font=Font(italic=True,size=9,color="6B7280")
title(s,"A11","SPESIFIKASI INSTRUMEN",12)
s["A12"]="Dipakai rumus PnL. Rentang VLOOKUP sampai baris 20 — ada 2 baris kosong untuk instrumen tambahan."
s["A12"].font=Font(italic=True,size=9,color="6B7280")
for i,t in enumerate(["Instrumen","Ukuran Kontrak","Pembagi Konversi","Nilai per 1.00 Gerak/Lot (USD)","Biaya per Lot (USD)","Digit"]):
    hdr(s,f"{get_column_letter(1+i)}13",t)
for i,(nm,cs,conv,cost,dg) in enumerate([("XAUUSD",100,1,11,2),("BTCUSD",1,1,8.75,2),("EURUSD",100000,1,10,5),
                                          ("GBPUSD",100000,1,15,5),("USDJPY",100000,155,6.5,3)]):
    rr=14+i
    s.cell(row=rr,column=1,value=nm).font=Font(bold=True)
    s.cell(row=rr,column=2,value=cs).number_format="#,##0"
    s.cell(row=rr,column=3,value=conv)
    s.cell(row=rr,column=4,value=f"=B{rr}/C{rr}").number_format="#,##0.00"
    s.cell(row=rr,column=5,value=cost).number_format="$#,##0.00"
    s.cell(row=rr,column=6,value=dg)
    for cc in range(1,7): s.cell(row=rr,column=cc).border=BOX
s["A19"]="Biaya per Lot = komisi round-turn per 1.0 lot. XAU $11 & BTC $8.75 diambil dari CSV brokermu 31 Agu 2026."
s["A19"].font=Font(italic=True,size=9,color="6B7280")
s["A20"]="Angka ini komisi saja. Kalau akunmu spread-based (bukan raw), tambahkan estimasi spread ke sini."
s["A20"].font=Font(italic=True,size=9,color="7C2D12")
print("✓ Panduan + Setelan")

# ───────────────────────────── JURNAL ─────────────────────────────
j=wb.create_sheet(J)
INSTR=f"{qS}!$A$14:$F$20"
COLS=[("A","No",6),("B","Tanggal",11),("C","Jam Masuk",10),("D","Jam Keluar",10),("E","Sesi",15),
 ("F","Instrumen",11),("G","Arah",8),
 ("H","Tipe Setup",14),("I","TF Eksekusi",11),("J","Bias M15 Searah?",13),
 ("K","Bias EMA200 Searah?",14),("L","Konfluensi SVP",13),("M","News Besar?",11),
 ("N","Entry",11),("O","Stop Loss",11),("P","TP Rencana",11),("Q","Exit Aktual",11),
 ("R","Lot Saran",10),("S","Lot Dipakai",11),
 ("T","Risiko $",11),("U","RR Rencana",11),("V","PnL Kotor $",12),("W","Biaya $",10),
 ("X","PnL Bersih $",12),("Y","R Hasil",9),("Z","Hasil",9),("AA","Durasi (mnt)",11),
 ("AB","Harga Terburuk",13),("AC","Harga Terbaik",13),("AD","MAE (R)",9),("AE","MFE (R)",9),
 ("AF","Emosi Sebelum Entry",18),("AG","Kondisi Fisik",13),("AH","Keyakinan (1-5)",11),
 ("AI","Sesuai Checklist?",13),("AJ","Kesalahan",18),("AK","Catatan",40),("AL","⚠️ Cek Revenge",13),
 ("AM","Link Sebelum",22),("AN","Gambar Sebelum",30),("AO","Link Sesudah",22),("AP","Gambar Sesudah",30),
 ("AQ","Lolos Filter",10)]
for a,b,txt,col in [("A","G","IDENTITAS","1F2937"),("H","M","SETUP & KONTEKS","4C1D95"),
  ("N","S","HARGA & UKURAN","1E3A8A"),("T","AA","HITUNGAN OTOMATIS","065F46"),
  ("AB","AE","MAE / MFE","7C2D12"),("AF","AK","PSIKOLOGI & EKSEKUSI","831843"),
  ("AL","AL","DETEKSI","7F1D1D"),("AM","AP","BUKTI","134E4A"),("AQ","AQ","BANTU","6B7280")]:
    j.merge_cells(f"{a}1:{b}1"); hdr(j,f"{a}1",txt,bg=col,size=9)
for L,t,w in COLS: hdr(j,f"{L}2",t,bg=INK2,size=9); j.column_dimensions[L].width=w
j.freeze_panes="F3"; j.row_dimensions[1].height=18; j.row_dimensions[2].height=34
AUTO=set("AERTUVWXYZ")|{"AA","AD","AE","AL","AN","AP","AQ"}
FMT={**{c:"0.00###" for c in ("N","O","P","Q","AB","AC")},
     **{c:"$#,##0.00" for c in ("T","V","W","X")},
     **{c:"0.00" for c in ("R","S","U","Y","AD","AE")},
     "B":"dd/mm/yyyy","C":"hh:mm","D":"hh:mm","AA":"0","AQ":"0"}
VL=lambda n,col: f'VLOOKUP($F{n},{INSTR},{col},FALSE)'
for n in range(FIRST,LAST+1):
    j.row_dimensions[n].height=58
    f={}
    f["A"]=f'=IF($B{n}="","",ROW()-2)'
    f["E"]=(f'=IF($C{n}="","",IF(AND($C{n}>=TIME(14,0,0),$C{n}<TIME(19,30,0)),"London",'
            f'IF(AND($C{n}>=TIME(19,30,0),$C{n}<TIME(23,0,0)),"Overlap LDN+NY",'
            f'IF(OR($C{n}>=TIME(23,0,0),$C{n}<TIME(4,0,0)),"New York","Asia"))))')
    f["R"]=(f'=IFERROR(IF(OR($N{n}="",$O{n}="",$F{n}=""),"",ROUND(({qS}!$B$3*{qS}!$B$4/100)'
            f'/(ABS($N{n}-$O{n})*{VL(n,4)}),2)),"")')
    f["T"]=f'=IFERROR(IF(OR($N{n}="",$O{n}="",$S{n}=""),"",ABS($N{n}-$O{n})*$S{n}*{VL(n,4)}),"")'
    f["U"]=f'=IFERROR(IF(OR($N{n}="",$O{n}="",$P{n}=""),"",ROUND(ABS($P{n}-$N{n})/ABS($N{n}-$O{n}),2)),"")'
    f["V"]=(f'=IFERROR(IF(OR($Q{n}="",$N{n}="",$S{n}=""),"",($Q{n}-$N{n})*IF($G{n}="Buy",1,-1)'
            f'*$S{n}*{VL(n,4)}),"")')
    f["W"]=f'=IFERROR(IF(OR($S{n}="",$F{n}=""),"",$S{n}*{VL(n,5)}),"")'
    f["X"]=f'=IF($V{n}="","",$V{n}-IF($W{n}="",0,$W{n}))'
    f["Y"]=f'=IF(OR($X{n}="",$T{n}="",$T{n}=0),"",ROUND($X{n}/$T{n},2))'
    f["Z"]=f'=IF($X{n}="","",IF($X{n}>0,"Win",IF($X{n}<0,"Loss","BE")))'
    f["AA"]=f'=IF(OR($C{n}="",$D{n}=""),"",ROUND(MOD($D{n}-$C{n},1)*1440,0))'
    f["AD"]=(f'=IFERROR(IF(OR($AB{n}="",$T{n}="",$T{n}=0),"",ROUND(ABS($N{n}-$AB{n})*$S{n}*{VL(n,4)}/$T{n},2)),"")')
    f["AE"]=(f'=IFERROR(IF(OR($AC{n}="",$T{n}="",$T{n}=0),"",ROUND(ABS($AC{n}-$N{n})*$S{n}*{VL(n,4)}/$T{n},2)),"")')
    f["AL"]='=""' if n==FIRST else (f'=IF(OR($C{n}="",$B{n}=""),"",IF(AND($Z{n-1}="Loss",$B{n}=$B{n-1},'
                                    f'MOD($C{n}-$D{n-1},1)*1440<{qS}!$B$9),"⚠️ Revenge",""))')
    f["AQ"]=(f'=IF($Z{n}="",0,IF(AND(OR({qD}!$B$4="(Semua)",$F{n}={qD}!$B$4),'
             f'OR({qD}!$B$5="(Semua)",$H{n}={qD}!$B$5),OR({qD}!$B$6="(Semua)",$E{n}={qD}!$B$6),'
             f'OR({qD}!$B$7="(Semua)",$AF{n}={qD}!$B$7),OR({qD}!$B$8="(Semua)",$AG{n}={qD}!$B$8),'
             f'OR({qD}!$B$9="(Semua)",$K{n}={qD}!$B$9)),1,0))')
    for src,dst in (("AM","AN"),("AO","AP")):
        f[dst]=(rf'=IF(${src}{n}="","",IFERROR(IMAGE(IF(REGEXMATCH(${src}{n},"\.(png|jpg|jpeg|gif)$"),'
                rf'${src}{n},"https://s3.tradingview.com/snapshots/"&LOWER(MID(REGEXEXTRACT(${src}{n},'
                rf'"/x/([A-Za-z0-9]+)"),1,1))&"/"&REGEXEXTRACT(${src}{n},"/x/([A-Za-z0-9]+)")&".png"),1),'
                rf'"⚠️ link tidak dikenali"))')
    for L,_,_ in COLS:
        c=j[f"{L}{n}"]
        if L in f: c.value=f[L]
        if L in FMT: c.number_format=FMT[L]
        c.border=BOX
        c.alignment=Alignment(vertical="center",wrap_text=(L=="AK"),
                              horizontal="center" if L not in ("AK","AM","AO") else "left")
        c.font=Font(size=9,color="374151") if L in AUTO else Font(size=9)
        if L in AUTO: c.fill=fill(GREY)
for L,opts in {"F":"XAUUSD,BTCUSD,EURUSD,GBPUSD,USDJPY","G":"Buy,Sell",
  "H":"First Touch,RBS Retest,SBR Retest,Lainnya","I":"M1,M5,M15",
  "J":"Ya,Tidak","K":"Ya,Tidak","M":"Ya,Tidak","AI":"Ya,Tidak","L":"POC,VAH,VAL,Tidak ada",
  "AF":"Tenang,FOMO,Balas dendam,Ragu,Overconfident,Bosan","AG":"Segar,Biasa,Capek,Ngantuk",
  "AH":"1,2,3,4,5",
  "AJ":"Tidak ada,Geser SL,Entry tanpa plan,Lot kegedean,Revenge trade,Exit kecepetan,Entry telat,Lawan bias,Lainnya"}.items():
    dv=DataValidation(type="list",formula1=f'"{opts}"',allow_blank=True,showDropDown=False)
    j.add_data_validation(dv); dv.add(f"{L}{FIRST}:{L}{LAST}")
rg=lambda L:f"{L}{FIRST}:{L}{LAST}"
for ref,formula,bg,fg in [
 (rg("Z"),f'$Z{FIRST}="Win"',WIN,"065F46"),(rg("Z"),f'$Z{FIRST}="Loss"',LOSS,"991B1B"),
 (rg("Z"),f'$Z{FIRST}="BE"',NEUT,"374151"),
 (rg("Y"),f'AND($Y{FIRST}<>"",$Y{FIRST}>0)',WIN,"065F46"),(rg("Y"),f'AND($Y{FIRST}<>"",$Y{FIRST}<0)',LOSS,"991B1B"),
 (rg("X"),f'AND($X{FIRST}<>"",$X{FIRST}>0)',WIN,"065F46"),(rg("X"),f'AND($X{FIRST}<>"",$X{FIRST}<0)',LOSS,"991B1B"),
 (rg("S"),f'AND($S{FIRST}<>"",$R{FIRST}<>"",OR($S{FIRST}>$R{FIRST}*1.5,$S{FIRST}<$R{FIRST}*0.5))',WARN,"7C2D12"),
 (rg("AL"),f'$AL{FIRST}="⚠️ Revenge"',LOSS,"991B1B"),
 (rg("AJ"),f'AND($AJ{FIRST}<>"",$AJ{FIRST}<>"Tidak ada")',WARN,"7C2D12"),
 (rg("AF"),f'OR($AF{FIRST}="FOMO",$AF{FIRST}="Balas dendam",$AF{FIRST}="Overconfident")',WARN,"7C2D12"),
 (rg("AG"),f'OR($AG{FIRST}="Capek",$AG{FIRST}="Ngantuk")',WARN,"7C2D12")]:
    j.conditional_formatting.add(ref,FormulaRule(formula=[formula],fill=fill(bg),font=Font(bold=True,color=fg,size=9)))
print("✓ Jurnal (43 kolom)")

# ───────────────────────────── HARIAN ─────────────────────────────
h=wb.create_sheet(H); h.sheet_view.showGridLines=False
title(h,"A1",f"📅 REKAP HARIAN — {dt.date(YEAR,MONTH,1).strftime('%B %Y')}",14)
for i,t in enumerate(["Tanggal","Trade","PnL Bersih $","Total R","Win Rate","Status Guardrail","Kumulatif R","Puncak R","Drawdown R"]):
    hdr(h,f"{get_column_letter(1+i)}2",t)
for col,w in zip("ABCDEFGHI",(13,8,14,10,10,20,12,11,12)): h.column_dimensions[col].width=w
JB=f"{qJ}!$B${FIRST}:$B${LAST}"; JX=f"{qJ}!$X${FIRST}:$X${LAST}"
JY=f"{qJ}!$Y${FIRST}:$Y${LAST}"; JZ=f"{qJ}!$Z${FIRST}:$Z${LAST}"
JAL=f"{qJ}!$AL${FIRST}:$AL${LAST}"; JAQ=f"{qJ}!$AQ${FIRST}:$AQ${LAST}"
JAA=f"{qJ}!$AA${FIRST}:$AA${LAST}"; JAD=f"{qJ}!$AD${FIRST}:$AD${LAST}"; JAE=f"{qJ}!$AE${FIRST}:$AE${LAST}"
for dd in range(NDAYS):
    r=3+dd
    h.cell(row=r,column=1,value=dt.date(YEAR,MONTH,1+dd)).number_format="ddd, dd/mm"
    cnt=f'(COUNTIFS({JB},$A{r},{JZ},"Win")+COUNTIFS({JB},$A{r},{JZ},"Loss")+COUNTIFS({JB},$A{r},{JZ},"BE"))'
    h.cell(row=r,column=2,value=f'={cnt}')
    h.cell(row=r,column=3,value=f'=SUMIFS({JX},{JB},$A{r})').number_format="$#,##0.00"
    h.cell(row=r,column=4,value=f'=SUMIFS({JY},{JB},$A{r})').number_format="0.00"
    h.cell(row=r,column=5,value=f'=IFERROR(COUNTIFS({JB},$A{r},{JZ},"Win")/{cnt},"")').number_format="0%"
    h.cell(row=r,column=6,value=(f'=IF($B{r}=0,"—",IF(OR($C{r}<=-{qS}!$B$5,$B{r}>{qS}!$B$6,'
                                 f'COUNTIFS({JB},$A{r},{JAL},"⚠️ Revenge")>0),"🔴 LANGGAR","✅ Aman"))'))
    h.cell(row=r,column=7,value=f'=SUM($D$3:$D{r})').number_format="0.00"
    h.cell(row=r,column=8,value=f'=MAX($G$3:$G{r})').number_format="0.00"
    h.cell(row=r,column=9,value=f'=$H{r}-$G{r}').number_format="0.00"
    for cc in range(1,10):
        c=h.cell(row=r,column=cc); c.border=BOX; c.font=Font(size=9); c.alignment=Alignment(horizontal="center")
        if cc>=7: c.fill=fill(GREY)
h.freeze_panes="A3"; END=2+NDAYS
h.conditional_formatting.add(f"F3:F{END}",FormulaRule(formula=['$F3="🔴 LANGGAR"'],fill=fill(LOSS),font=Font(bold=True,color="991B1B",size=9)))
h.conditional_formatting.add(f"F3:F{END}",FormulaRule(formula=['$F3="✅ Aman"'],fill=fill(WIN),font=Font(color="065F46",size=9)))
for cl in ("C","D"):
    h.conditional_formatting.add(f"{cl}3:{cl}{END}",FormulaRule(formula=[f'AND($B3>0,${cl}3>0)'],font=Font(bold=True,color="065F46",size=9)))
    h.conditional_formatting.add(f"{cl}3:{cl}{END}",FormulaRule(formula=[f'AND($B3>0,${cl}3<0)'],font=Font(bold=True,color="991B1B",size=9)))

# ─────────────────────────── DATA CHART ───────────────────────────
dc=wb.create_sheet(C); dc.sheet_view.showGridLines=False
title(dc,"A1","📈 DATA CHART — bahan mentah grafik",13)
dc["A2"]="Tab ini diisi rumus otomatis dan dipakai oleh grafik di Dashboard. Boleh disembunyikan, jangan dihapus."
dc["A2"].font=Font(italic=True,size=9,color="6B7280")
def tbl(anchor_col, tname, headers, rows_data, widths):
    c0=anchor_col
    dc.cell(row=3,column=c0,value=tname).font=Font(bold=True,size=10,color="FFFFFF")
    dc.cell(row=3,column=c0).fill=fill(INK2)
    for i,ht in enumerate(headers): hdr(dc,f"{get_column_letter(c0+i)}4",ht,bg="4B5563",size=9)
    for i,w in enumerate(widths): dc.column_dimensions[get_column_letter(c0+i)].width=w
    for k,vals in enumerate(rows_data):
        for i,(v,fmt) in enumerate(vals):
            cc=dc.cell(row=5+k,column=c0+i,value=v)
            if fmt: cc.number_format=fmt
            cc.font=Font(size=9); cc.border=BOX
def cat_rows(col_letter, values, extra=("n","exp")):
    JC=f"{qJ}!${col_letter}${FIRST}:${col_letter}${LAST}"
    out=[]
    for k,v in enumerate(values):
        r=5+k
        cnt=(f'(COUNTIFS({JC},"{v}",{JZ},"Win",{JAQ},1)+COUNTIFS({JC},"{v}",{JZ},"Loss",{JAQ},1)'
             f'+COUNTIFS({JC},"{v}",{JZ},"BE",{JAQ},1))')
        row=[(v,None),(f'={cnt}',"0")]
        if "win" in extra: row.append((f'=IFERROR(COUNTIFS({JC},"{v}",{JZ},"Win",{JAQ},1)/{cnt},0)',"0%"))
        row.append((f'=IFERROR(AVERAGEIFS({JY},{JC},"{v}",{JAQ},1),0)',"0.00"))
        out.append(row)
    return out
tbl(1,"T1 · Ekuitas Harian",["Tanggal","Kumulatif R"],
    [[(f'={qH}!$A{3+i}',"dd/mm"),(f'={qH}!$G{3+i}',"0.00")] for i in range(NDAYS)],(11,12))
tbl(4,"T2 · PnL Harian",["Tanggal","PnL $"],
    [[(f'={qH}!$A{3+i}',"dd/mm"),(f'={qH}!$C{3+i}',"0.00")] for i in range(NDAYS)],(11,12))
tbl(7,"T3 · Per Setup",["Setup","N","Win %","Exp R"],
    cat_rows("H",["First Touch","RBS Retest","SBR Retest","Lainnya"],("n","win","exp")),(14,7,8,8))
buckets=[("≤ -1.5",None,-1.5),("-1.5 s/d -1",-1.5,-1.0),("-1 s/d -0.5",-1.0,-0.5),("-0.5 s/d 0",-0.5,0),
         ("0 s/d 0.5",0,0.5),("0.5 s/d 1",0.5,1.0),("1 s/d 2",1.0,2.0),("> 2.0",2.0,None)]
brows=[]
for lbl,lo,hi in buckets:
    if lo is None: cond=f'=COUNTIFS({JY},"<="&{hi},{JAQ},1)'
    elif hi is None: cond=f'=COUNTIFS({JY},">"&{lo},{JAQ},1)'
    else: cond=f'=COUNTIFS({JY},">"&{lo},{JY},"<="&{hi},{JAQ},1)'
    brows.append([(lbl,None),(cond,"0")])
tbl(12,"T4 · Sebaran R",["Rentang R","Jumlah"],brows,(13,9))
tbl(15,"T5 · Per Emosi",["Emosi","N","Exp R"],
    cat_rows("AF",["Tenang","FOMO","Balas dendam","Ragu","Overconfident","Bosan"]),(15,7,8))
tbl(19,"T6 · Per Sesi",["Sesi","N","Exp R"],
    cat_rows("E",["London","Overlap LDN+NY","New York","Asia"]),(16,7,8))
tbl(23,"T7 · Hasil",["Hasil","Jumlah"],
    [[(v,None),(f'=COUNTIFS({JZ},"{v}",{JAQ},1)',"0")] for v in ("Win","Loss","BE")],(9,9))
tbl(26,"T8 · Kondisi Fisik",["Fisik","N","Exp R"],
    cat_rows("AG",["Segar","Biasa","Capek","Ngantuk"]),(11,7,8))
print("✓ Harian + Data Chart")

# ───────────────────────────── DASHBOARD ─────────────────────────────
d=wb.create_sheet(D); d.sheet_view.showGridLines=False
for col,w in zip("ABCDEF",(26,16,13,13,13,20)): d.column_dimensions[col].width=w
title(d,"A1","📊 DASHBOARD",16)
d["A2"]="Ubah dropdown filter → semua metrik, tabel, dan grafik ikut menyesuaikan."
d["A2"].font=Font(italic=True,size=9,color="6B7280")
band(d,3,"🎛️  FILTER INTERAKTIF")
FILTERS=[("Instrumen","(Semua),XAUUSD,BTCUSD,EURUSD,GBPUSD,USDJPY"),
         ("Tipe Setup","(Semua),First Touch,RBS Retest,SBR Retest,Lainnya"),
         ("Sesi","(Semua),London,Overlap LDN+NY,New York,Asia"),
         ("Emosi","(Semua),Tenang,FOMO,Balas dendam,Ragu,Overconfident,Bosan"),
         ("Kondisi Fisik","(Semua),Segar,Biasa,Capek,Ngantuk"),
         ("Bias EMA200 Searah","(Semua),Ya,Tidak")]
for i,(label,opts) in enumerate(FILTERS):
    r=4+i
    c=d.cell(row=r,column=1,value=label); c.font=Font(bold=True,size=10); c.fill=fill(GREY); c.border=BOX
    v=d.cell(row=r,column=2,value="(Semua)")
    v.font=Font(bold=True,size=10,color="1E3A8A"); v.fill=fill("EFF6FF"); v.border=BOX
    v.alignment=Alignment(horizontal="center")
    dv=DataValidation(type="list",formula1=f'"{opts}"',allow_blank=False,showDropDown=False)
    d.add_data_validation(dv); dv.add(f"B{r}")
d["C4"]="← klik sel biru untuk memfilter. \"(Semua)\" = tanpa filter."
d["C4"].font=Font(italic=True,size=9,color="6B7280")
NALL=f'(COUNTIFS({JZ},"Win",{JAQ},1)+COUNTIFS({JZ},"Loss",{JAQ},1)+COUNTIFS({JZ},"BE",{JAQ},1))'
band(d,11,"📌  RINGKASAN (mengikuti filter)")
for cell,label,formula,fmt in [
 ("A12","Total Trade",f'={NALL}',"0"),
 ("A13","Win / Loss / BE",f'=COUNTIFS({JZ},"Win",{JAQ},1)&" / "&COUNTIFS({JZ},"Loss",{JAQ},1)&" / "&COUNTIFS({JZ},"BE",{JAQ},1)',"@"),
 ("A14","Win Rate",f'=IFERROR(COUNTIFS({JZ},"Win",{JAQ},1)/{NALL},"")',"0.0%"),
 ("A15","Expectancy (R)",f'=IFERROR(AVERAGEIFS({JY},{JAQ},1),"")',"0.000"),
 ("A16","Profit Factor",f'=IFERROR(SUMIFS({JX},{JAQ},1,{JX},">0")/ABS(SUMIFS({JX},{JAQ},1,{JX},"<0")),"")',"0.00"),
 ("D12","Total PnL Bersih",f'=SUMIFS({JX},{JAQ},1)',"$#,##0.00"),
 ("D13","Total Biaya Dibayar",f'=SUMIFS({qJ}!$W${FIRST}:$W${LAST},{JAQ},1)',"$#,##0.00"),
 ("D14","Total R",f'=SUMIFS({JY},{JAQ},1)',"0.00"),
 ("D15","Max Drawdown R (sebulan)",f'=MAX({qH}!$I$3:$I${2+NDAYS})',"0.00"),
 ("D16","Rata-rata Durasi (mnt)",f'=IFERROR(AVERAGEIFS({JAA},{JAQ},1),"")',"0")]:
    col=cell[0]; row=int(cell[1:]); vcol=get_column_letter(ord(col)-64+1)
    c=d[f"{col}{row}"]; c.value=label; c.font=Font(bold=True,size=10); c.fill=fill(GREY); c.border=BOX
    v=d[f"{vcol}{row}"]; v.value=formula; v.number_format=fmt; v.border=BOX
    v.font=Font(bold=True,size=11,color=INK); v.alignment=Alignment(horizontal="center")
PCT=f'SUM({JX})/{qS}!$B$7'; BARN=f'MAX(0,MIN(20,ROUND({PCT}*20,0)))'
band(d,18,"🎯  PROGRESS TARGET BULANAN (seluruh bulan, tidak ikut filter)")
d["A19"]="Tercapai"; d["A19"].font=Font(bold=True,size=10)
d["B19"]=f'=IFERROR({PCT},"")'; d["B19"].number_format="0.0%"; d["B19"].font=Font(bold=True,size=12)
d["C19"]=f'=IFERROR(REPT("█",{BARN})&REPT("░",20-{BARN}),"")'; d["C19"].font=Font(size=11,color="065F46")
d["A20"]="Setara Rupiah"; d["A20"].font=Font(bold=True,size=10)
d["B20"]=f'=SUM({JX})*{qS}!$B$8'; d["B20"].number_format='"Rp"#,##0'; d["B20"].font=Font(bold=True,size=11,color="065F46")
def block(row,heading,col,values,note=""):
    band(d,row,heading)
    if note:
        d.merge_cells(f"A{row+1}:F{row+1}")
        n=d[f"A{row+1}"]; n.value=note; n.font=Font(italic=True,size=9,color="6B7280"); row+=1
    hrow=row+1
    for i,t in enumerate(["Kategori","N","Win %","Exp R","Total R","Visual Exp R"]):
        hdr(d,f"{get_column_letter(1+i)}{hrow}",t,bg="4B5563",size=9)
    JC=f"{qJ}!${col}${FIRST}:${col}${LAST}"
    for k,val in enumerate(values):
        r=hrow+1+k
        d.cell(row=r,column=1,value=val).font=Font(size=9,bold=True)
        cnt=(f'(COUNTIFS({JC},$A{r},{JZ},"Win",{JAQ},1)+COUNTIFS({JC},$A{r},{JZ},"Loss",{JAQ},1)'
             f'+COUNTIFS({JC},$A{r},{JZ},"BE",{JAQ},1))')
        d.cell(row=r,column=2,value=f'={cnt}').number_format="0"
        d.cell(row=r,column=3,value=f'=IFERROR(COUNTIFS({JC},$A{r},{JZ},"Win",{JAQ},1)/{cnt},"")').number_format="0%"
        d.cell(row=r,column=4,value=f'=IFERROR(AVERAGEIFS({JY},{JC},$A{r},{JAQ},1),"")').number_format="0.00"
        d.cell(row=r,column=5,value=f'=IFERROR(SUMIFS({JY},{JC},$A{r},{JAQ},1),"")').number_format="0.00"
        d.cell(row=r,column=6,value=(f'=IF($B{r}=0,"",IF($D{r}>=0,REPT("▉",MIN(14,ROUND($D{r}*14,0))),'
                                     f'REPT("▒",MIN(14,ROUND(-$D{r}*14,0)))))'))
        for cc in range(1,7):
            cx=d.cell(row=r,column=cc); cx.border=BOX; cx.font=Font(size=9)
            if cc>1: cx.alignment=Alignment(horizontal="center")
        d.conditional_formatting.add(f"D{r}:D{r}",FormulaRule(formula=[f'AND($B{r}>0,$D{r}>0)'],fill=fill(WIN),font=Font(bold=True,color="065F46",size=9)))
        d.conditional_formatting.add(f"D{r}:D{r}",FormulaRule(formula=[f'AND($B{r}>0,$D{r}<0)'],fill=fill(LOSS),font=Font(bold=True,color="991B1B",size=9)))
    return hrow+1+len(values)+1
r=22
r=block(r,"①  PER TIPE SETUP","H",["First Touch","RBS Retest","SBR Retest","Lainnya"],
        "Menjawab pertanyaan yang backtest Juli gantung: retest beneran lebih bagus dari first touch?")
r=block(r,"②  PER SESI","E",["London","Overlap LDN+NY","New York","Asia"],
        "Kamu mulai 19:00 WIB. Sesi mana yang beneran bayar?")
r=block(r,"③  PER EMOSI SEBELUM ENTRY","AF",["Tenang","FOMO","Balas dendam","Ragu","Overconfident","Bosan"],
        "Ini yang paling sering mengubah hasil orang. Lihat selisih Tenang vs FOMO.")
r=block(r,"④  PER KONDISI FISIK","AG",["Segar","Biasa","Capek","Ngantuk"],
        "Kamu trading malam setelah kerja 9–5. Cek apakah 'Capek' punya harga.")
r=block(r,"⑤  BIAS EMA200 SEARAH?","K",["Ya","Tidak"],
        "Backtest 31 Agu tidak bisa memutuskan ini (CI lewat nol). Data live kamu yang menjawab.")
r=block(r,"⑥  SESUAI CHECKLIST?","AI",["Ya","Tidak"],
        "Kalau 'Tidak' ternyata lebih untung, checklist-nya yang salah — bukan kamu.")
r=block(r,"⑦  PER INSTRUMEN","F",["XAUUSD","BTCUSD","EURUSD","GBPUSD","USDJPY"])
band(d,r,"⑧  ANALISA MAE / MFE — SL kesempitan atau TP kecepetan?"); r+=1
for lbl,fm,note in [
  ("Rata-rata MAE trade WIN",f'=IFERROR(AVERAGEIFS({JAD},{JZ},"Win",{JAQ},1),"")',"Kalau > 0.7R: SL kamu nyaris kena terus. Pertimbangkan SL sedikit lebih lebar."),
  ("Rata-rata MAE trade LOSS",f'=IFERROR(AVERAGEIFS({JAD},{JZ},"Loss",{JAQ},1),"")',"Pembanding."),
  ("Rata-rata MFE trade WIN",f'=IFERROR(AVERAGEIFS({JAE},{JZ},"Win",{JAQ},1),"")',"Kalau jauh di atas R hasilmu: keluar kecepetan, profit ditinggal di meja."),
  ("Rata-rata MFE trade LOSS",f'=IFERROR(AVERAGEIFS({JAE},{JZ},"Loss",{JAQ},1),"")',"Kalau > 1.0R: sering sudah untung 1R lalu balik rugi. Pertimbangkan geser ke BE.")]:
    d.cell(row=r,column=1,value=lbl).font=Font(bold=True,size=9)
    d.cell(row=r,column=2,value=fm).number_format="0.00"
    d.cell(row=r,column=2).alignment=Alignment(horizontal="center")
    d.merge_cells(f"C{r}:F{r}"); d.cell(row=r,column=3,value=note).font=Font(italic=True,size=9,color="6B7280")
    for cc in (1,2): d.cell(row=r,column=cc).border=BOX
    r+=1
r+=1
band(d,r,"⑨  KESALAHAN PALING MAHAL"); r+=1
for i,t in enumerate(["Kesalahan","Jumlah","","Total R","PnL $",""]):
    if t: hdr(d,f"{get_column_letter(1+i)}{r}",t,bg="4B5563",size=9)
JAJ=f"{qJ}!$AJ${FIRST}:$AJ${LAST}"
for k,e in enumerate(["Geser SL","Entry tanpa plan","Lot kegedean","Revenge trade","Exit kecepetan","Entry telat","Lawan bias","Lainnya"]):
    rr=r+1+k
    d.cell(row=rr,column=1,value=e).font=Font(size=9,bold=True)
    d.cell(row=rr,column=2,value=f'=COUNTIFS({JAJ},$A{rr},{JAQ},1)').number_format="0"
    d.cell(row=rr,column=4,value=f'=IFERROR(SUMIFS({JY},{JAJ},$A{rr},{JAQ},1),"")').number_format="0.00"
    d.cell(row=rr,column=5,value=f'=IFERROR(SUMIFS({JX},{JAJ},$A{rr},{JAQ},1),"")').number_format="$#,##0.00"
    for cc in (1,2,4,5):
        cx=d.cell(row=rr,column=cc); cx.border=BOX; cx.font=Font(size=9)
        if cc>1: cx.alignment=Alignment(horizontal="center")
    d.conditional_formatting.add(f"E{rr}:E{rr}",FormulaRule(formula=[f'AND($B{rr}>0,$E{rr}<0)'],fill=fill(LOSS),font=Font(bold=True,color="991B1B",size=9)))
r=r+1+8+1
d.merge_cells(f"A{r}:F{r+2}")
w=d[f"A{r}"]
w.value=("⚠️ INGAT: 1 bulan ≈ 40–100 trade — belum cukup untuk kesimpulan statistik.\n"
         "Beda win rate 10% pada 40 trade masih sangat mungkin kebetulan. Baca sebagai PETUNJUK ARAH.\n"
         "Kumpulkan 3–6 bulan sebelum membuang satu jenis setup.")
w.font=Font(bold=True,size=9,color="7C2D12"); w.fill=fill(WARN)
w.alignment=Alignment(wrap_text=True,vertical="center"); w.border=BOX

# ───────────────────────────── REVIEW ─────────────────────────────
v=wb.create_sheet(R); v.sheet_view.showGridLines=False
v.column_dimensions["A"].width=30; v.column_dimensions["B"].width=95
title(v,"A1","🔍 REVIEW MINGGUAN — isi tiap Sabtu, 10 menit",14)
v["A2"]="Jurnal yang dibaca ulang jauh lebih berharga daripada jurnal yang cuma diisi."
v["A2"].font=Font(italic=True,size=9,color="6B7280")
prompts=["Berapa total R minggu ini? Naik atau turun dari minggu lalu?",
 "Setup mana yang paling menghasilkan? Mana yang paling merugikan?",
 "Berapa kali aku melanggar checklist sendiri? Apa pemicunya?",
 "Emosi apa yang paling sering muncul saat aku rugi?",
 "Ada guardrail yang jebol (batas rugi / max trade / revenge)? Kenapa?",
 "Satu hal yang akan aku ubah minggu depan (SATU saja, spesifik):"]
row=4
for wk in range(1,5):
    v.merge_cells(f"A{row}:B{row}")
    c=v[f"A{row}"]; c.value=f"MINGGU {wk}"; c.font=Font(bold=True,size=12,color="FFFFFF")
    c.fill=fill(INK); c.alignment=Alignment(horizontal="center"); row+=1
    for p in prompts:
        q=v.cell(row=row,column=1,value=p); q.font=Font(size=9,bold=True); q.fill=fill(GREY)
        q.alignment=Alignment(wrap_text=True,vertical="center"); q.border=BOX
        a=v.cell(row=row,column=2); a.border=BOX; a.alignment=Alignment(wrap_text=True,vertical="top")
        v.row_dimensions[row].height=34; row+=1
    row+=1


# ───────────────────── IMPORT CSV BROKER (opsional) ─────────────────────
# Hanya mengisi kolom yang MEMANG ada di export broker. Kolom penilaian
# (setup, bias, emosi, MAE/MFE, screenshot) sengaja dibiarkan kosong.
import csv as _csv, os as _os
CSV_IMPORT = "/Users/wahyusetiawan/Downloads/31_08_2026-31_08_2026.csv"
TZ_JAM = 7            # CSV bertanda UTC -> WIB (+7)
if CSV_IMPORT and _os.path.exists(CSV_IMPORT):
    tr=[r for r in _csv.DictReader(open(CSV_IMPORT,encoding="utf-8-sig")) if r.get("ticket")]
    tr.sort(key=lambda r: r["opening_time_utc"])      # urut naik: perlu utk deteksi revenge
    num=lambda v: float(v) if v not in (None,"") else None
    for i,t in enumerate(tr):
        n=FIRST+i
        if n>LAST: break
        o=dt.datetime.fromisoformat(t["opening_time_utc"])+dt.timedelta(hours=TZ_JAM)
        c=dt.datetime.fromisoformat(t["closing_time_utc"])+dt.timedelta(hours=TZ_JAM)
        j[f"B{n}"]=o.date()
        j[f"C{n}"]=o.time()
        j[f"D{n}"]=c.time()
        j[f"F{n}"]=t["symbol"]
        j[f"G{n}"]="Buy" if t["type"].lower()=="buy" else "Sell"
        j[f"N{n}"]=num(t["opening_price"])
        if num(t["stop_loss"]):    j[f"O{n}"]=num(t["stop_loss"])
        if num(t["take_profit"]):  j[f"P{n}"]=num(t["take_profit"])
        j[f"Q{n}"]=num(t["closing_price"])
        j[f"S{n}"]=num(t["lots"])
        j[f"AK{n}"]=f"tiket {t['ticket']} · impor otomatis dari CSV broker"
        if not num(t["stop_loss"]):
            j[f"O{n}"]=None
            j[f"AK{n}"]=(f"tiket {t['ticket']} · impor CSV · ⚠️ TANPA SL di broker — "
                         f"isi SL yang kamu niatkan biar Risiko $ dan R Hasil bisa terhitung")
    print(f"✓ Impor {min(len(tr),LAST-FIRST+1)} trade dari CSV broker")

wb.save(OUT)
print("✓ Dashboard + Review")

# ───────────────────────── APPS SCRIPT (grafik) ─────────────────────────
E=4+NDAYS
gs=f'''/**
 * Pasang grafik native di tab Dashboard.
 * Cara pakai: Extensions > Apps Script > paste semua ini > Save > pilih buatGrafik > Run.
 * Aman dijalankan berkali-kali — grafik lama dihapus dulu, tidak menumpuk.
 */
function buatGrafik() {{
  const ss   = SpreadsheetApp.getActiveSpreadsheet();
  const dash = ss.getSheetByName('{D}');
  const src  = ss.getSheetByName('{C}');
  if (!dash || !src) {{
    SpreadsheetApp.getUi().alert('Tab Dashboard atau Data Chart tidak ketemu. Pastikan nama tab belum diubah.');
    return;
  }}
  dash.getCharts().forEach(c => dash.removeChart(c));

  const buat = (type, ranges, row, col, judul, opts) => {{
    let b = dash.newChart().setChartType(type);
    ranges.forEach(r => b = b.addRange(src.getRange(r)));
    b = b.setPosition(row, col, 0, 0)
         .setOption('title', judul)
         .setOption('width', 460).setOption('height', 260)
         .setOption('titleTextStyle', {{fontSize: 12, bold: true}})
         .setOption('legend', {{position: 'none'}});
    for (const k in (opts || {{}})) b = b.setOption(k, opts[k]);
    dash.insertChart(b.build());
  }};

  const CH = Charts.ChartType;
  buat(CH.LINE,   ['A4:B{E}'], 3,  8, 'Kurva Ekuitas — R kumulatif harian',
       {{colors: ['#00bcd4'], curveType: 'none', pointSize: 3}});
  buat(CH.COLUMN, ['D4:E{E}'], 17, 8, 'PnL Harian ($)', {{colors: ['#1E3A8A']}});
  buat(CH.BAR,    ['G4:G8', 'J4:J8'], 31, 8, 'Expectancy R per Tipe Setup', {{colors: ['#065F46']}});
  buat(CH.COLUMN, ['L4:M12'], 3,  16, 'Sebaran Hasil (R)', {{colors: ['#7C2D12']}});
  buat(CH.BAR,    ['O4:O10', 'Q4:Q10'], 17, 16, 'Expectancy R per Emosi', {{colors: ['#831843']}});
  buat(CH.PIE,    ['W4:X7'], 31, 16, 'Win / Loss / BE',
       {{colors: ['#10B981', '#EF4444', '#9CA3AF'], legend: {{position: 'right'}}}});

  SpreadsheetApp.getActiveSpreadsheet().toast('6 grafik terpasang di Dashboard.', 'Selesai', 5);
}}
'''
open(GS,"w",encoding="utf-8").write(gs)
print("SAVED:", OUT)
print("SAVED:", GS)
