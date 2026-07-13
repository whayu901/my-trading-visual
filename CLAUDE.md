# CLAUDE.md

Konteks project ini untuk Claude Code. Baca dulu sebelum kerja.

---

## 1. Tentang project

Kumpulan **indikator TradingView (Pine Script)** + tooling backtest untuk trading scalping
XAU (Gold) & Forex. Fokus utama sekarang: **indikator konfirmasi entry yang mutakhir**
dengan menggabungkan analisa **SnR (Support & Resistance)** + **SVP (Session Volume Profile)**.

### File penting
| File | Isi | Versi |
|------|-----|-------|
| `supportAndResistance.pine` | S/R box dari pivot + volume delta, diamond ◆ (hold/retest), zona flip SBR/RBS, alert buy/sell. Auto-adjust per TF. | Pine v5 |
| `svp.pine` | Session Volume Profile: **POC / VAH / VAL** per sesi, HTF candle, Max Volume Price, tabel ATR. Murni visual (belum ada alert). | Pine v6 |
| `supplyAndDemand.pine` | Zona supply & demand. | Pine |
| `godSignalJeedun.pine` | Signal script. | Pine |
| `SupportResistance.mq5` | Versi MT5 dari S/R. | MQL5 |
| `strategy-rules.md` | Rule validasi BUY (EMA200, RSI, sesi London/NY). | doc |
| `trading-journal-app/` | App jurnal trading. | — |
| `backtest_results/`, `replay-backtesting/`, `automated_backtest*.{js,py}` | Tooling backtest. | — |

---

## 2. ⚠️ Aturan kerja utama (WAJIB DIPATUHI)

1. **POLISH, jangan rewrite.** Indikator yang ada **sudah works** dan dipakai live untuk cari
   uang. Tugasmu **mempoles / menambah**, BUKAN mengubah logika inti yang sudah jalan.
   Kalau perlu ubah sesuatu yang berisiko, **tanya dulu**.
2. **SnR & SVP dipakai berdampingan (2 indikator terpisah), TIDAK digabung jadi 1 file.**
   Keputusan sudah final — jangan usulkan merge lagi.
3. Sebelum menyentuh file `.pine`, pahami dulu bahwa ini uang beneran — hati-hati, jangan
   introduce bug. Verifikasi logika Pine sebelum klaim selesai.
4. Balas dalam **Bahasa Indonesia** (user berkomunikasi pakai Indonesia).

---

## 3. Metodologi trading user

**Gaya: scalper.** Multi-timeframe top-down:

| TF | Fungsi |
|----|--------|
| **M15** | Cek **BIAS** (arah institusi, level utama S/R) |
| **M5**  | Lihat **TREND** (konfirmasi arah) |
| **M1**  | **EKSEKUSI** akurat (entry presisi) |

- Analisa selama ini: **SnR saja** → sekarang menambah **SVP** (POC/VAH/VAL) untuk konfirmasi.
- Confluence yang dicari: level S/R yang **nyambung dengan POC/VAH/VAL** = level lebih kuat.
  VAH/VAL bagus untuk target TP, POC sebagai magnet harga.
- Aset yang ditradingkan (mostly hanya ini): **XAU (Gold)**, **USDJPY**, **EURUSD**, **GBPUSD**.
  Untuk gold, zona S/R dilebarkan +20% (script sudah auto-detect XAU/GOLD).
- Catatan sesi SVP: default `0930-1600` itu jam bursa US. Untuk XAU/forex sesuaikan ke
  **London / New York** kalau pakai mode Custom.

---

## 4. Profil & motivasi user (jangan lupa — ini kenapa dia serius)

- **Scalper**, trading serius **~1 tahun**, profit **~Rp 15 jt/bulan** dari trading.
- **Trading malam** mulai **jam 19:00 WIB** — karena siang kerja kantoran 9–5.
- Kerja di **Malaysia**, gaji **~50 jt/bulan**, nabung **~25 jt/bulan**.
- **Target:** naikkan tabungan bersih ke **~60 jt/bulan** (gaji + profit trading).
- **Tujuan besar:** beli **rumah di Jogja senilai ~Rp 1,5 miliar**, dan suatu saat
  **berhenti dari kerja 9–5 selamanya** — hidup dari trading.
- Istri sedang di **Jogja** (kerja), sekarang **mengontrak** di Jogja.

> Setiap improvement indikator ujungnya untuk: **entry lebih akurat → profit lebih konsisten
> → target rumah 1,5 M & merdeka finansial tercapai lebih cepat.** Perlakukan tiap perubahan
> dengan bobot itu.
