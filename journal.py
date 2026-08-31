# -*- coding: utf-8 -*-
"""
Jurnal trading — SATU file master, append-only.

  python journal.py build              -> bikin master (menolak kalau sudah ada)
  python journal.py add <file.csv>     -> tambah trade baru ke master yang sama
  python journal.py add <csv> --tz -1  -> ubah offset jam (default +7 UTC->WIB)

Aturan: baris lama TIDAK PERNAH disentuh. Trade yang nomor tiketnya sudah ada
akan dilewati, jadi CSV yang sama dikirim dua kali tidak bikin duplikat.
"""
import sys, os, csv, datetime as dt
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

BASE = "/Users/wahyusetiawan/Documents/tradingview/snd"
OUT  = f"{BASE}/trading-journal-MASTER.xlsx"
GS   = f"{BASE}/journal-charts.gs"
FIRST, LAST = 3, 502      # kapasitas 500 trade
DFIRST, DLAST = 3, 152    # 150 baris rekap harian

G="📋 Panduan"; S="⚙️ Setelan"; J="📒 Jurnal"; H="📅 Harian"
C="📈 Data Chart"; D="📊 Dashboard"; R="🔍 Review"
qJ,qS,qH,qD = f"'{J}'", f"'{S}'", f"'{H}'", f"'{D}'"
INK="1F2937"; INK2="374151"; GREY="F3F4F6"
WIN="D1FAE5"; LOSS="FEE2E2"; WARN="FEF3C7"; NEUT="E5E7EB"
def fill(c): return PatternFill("solid", fgColor=c)
_t=Side(style="thin",color="D1D5DB"); BOX=Border(left=_t,right=_t,top=_t,bottom=_t)
def hdr(ws,cell,text,bg=INK,fg="FFFFFF",size=10):
    c=ws[cell]; c.value=text; c.font=Font(bold=True,color=fg,size=size); c.fill=fill(bg)
    c.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True); c.border=BOX; return c
def title(ws,cell,text,size=14):
    c=ws[cell]; c.value=text; c.font=Font(bold=True,size=size,color=INK); return c
def band(ws,row,text,span="A:F"):
    a,b=span.split(":"); ws.merge_cells(f"{a}{row}:{b}{row}")
    c=ws[f"{a}{row}"]; c.value=text; c.font=Font(bold=True,size=11,color="FFFFFF"); c.fill=fill(INK2); return c

# rentang yang sering dipakai
JB=f"{qJ}!$B${FIRST}:$B${LAST}"; JX=f"{qJ}!$X${FIRST}:$X${LAST}"
JY=f"{qJ}!$Y${FIRST}:$Y${LAST}"; JZ=f"{qJ}!$Z${FIRST}:$Z${LAST}"
JAL=f"{qJ}!$AL${FIRST}:$AL${LAST}"; JAQ=f"{qJ}!$AQ${FIRST}:$AQ${LAST}"
JAA=f"{qJ}!$AA${FIRST}:$AA${LAST}"; JAD=f"{qJ}!$AD${FIRST}:$AD${LAST}"
JAE=f"{qJ}!$AE${FIRST}:$AE${LAST}"; JAJ=f"{qJ}!$AJ${FIRST}:$AJ${LAST}"
INSTR=f"{qS}!$A$14:$F$20"

def bikin_panduan(wb):
    g=wb.active; g.title=G
    g.column_dimensions["A"].width=4; g.column_dimensions["B"].width=118
    g.sheet_view.showGridLines=False
    title(g,"B2","📋 JURNAL TRADING — FILE MASTER",16)
    baris=[("",""),
     ("h","① FILE INI SATU-SATUNYA — TIDAK PERNAH DIGANTI"),
     ("t","Semua bulan menumpuk di sini. Tiap ada CSV broker baru, trade ditambahkan di baris"),
     ("t","kosong berikutnya. Baris lama beserta catatan/emosi/screenshot kamu TIDAK disentuh."),
     ("t","Trade dengan nomor tiket yang sudah ada otomatis dilewati — aman kirim CSV dua kali."),
     ("",""),
     ("w","⚠️ BACA INI DULU — SOAL SINKRONISASI"),
     ("t","Anotasi manualmu (emosi, setup, screenshot) hidup di Google Sheets, bukan di file lokal."),
     ("t","Kalau kamu re-import file master mentah, anotasi itu HILANG tertimpa."),
     ("t","Alur yang benar setelah import pertama:"),
     ("t","   • Trade baru ditambahkan → salin HANYA baris barunya ke Sheets (nomor barisnya"),
     ("t","     akan disebutkan), atau"),
     ("t","   • Export Sheets kamu (File → Download → .xlsx), kirim balik, biar jadi master baru."),
     ("t","JANGAN re-import penuh kalau kamu sudah mengisi kolom penilaian."),
     ("",""),
     ("h","② IMPORT PERTAMA KE GOOGLE SHEETS"),
     ("t","sheets.google.com → File → Import → Upload → \"Create new spreadsheet\"."),
     ("t","Lalu File → Settings → Locale → Indonesia (biar tanggal dd/mm terbaca benar)."),
     ("",""),
     ("h","③ PASANG GRAFIK (sekali saja, ~2 menit)"),
     ("t","Extensions → Apps Script → paste isi journal-charts.gs → Save → pilih buatGrafik → Run."),
     ("t","6 grafik muncul di tab Dashboard dan ikut update tiap kamu isi trade."),
     ("",""),
     ("h","④ KOLOM YANG DIISI OTOMATIS DARI CSV BROKER"),
     ("t","Tanggal, Jam Masuk/Keluar, Instrumen, Arah, Entry, SL, TP, Exit, Lot, Tiket."),
     ("t","Sisanya kamu yang isi: Setup, TF, Bias, SVP, News, Harga Terburuk/Terbaik,"),
     ("t","Emosi, Kondisi Fisik, Keyakinan, Checklist, Kesalahan, Screenshot."),
     ("",""),
     ("h","⑤ FILTER INTERAKTIF DI DASHBOARD"),
     ("t","6 dropdown di atas Dashboard. Ubah satu → semua metrik, tabel, dan grafik menyesuaikan."),
     ("t","Contoh: Emosi = FOMO → lihat win rate & expectancy kamu khusus saat FOMO."),
     ("",""),
     ("h","⑥ TAB HARIAN MENGISI DIRI SENDIRI"),
     ("t","Daftar tanggalnya muncul otomatis dari trade yang ada — tidak terkunci ke satu bulan."),
     ("",""),
     ("w","⚠️ PERINGATAN JUMLAH SAMPEL"),
     ("t","Di bawah ~100 trade, angka Dashboard adalah PETUNJUK ARAH, bukan vonis."),
     ("t","Beda win rate 10% pada 40 trade masih sangat mungkin kebetulan."),
    ]
    r=3
    for kind,txt in baris:
        c=g.cell(row=r,column=2,value=txt)
        if kind=="h": c.font=Font(bold=True,size=11,color="FFFFFF"); c.fill=fill(INK2)
        elif kind=="w": c.font=Font(bold=True,size=11,color="7C2D12"); c.fill=fill(WARN)
        else: c.font=Font(size=10,color=INK)
        c.alignment=Alignment(vertical="center"); r+=1

def bikin_setelan(wb):
    s=wb.create_sheet(S)
    s.column_dimensions["A"].width=34
    for col,w in zip("BCDEF",(16,18,26,20,10)): s.column_dimensions[col].width=w
    s.sheet_view.showGridLines=False
    title(s,"A1","⚙️ SETELAN — isi sekali",14)
    for i,(label,val,fmt) in enumerate([
        ("Modal Awal (USD)",5600,"$#,##0"),("Risiko per Trade (%)",1.0,"0.0"),
        ("Batas Rugi Harian (USD)",100,"$#,##0"),("Max Trade per Hari",10,"0"),
        ("Target Profit Bulanan (USD)",1000,"$#,##0"),("Kurs USD → IDR",16000,"#,##0"),
        ("Jeda Min Setelah Loss (menit)",10,"0")]):
        rr=3+i
        c=s.cell(row=rr,column=1,value=label); c.font=Font(bold=True,size=10); c.fill=fill(GREY); c.border=BOX
        v=s.cell(row=rr,column=2,value=val); v.number_format=fmt; v.border=BOX
        v.font=Font(bold=True,color="065F46"); v.fill=fill("ECFDF5"); v.alignment=Alignment(horizontal="center")
    s["C3"]="← angka hijau ini tebakan awal dari data 31 Agu. Ganti dengan angka aslimu."
    s["C3"].font=Font(italic=True,size=9,color="6B7280")
    title(s,"A11","SPESIFIKASI INSTRUMEN",12)
    s["A12"]="Dipakai rumus PnL. Rentang VLOOKUP sampai baris 20 — ada 2 baris kosong untuk instrumen tambahan."
    s["A12"].font=Font(italic=True,size=9,color="6B7280")
    for i,t in enumerate(["Instrumen","Ukuran Kontrak","Pembagi Konversi","Nilai per 1.00 Gerak/Lot (USD)","Biaya per Lot (USD)","Digit"]):
        hdr(s,f"{get_column_letter(1+i)}13",t)
    for i,(nm,cs,conv,cost,dg) in enumerate([("XAUUSD",100,1,11,2),("BTCUSD",1,1,8.75,2),
            ("EURUSD",100000,1,10,5),("GBPUSD",100000,1,15,5),("USDJPY",100000,155,6.5,3)]):
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

COLS=[("A","No",6),("B","Tanggal",11),("C","Jam Masuk",10),("D","Jam Keluar",10),("E","Sesi",15),
 ("F","Instrumen",11),("G","Arah",8),("H","Tipe Setup",14),("I","TF Eksekusi",11),
 ("J","Bias M15 Searah?",13),("K","Bias EMA200 Searah?",14),("L","Konfluensi SVP",13),("M","News Besar?",11),
 ("N","Entry",11),("O","Stop Loss",11),("P","TP Rencana",11),("Q","Exit Aktual",11),
 ("R","Lot Saran",10),("S","Lot Dipakai",11),
 ("T","Risiko $",11),("U","RR Rencana",11),("V","PnL Kotor $",12),("W","Biaya $",10),
 ("X","PnL Bersih $",12),("Y","R Hasil",9),("Z","Hasil",9),("AA","Durasi (mnt)",11),
 ("AB","Harga Terburuk",13),("AC","Harga Terbaik",13),("AD","MAE (R)",9),("AE","MFE (R)",9),
 ("AF","Emosi Sebelum Entry",18),("AG","Kondisi Fisik",13),("AH","Keyakinan (1-5)",11),
 ("AI","Sesuai Checklist?",13),("AJ","Kesalahan",18),("AK","Catatan",40),("AL","⚠️ Cek Revenge",13),
 ("AM","Link Sebelum",22),("AN","Gambar Sebelum",30),("AO","Link Sesudah",22),("AP","Gambar Sesudah",30),
 ("AQ","Lolos Filter",10),("AR","Tiket Broker — jangan diubah",20)]
TIKET_COL="AR"

def bikin_jurnal(wb):
    j=wb.create_sheet(J)
    for a,b,txt,col in [("A","G","IDENTITAS","1F2937"),("H","M","SETUP & KONTEKS","4C1D95"),
      ("N","S","HARGA & UKURAN","1E3A8A"),("T","AA","HITUNGAN OTOMATIS","065F46"),
      ("AB","AE","MAE / MFE","7C2D12"),("AF","AK","PSIKOLOGI & EKSEKUSI","831843"),
      ("AL","AL","DETEKSI","7F1D1D"),("AM","AP","BUKTI","134E4A"),("AQ","AR","SISTEM","6B7280")]:
        j.merge_cells(f"{a}1:{b}1"); hdr(j,f"{a}1",txt,bg=col,size=9)
    for L,t,w in COLS: hdr(j,f"{L}2",t,bg=INK2,size=9); j.column_dimensions[L].width=w
    j.freeze_panes="F3"; j.row_dimensions[1].height=18; j.row_dimensions[2].height=34
    AUTO=set("AERTUVWXYZ")|{"AA","AD","AE","AL","AN","AP","AQ","AR"}
    FMT={**{c:"0.00###" for c in ("N","O","P","Q","AB","AC")},
         **{c:"$#,##0.00" for c in ("T","V","W","X")},
         **{c:"0.00" for c in ("R","S","U","Y","AD","AE")},
         "B":"dd/mm/yyyy","C":"hh:mm","D":"hh:mm","AA":"0","AQ":"0","AR":"@"}
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
        f["AD"]=f'=IFERROR(IF(OR($AB{n}="",$T{n}="",$T{n}=0),"",ROUND(ABS($N{n}-$AB{n})*$S{n}*{VL(n,4)}/$T{n},2)),"")'
        f["AE"]=f'=IFERROR(IF(OR($AC{n}="",$T{n}="",$T{n}=0),"",ROUND(ABS($AC{n}-$N{n})*$S{n}*{VL(n,4)}/$T{n},2)),"")'
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
     (rg("O"),f'AND($N{FIRST}<>"",$O{FIRST}="")',WARN,"7C2D12"),
     (rg("AL"),f'$AL{FIRST}="⚠️ Revenge"',LOSS,"991B1B"),
     (rg("AJ"),f'AND($AJ{FIRST}<>"",$AJ{FIRST}<>"Tidak ada")',WARN,"7C2D12"),
     (rg("AF"),f'OR($AF{FIRST}="FOMO",$AF{FIRST}="Balas dendam",$AF{FIRST}="Overconfident")',WARN,"7C2D12"),
     (rg("AG"),f'OR($AG{FIRST}="Capek",$AG{FIRST}="Ngantuk")',WARN,"7C2D12")]:
        j.conditional_formatting.add(ref,FormulaRule(formula=[formula],fill=fill(bg),font=Font(bold=True,color=fg,size=9)))

DCROWS=150
def bikin_harian(wb):
    h=wb.create_sheet(H); h.sheet_view.showGridLines=False
    title(h,"A1","📅 REKAP HARIAN — daftar tanggal muncul otomatis dari trade yang ada",13)
    for i,t in enumerate(["Tanggal","Trade","PnL Bersih $","Total R","Win Rate","Status Guardrail","Kumulatif R","Puncak R","Drawdown R"]):
        hdr(h,f"{get_column_letter(1+i)}2",t)
    for col,w in zip("ABCDEFGHI",(13,8,14,10,10,20,12,11,12)): h.column_dimensions[col].width=w
    # kolom A: satu rumus yang "spill" ke bawah -> A4 dst WAJIB dibiarkan kosong
    h[f"A{DFIRST}"]=f'=IFERROR(SORT(UNIQUE(FILTER({JB},{JB}<>""))),"")'
    h[f"A{DFIRST}"].number_format="ddd, dd/mm"
    for r in range(DFIRST,DLAST+1):
        cnt=f'(COUNTIFS({JB},$A{r},{JZ},"Win")+COUNTIFS({JB},$A{r},{JZ},"Loss")+COUNTIFS({JB},$A{r},{JZ},"BE"))'
        g=lambda v: f'=IF($A{r}="","",{v})'
        h.cell(row=r,column=2,value=g(cnt))
        h.cell(row=r,column=3,value=g(f'SUMIFS({JX},{JB},$A{r})')).number_format="$#,##0.00"
        h.cell(row=r,column=4,value=g(f'SUMIFS({JY},{JB},$A{r})')).number_format="0.00"
        h.cell(row=r,column=5,value=g(f'IFERROR(COUNTIFS({JB},$A{r},{JZ},"Win")/{cnt},"")')).number_format="0%"
        h.cell(row=r,column=6,value=g(f'IF($B{r}=0,"—",IF(OR($C{r}<=-{qS}!$B$5,$B{r}>{qS}!$B$6,'
                                      f'COUNTIFS({JB},$A{r},{JAL},"⚠️ Revenge")>0),"🔴 LANGGAR","✅ Aman"))'))
        h.cell(row=r,column=7,value=g(f'SUM($D${DFIRST}:$D{r})')).number_format="0.00"
        h.cell(row=r,column=8,value=g(f'MAX($G${DFIRST}:$G{r})')).number_format="0.00"
        h.cell(row=r,column=9,value=g(f'$H{r}-$G{r}')).number_format="0.00"
        for cc in range(2,10):
            c=h.cell(row=r,column=cc); c.border=BOX; c.font=Font(size=9)
            c.alignment=Alignment(horizontal="center")
            if cc>=7: c.fill=fill(GREY)
    h.freeze_panes="A3"
    for f_,bg,fg in [('$F3="🔴 LANGGAR"',LOSS,"991B1B"),('$F3="✅ Aman"',WIN,"065F46")]:
        h.conditional_formatting.add(f"F{DFIRST}:F{DLAST}",FormulaRule(formula=[f_],fill=fill(bg),font=Font(bold=True,color=fg,size=9)))
    for cl in ("C","D"):
        for op,fg in ((">",""),("<","")):
            h.conditional_formatting.add(f"{cl}{DFIRST}:{cl}{DLAST}",
                FormulaRule(formula=[f'AND($B3>0,${cl}3{op}0)'],
                            font=Font(bold=True,color="065F46" if op==">" else "991B1B",size=9)))

def bikin_datachart(wb):
    dc=wb.create_sheet(C); dc.sheet_view.showGridLines=False
    title(dc,"A1","📈 DATA CHART — bahan mentah grafik",13)
    dc["A2"]="Diisi rumus otomatis, dipakai grafik di Dashboard. Boleh disembunyikan, jangan dihapus."
    dc["A2"].font=Font(italic=True,size=9,color="6B7280")
    def tbl(c0,nama,headers,rows_data,widths):
        dc.cell(row=3,column=c0,value=nama).font=Font(bold=True,size=10,color="FFFFFF")
        dc.cell(row=3,column=c0).fill=fill(INK2)
        for i,ht in enumerate(headers): hdr(dc,f"{get_column_letter(c0+i)}4",ht,bg="4B5563",size=9)
        for i,w in enumerate(widths): dc.column_dimensions[get_column_letter(c0+i)].width=w
        for k,vals in enumerate(rows_data):
            for i,(v,fmt) in enumerate(vals):
                cc=dc.cell(row=5+k,column=c0+i,value=v)
                if fmt: cc.number_format=fmt
                cc.font=Font(size=9); cc.border=BOX
    def cat(col_letter,values,pakai_win=False):
        JC=f"{qJ}!${col_letter}${FIRST}:${col_letter}${LAST}"
        out=[]
        for v in values:
            cnt=(f'(COUNTIFS({JC},"{v}",{JZ},"Win",{JAQ},1)+COUNTIFS({JC},"{v}",{JZ},"Loss",{JAQ},1)'
                 f'+COUNTIFS({JC},"{v}",{JZ},"BE",{JAQ},1))')
            row=[(v,None),(f'={cnt}',"0")]
            if pakai_win: row.append((f'=IFERROR(COUNTIFS({JC},"{v}",{JZ},"Win",{JAQ},1)/{cnt},0)',"0%"))
            row.append((f'=IFERROR(AVERAGEIFS({JY},{JC},"{v}",{JAQ},1),0)',"0.00"))
            out.append(row)
        return out
    tbl(1,"T1 · Ekuitas Harian",["Tanggal","Kumulatif R"],
        [[(f'=IF({qH}!$A{DFIRST+i}="","",{qH}!$A{DFIRST+i})',"dd/mm"),
          (f'=IF({qH}!$A{DFIRST+i}="","",{qH}!$G{DFIRST+i})',"0.00")] for i in range(DCROWS)],(11,12))
    tbl(4,"T2 · PnL Harian",["Tanggal","PnL $"],
        [[(f'=IF({qH}!$A{DFIRST+i}="","",{qH}!$A{DFIRST+i})',"dd/mm"),
          (f'=IF({qH}!$A{DFIRST+i}="","",{qH}!$C{DFIRST+i})',"0.00")] for i in range(DCROWS)],(11,12))
    tbl(7,"T3 · Per Setup",["Setup","N","Win %","Exp R"],
        cat("H",["First Touch","RBS Retest","SBR Retest","Lainnya"],True),(14,7,8,8))
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
        cat("AF",["Tenang","FOMO","Balas dendam","Ragu","Overconfident","Bosan"]),(15,7,8))
    tbl(19,"T6 · Per Sesi",["Sesi","N","Exp R"],
        cat("E",["London","Overlap LDN+NY","New York","Asia"]),(16,7,8))
    tbl(23,"T7 · Hasil",["Hasil","Jumlah"],
        [[(v,None),(f'=COUNTIFS({JZ},"{v}",{JAQ},1)',"0")] for v in ("Win","Loss","BE")],(9,9))
    tbl(26,"T8 · Kondisi Fisik",["Fisik","N","Exp R"],
        cat("AG",["Segar","Biasa","Capek","Ngantuk"]),(11,7,8))

def bikin_dashboard(wb):
    d=wb.create_sheet(D); d.sheet_view.showGridLines=False
    for col,w in zip("ABCDEF",(26,16,13,13,13,20)): d.column_dimensions[col].width=w
    title(d,"A1","📊 DASHBOARD",16)
    d["A2"]="Ubah dropdown filter → semua metrik, tabel, dan grafik ikut menyesuaikan."
    d["A2"].font=Font(italic=True,size=9,color="6B7280")
    band(d,3,"🎛️  FILTER INTERAKTIF")
    for i,(label,opts) in enumerate([("Instrumen","(Semua),XAUUSD,BTCUSD,EURUSD,GBPUSD,USDJPY"),
      ("Tipe Setup","(Semua),First Touch,RBS Retest,SBR Retest,Lainnya"),
      ("Sesi","(Semua),London,Overlap LDN+NY,New York,Asia"),
      ("Emosi","(Semua),Tenang,FOMO,Balas dendam,Ragu,Overconfident,Bosan"),
      ("Kondisi Fisik","(Semua),Segar,Biasa,Capek,Ngantuk"),
      ("Bias EMA200 Searah","(Semua),Ya,Tidak")]):
        r=4+i
        c=d.cell(row=r,column=1,value=label); c.font=Font(bold=True,size=10); c.fill=fill(GREY); c.border=BOX
        v=d.cell(row=r,column=2,value="(Semua)"); v.font=Font(bold=True,size=10,color="1E3A8A")
        v.fill=fill("EFF6FF"); v.border=BOX; v.alignment=Alignment(horizontal="center")
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
     ("D15","Max Drawdown R (semua)",f'=IFERROR(MAX({qH}!$I${DFIRST}:$I${DLAST}),"")',"0.00"),
     ("D16","Rata-rata Durasi (mnt)",f'=IFERROR(AVERAGEIFS({JAA},{JAQ},1),"")',"0")]:
        col=cell[0]; row=int(cell[1:]); vcol=get_column_letter(ord(col)-64+1)
        c=d[f"{col}{row}"]; c.value=label; c.font=Font(bold=True,size=10); c.fill=fill(GREY); c.border=BOX
        v=d[f"{vcol}{row}"]; v.value=formula; v.number_format=fmt; v.border=BOX
        v.font=Font(bold=True,size=11,color=INK); v.alignment=Alignment(horizontal="center")
    PCT=f'SUM({JX})/{qS}!$B$7'; BARN=f'MAX(0,MIN(20,ROUND({PCT}*20,0)))'
    band(d,18,"🎯  PROGRESS TARGET (total semua trade, tidak ikut filter)")
    d["A19"]="Tercapai"; d["A19"].font=Font(bold=True,size=10)
    d["B19"]=f'=IFERROR({PCT},"")'; d["B19"].number_format="0.0%"; d["B19"].font=Font(bold=True,size=12)
    d["C19"]=f'=IFERROR(REPT("█",{BARN})&REPT("░",20-{BARN}),"")'; d["C19"].font=Font(size=11,color="065F46")
    d["A20"]="Setara Rupiah"; d["A20"].font=Font(bold=True,size=10)
    d["B20"]=f'=SUM({JX})*{qS}!$B$8'; d["B20"].number_format='"Rp"#,##0'
    d["B20"].font=Font(bold=True,size=11,color="065F46")
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
            for op,bg,fg in ((">",WIN,"065F46"),("<",LOSS,"991B1B")):
                d.conditional_formatting.add(f"D{r}:D{r}",FormulaRule(
                    formula=[f'AND($B{r}>0,$D{r}{op}0)'],fill=fill(bg),font=Font(bold=True,color=fg,size=9)))
        return hrow+1+len(values)+1
    r=22
    r=block(r,"①  PER TIPE SETUP","H",["First Touch","RBS Retest","SBR Retest","Lainnya"],
            "Menjawab pertanyaan yang backtest Juli gantung: retest beneran lebih bagus dari first touch?")
    r=block(r,"②  PER SESI","E",["London","Overlap LDN+NY","New York","Asia"],
            "Sesi mana yang beneran bayar?")
    r=block(r,"③  PER EMOSI SEBELUM ENTRY","AF",["Tenang","FOMO","Balas dendam","Ragu","Overconfident","Bosan"],
            "Ini yang paling sering mengubah hasil orang. Lihat selisih Tenang vs FOMO.")
    r=block(r,"④  PER KONDISI FISIK","AG",["Segar","Biasa","Capek","Ngantuk"],
            "Cek apakah 'Capek' punya harga.")
    r=block(r,"⑤  BIAS EMA200 SEARAH?","K",["Ya","Tidak"],
            "Backtest 31 Agu tidak bisa memutuskan ini (CI lewat nol). Data live kamu yang menjawab.")
    r=block(r,"⑥  SESUAI CHECKLIST?","AI",["Ya","Tidak"],
            "Kalau 'Tidak' ternyata lebih untung, checklist-nya yang salah — bukan kamu.")
    r=block(r,"⑦  PER INSTRUMEN","F",["XAUUSD","BTCUSD","EURUSD","GBPUSD","USDJPY"])
    band(d,r,"⑧  ANALISA MAE / MFE — SL kesempitan atau TP kecepetan?"); r+=1
    for lbl,fm,note in [
      ("Rata-rata MAE trade WIN",f'=IFERROR(AVERAGEIFS({JAD},{JZ},"Win",{JAQ},1),"")',"Kalau > 0.7R: SL kamu nyaris kena terus. Pertimbangkan SL sedikit lebih lebar."),
      ("Rata-rata MAE trade LOSS",f'=IFERROR(AVERAGEIFS({JAD},{JZ},"Loss",{JAQ},1),"")',"Pembanding."),
      ("Rata-rata MFE trade WIN",f'=IFERROR(AVERAGEIFS({JAE},{JZ},"Win",{JAQ},1),"")',"Kalau jauh di atas R hasilmu: keluar kecepetan."),
      ("Rata-rata MFE trade LOSS",f'=IFERROR(AVERAGEIFS({JAE},{JZ},"Loss",{JAQ},1),"")',"Kalau > 1.0R: sering sudah untung 1R lalu balik rugi.")]:
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
    for k,e in enumerate(["Geser SL","Entry tanpa plan","Lot kegedean","Revenge trade","Exit kecepetan","Entry telat","Lawan bias","Lainnya"]):
        rr=r+1+k
        d.cell(row=rr,column=1,value=e).font=Font(size=9,bold=True)
        d.cell(row=rr,column=2,value=f'=COUNTIFS({JAJ},$A{rr},{JAQ},1)').number_format="0"
        d.cell(row=rr,column=4,value=f'=IFERROR(SUMIFS({JY},{JAJ},$A{rr},{JAQ},1),"")').number_format="0.00"
        d.cell(row=rr,column=5,value=f'=IFERROR(SUMIFS({JX},{JAJ},$A{rr},{JAQ},1),"")').number_format="$#,##0.00"
        for cc in (1,2,4,5):
            cx=d.cell(row=rr,column=cc); cx.border=BOX; cx.font=Font(size=9)
            if cc>1: cx.alignment=Alignment(horizontal="center")
        d.conditional_formatting.add(f"E{rr}:E{rr}",FormulaRule(formula=[f'AND($B{rr}>0,$E{rr}<0)'],
            fill=fill(LOSS),font=Font(bold=True,color="991B1B",size=9)))
    r=r+10
    d.merge_cells(f"A{r}:F{r+2}")
    w=d[f"A{r}"]
    w.value=("⚠️ INGAT: di bawah ~100 trade, angka di atas adalah PETUNJUK ARAH, bukan vonis.\n"
             "Beda win rate 10% pada 40 trade masih sangat mungkin kebetulan.\n"
             "Kumpulkan 3–6 bulan sebelum membuang satu jenis setup.")
    w.font=Font(bold=True,size=9,color="7C2D12"); w.fill=fill(WARN)
    w.alignment=Alignment(wrap_text=True,vertical="center"); w.border=BOX

def bikin_review(wb):
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
    for wk in range(1,13):
        v.merge_cells(f"A{row}:B{row}")
        c=v[f"A{row}"]; c.value=f"MINGGU {wk}"; c.font=Font(bold=True,size=12,color="FFFFFF")
        c.fill=fill(INK); c.alignment=Alignment(horizontal="center"); row+=1
        for p in prompts:
            q=v.cell(row=row,column=1,value=p); q.font=Font(size=9,bold=True); q.fill=fill(GREY)
            q.alignment=Alignment(wrap_text=True,vertical="center"); q.border=BOX
            a=v.cell(row=row,column=2); a.border=BOX; a.alignment=Alignment(wrap_text=True,vertical="top")
            v.row_dimensions[row].height=34; row+=1
        row+=1

def tulis_gs():
    E=4+DCROWS
    open(GS,"w",encoding="utf-8").write(f'''/**
 * Pasang grafik native di tab Dashboard.
 * Extensions > Apps Script > paste semua ini > Save > pilih buatGrafik > Run.
 * Aman dijalankan berkali-kali — grafik lama dihapus dulu.
 */
function buatGrafik() {{
  const ss   = SpreadsheetApp.getActiveSpreadsheet();
  const dash = ss.getSheetByName('{D}');
  const src  = ss.getSheetByName('{C}');
  if (!dash || !src) {{
    SpreadsheetApp.getUi().alert('Tab Dashboard atau Data Chart tidak ketemu.');
    return;
  }}
  dash.getCharts().forEach(c => dash.removeChart(c));
  const buat = (type, ranges, row, col, judul, opts) => {{
    let b = dash.newChart().setChartType(type);
    ranges.forEach(r => b = b.addRange(src.getRange(r)));
    b = b.setPosition(row, col, 0, 0)
         .setOption('title', judul).setOption('width', 460).setOption('height', 260)
         .setOption('titleTextStyle', {{fontSize: 12, bold: true}})
         .setOption('legend', {{position: 'none'}});
    for (const k in (opts || {{}})) b = b.setOption(k, opts[k]);
    dash.insertChart(b.build());
  }};
  const CH = Charts.ChartType;
  buat(CH.LINE,   ['A4:B{E}'], 3,  8, 'Kurva Ekuitas — R kumulatif harian',
       {{colors: ['#00bcd4'], pointSize: 3}});
  buat(CH.COLUMN, ['D4:E{E}'], 17, 8, 'PnL Harian ($)', {{colors: ['#1E3A8A']}});
  buat(CH.BAR,    ['G4:G8', 'J4:J8'], 31, 8, 'Expectancy R per Tipe Setup', {{colors: ['#065F46']}});
  buat(CH.COLUMN, ['L4:M12'], 3,  16, 'Sebaran Hasil (R)', {{colors: ['#7C2D12']}});
  buat(CH.BAR,    ['O4:O10', 'Q4:Q10'], 17, 16, 'Expectancy R per Emosi', {{colors: ['#831843']}});
  buat(CH.PIE,    ['W4:X7'], 31, 16, 'Win / Loss / BE',
       {{colors: ['#10B981', '#EF4444', '#9CA3AF'], legend: {{position: 'right'}}}});
  ss.toast('6 grafik terpasang di Dashboard.', 'Selesai', 5);
}}
''')

def build():
    if os.path.exists(OUT):
        sys.exit(f"❌ {OUT} sudah ada. File master tidak boleh ditimpa.\n"
                 f"   Pakai:  python journal.py add <file.csv>")
    wb=Workbook()
    bikin_panduan(wb); bikin_setelan(wb); bikin_jurnal(wb)
    bikin_harian(wb); bikin_datachart(wb); bikin_dashboard(wb); bikin_review(wb)
    wb.save(OUT); tulis_gs()
    print(f"✓ master dibuat: {OUT}")
    print(f"✓ skrip grafik : {GS}")

def add(csv_path, tz=7):
    if not os.path.exists(OUT): sys.exit("❌ master belum ada. Jalankan: python journal.py build")
    if not os.path.exists(csv_path): sys.exit(f"❌ CSV tidak ketemu: {csv_path}")
    wb=load_workbook(OUT); j=wb[J]
    ada={str(j[f"{TIKET_COL}{n}"].value).strip() for n in range(FIRST,LAST+1)
         if j[f"{TIKET_COL}{n}"].value not in (None,"")}
    baris=FIRST
    while baris<=LAST and j[f"B{baris}"].value not in (None,""): baris+=1
    tr=[r for r in csv.DictReader(open(csv_path,encoding="utf-8-sig")) if r.get("ticket")]
    tr.sort(key=lambda r: r["opening_time_utc"])
    num=lambda v: float(v) if v not in (None,"") else None
    masuk=[]; lewat=0
    for t in tr:
        tk=str(t["ticket"]).strip()
        if tk in ada: lewat+=1; continue
        if baris>LAST: print(f"⚠️ kapasitas {LAST-FIRST+1} baris penuh. Sisa trade tidak dimasukkan."); break
        o=dt.datetime.fromisoformat(t["opening_time_utc"])+dt.timedelta(hours=tz)
        c=dt.datetime.fromisoformat(t["closing_time_utc"])+dt.timedelta(hours=tz)
        j[f"B{baris}"]=o.date(); j[f"C{baris}"]=o.time(); j[f"D{baris}"]=c.time()
        j[f"F{baris}"]=t["symbol"]; j[f"G{baris}"]="Buy" if t["type"].lower()=="buy" else "Sell"
        j[f"N{baris}"]=num(t["opening_price"]); j[f"Q{baris}"]=num(t["closing_price"])
        if num(t.get("stop_loss")):   j[f"O{baris}"]=num(t["stop_loss"])
        if num(t.get("take_profit")): j[f"P{baris}"]=num(t["take_profit"])
        j[f"S{baris}"]=num(t["lots"])
        j[f"{TIKET_COL}{baris}"]=tk
        j[f"AK{baris}"]=("" if num(t.get("stop_loss")) else
                         "⚠️ TANPA SL di broker — isi SL yang kamu niatkan biar Risiko $ & R Hasil terhitung")
        ada.add(tk); masuk.append((baris,tk,t["symbol"])); baris+=1
    wb.save(OUT)
    print(f"✓ {len(masuk)} trade baru ditambahkan" + (f", {lewat} dilewati (tiket sudah ada)" if lewat else ""))
    if masuk: print(f"✓ baris {masuk[0][0]}–{masuk[-1][0]} di tab '{J}'")

if __name__=="__main__":
    a=sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0]=="build": build()
    elif a[0]=="add":
        tz=7
        if "--tz" in a: tz=float(a[a.index("--tz")+1])
        add(a[1], tz)
    else: sys.exit(__doc__)
