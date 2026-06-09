# 📊 Support & Resistance Indicator - Panduan Lengkap

## 🎯 Untuk Scalping XAU & Forex (M1/M5/M15)

---

## 📖 Daftar Isi
1. [Penjelasan Indikator](#penjelasan-indikator)
2. [Setting Optimal](#setting-optimal)
3. [Kapan Entry](#kapan-entry)
4. [Kapan Exit](#kapan-exit)
5. [Risk Management](#risk-management)
6. [Tips Penting](#tips-penting)

---

## 🔍 Penjelasan Indikator

### Apa yang Ditampilkan?

**1. BOX HIJAU (Support)**
- Zona dimana harga cenderung **naik/rebound**
- Muncul di area **pivot low** dengan **volume tinggi**
- Entry: **BUY** ketika harga reject dari zona ini

**2. BOX MERAH (Resistance)**
- Zona dimana harga cenderung **turun/reject**
- Muncul di area **pivot high** dengan **volume tinggi**
- Entry: **SELL** ketika harga reject dari zona ini

**3. DIAMOND (◆) - SINYAL ENTRY**
- 🟢 **Diamond HIJAU di bawah candle** = Sinyal **BUY**
  - Support bertahan / Resistance yang sudah break jadi support
- 🔴 **Diamond MERAH di atas candle** = Sinyal **SELL**
  - Resistance bertahan / Support yang sudah break jadi resistance

**4. LABEL "Break Res" / "Break Sup"**
- Muncul ketika harga **break through** zona
- Tunggu **pullback** (retest) untuk entry
- Entry saat diamond muncul setelah retest

**5. PERUBAHAN WARNA BOX**
- **Box jadi DASHED (putus-putus)** = Zone sudah di-break
- **Box hijau jadi merah** = Support broken, sekarang jadi resistance
- **Box merah jadi hijau** = Resistance broken, sekarang jadi support

---

## ⚙️ Setting Optimal

### File: `supportandresistance.pine`

**Setting Baru (Optimized untuk Scalping):**

```
Lookback Period: 10
- Lebih kecil = zona muncul lebih cepat
- Untuk M5 scalping: gunakan 8-10
- Untuk swing trading: gunakan 15-20

Delta Volume Filter Length: 2
- Lebih kecil = lebih banyak zona
- Untuk scalping: gunakan 2
- Untuk filter ketat: gunakan 4-5

Adjust Box Width: 1.0
- Standar: 1.0
- Untuk XAU (volatile): 1.2-1.5
- Untuk Forex (stable): 0.8-1.0
```

### Multi-Timeframe Setup (RECOMMENDED)

**Chart 1: M15 (Untuk Cari Zona)**
```
Indicator: S&R dengan setting lookback=20, vol=4
Fungsi: Cari zona besar/major levels
Cek: Setiap 30-60 menit
```

**Chart 2: M5 (Untuk Eksekusi)**
```
Indicator: S&R Fast dengan setting lookback=10, vol=2
Fungsi: Confirm zona M15 + cari setup
Cek: Setiap 10-15 menit
```

**Chart 3: M1 (Untuk Timing)**
```
Indicator: S&R Fast (same settings)
Fungsi: Entry presisi, lihat rejection detail
Cek: Hanya saat setup muncul di M5
```

---

## 🎯 Kapan Entry

### Strategi 1: FIRST TOUCH (Sentuhan Pertama)

**Untuk zona FRESH yang belum pernah disentuh**

#### Entry BUY (di Support):
```
1. ✅ Harga turun mendekati box HIJAU
2. ✅ Harga masuk DALAM box
3. ✅ Muncul candle rejection (wick panjang ke bawah / pin bar)
4. ✅ Candle CLOSE di ATAS box
5. 🚀 ENTRY: BUY saat candle close
6. 🛑 Stop Loss: Di bawah box (bawah zone + 5-10 pips buffer)
7. 🎯 Target: Resistance berikutnya ATAU 1:2 RR
```

#### Entry SELL (di Resistance):
```
1. ✅ Harga naik mendekati box MERAH
2. ✅ Harga masuk DALAM box
3. ✅ Muncul candle rejection (wick panjang ke atas / shooting star)
4. ✅ Candle CLOSE di BAWAH box
5. 🚀 ENTRY: SELL saat candle close
6. 🛑 Stop Loss: Di atas box (atas zone + 5-10 pips buffer)
7. 🎯 Target: Support berikutnya ATAU 1:2 RR
```

**Contoh Visual - SELL di Resistance:**
```
💰 Target: 2,625 (next support)
        ↑
        |
   2,635 |
        |     ╔══════════════╗
        | ────║   ◆ SELL    ║──── 🚀 ENTRY (candle close di bawah box)
   2,630 |     ║      ↓      ║
        | ────╠──────────────╣──── ⬆ Box MERAH (Resistance)
        |     ║   |  ↑  |    ║
        |     ║   | ███ |    ║──── ⚡ Rejection wick (shooting star)
   2,625 |     ║   |     |   ║
        | ────╚══════════════╝──── ⬇ Box bawah
        |
        |  🛑 Stop Loss: 2,631 (di atas box + 10 pips buffer)
   2,620 |
```

**Contoh Visual - BUY di Support:**
```
   2,640 |  🛑 Stop Loss: 2,618 (di bawah box - 10 pips buffer)
        |
        | ────╔══════════════╗──── ⬆ Box atas
   2,635 |     ║   |     |   ║
        |     ║   | ███ |    ║──── ⚡ Rejection wick (pin bar)
        |     ║   |  ↓  |    ║
   2,630 |     ╠──────────────╣──── ⬇ Box HIJAU (Support)
        | ────║   ◆ BUY     ║──── 🚀 ENTRY (candle close di atas box)
        |     ║      ↑      ║
   2,625 |     ╚══════════════╝
        |
        |
   2,620 |
        ↓
💰 Target: 2,635 (next resistance)
```

---

### Strategi 2: BREAK & RETEST ⭐ (PALING AKURAT)

**Untuk zona yang sudah di-break, tunggu retest**

#### Break RESISTANCE (Jadi Support Baru):
```
1. ✅ Muncul label "Break Res"
2. ✅ Box merah berubah jadi HIJAU + DASHED
3. ✅ Tunggu harga PULLBACK ke box
4. ✅ Diamond HIJAU (◆) muncul di BAWAH candle
5. 🚀 ENTRY: BUY saat diamond muncul
6. 🛑 Stop Loss: Di bawah box
7. 🎯 Target: Resistance berikutnya / 1:2 RR
```

#### Break SUPPORT (Jadi Resistance Baru):
```
1. ✅ Muncul label "Break Sup"
2. ✅ Box hijau berubah jadi MERAH + DASHED
3. ✅ Tunggu harga PULLBACK ke box
4. ✅ Diamond MERAH (◆) muncul di ATAS candle
5. 🚀 ENTRY: SELL saat diamond muncul
6. 🛑 Stop Loss: Di atas box
7. 🎯 Target: Support berikutnya / 1:2 RR
```

**Contoh Visual - Break Resistance (Jadi Support):**
```
FASE 1: BREAKOUT          FASE 2: RETEST           FASE 3: ENTRY
   ↑                          ↑                         ↑
   |                          |                         |
   |    "Break Res"           |    Pullback             |    ◆ BUY!
   |    ⬆⬆⬆                   |      ↓↓↓                |    🚀
   | ═══════════════       ═══════════════         ═══════════════
   | ║ RESISTANCE  ║       ║ RESISTANCE  ║         ║ NEW SUPPORT ║
   | ║   (MERAH)   ║  -->  ║  BROKEN ❌  ║   -->   ║   (HIJAU)   ║
   | ║             ║       ║             ║         ║      ◆      ║
   | ═══════════════       ═══════════════         ═══════════════
   |                          |     ⬆                   |
   |                          |   RETEST                | 🛑 SL di bawah

   Harga break UP           Harga kembali            Diamond hijau
   Box jadi DASHED          test bekas resistance    muncul = ENTRY!
```

**Contoh Visual - Break Support (Jadi Resistance):**
```
FASE 1: BREAKDOWN         FASE 2: RETEST           FASE 3: ENTRY
   |                          |                         |
   | ═══════════════       ═══════════════         ═══════════════
   | ║   SUPPORT   ║       ║   SUPPORT   ║         ║NEW RESISTANCE║
   | ║   (HIJAU)   ║  -->  ║  BROKEN ❌  ║   -->   ║   (MERAH)    ║
   | ║             ║       ║             ║         ║      ◆       ║
   | ═══════════════       ═══════════════         ═══════════════
   |    ⬇⬇⬇                   |     ⬆                   | 🛑 SL di atas
   |                          |   RETEST                |
   |   "Break Sup"            |      ↑↑↑                |    🚀
   ↓                          ↓   Pullback             ↓  ◆ SELL!

   Harga break DOWN         Harga kembali            Diamond merah
   Box jadi DASHED          test bekas support       muncul = ENTRY!
```

**Kenapa Strategi Ini Paling Bagus?**
- ✅ Konfirmasi sudah ada (price action proven)
- ✅ Role reversal = psychological level kuat
- ✅ Diamond = entry trigger yang jelas
- ✅ Stop loss jelas (pakai box edge)
- ✅ Win rate tinggi (60-70%)

---

### Strategi 3: CONFLUENCE (Kombinasi Sinyal)

**Jangan entry kalau cuma 1 sinyal! Tunggu minimal 3 konfirmasi:**

```
CHECKLIST ENTRY (minimal 3 harus centang):
☐ Diamond (◆) muncul
☐ Candlestick pattern (pin bar, engulfing, doji)
☐ Volume tinggi (lihat angka di box)
☐ M15 zone alignment (zona M15 dan M5 overlap)
☐ RSI oversold (<30) untuk BUY / overbought (>70) untuk SELL
☐ Trend alignment (entry searah trend HTF)

Kalau dapat 3+ ✅ = ENTRY
Kalau cuma 1-2 = SKIP atau wait
```

**Contoh Entry dengan Confluence:**
```
1. Harga touch support box HIJAU ← ✅
2. Diamond hijau muncul ← ✅
3. Bullish engulfing candle ← ✅
4. Volume box = 1250 (tinggi) ← ✅
5. M15 juga ada support zone di area sama ← ✅

= 5 konfirmasi! STRONG BUY!
```

---

### Strategi 4: MULTI-TOUCH (Sentuhan Berulang)

**Zona yang sudah disentuh beberapa kali:**

```
⚠️ PERHATIAN:
- Touch 1x = Zona kuat, HIGH probability
- Touch 2x = Zona masih OK, MEDIUM probability
- Touch 3x = Zona mulai lemah, LOW probability
- Touch 4x+ = JANGAN ENTRY, siap-siap breakout!

RULE:
❌ Jangan ambil sentuhan ke-4 atau lebih
✅ Malah siapkan untuk entry BREAKOUT (strategi 2)
```

---

## 🚪 Kapan Exit

### Exit Strategy 1: TARGET ZONE (Recommended)

```
Target: Zone S&R berikutnya

Contoh:
- Entry BUY di support 2,620
- Target: Resistance berikutnya di 2,635
- Jarak: 15 pips
- Exit: Saat harga TOUCH resistance box
```

### Exit Strategy 2: RISK:REWARD Ratio

```
Minimum: 1:2 RR

Contoh:
- Entry: 2,620
- Stop Loss: 2,615 (5 pips)
- Take Profit: 2,630 (10 pips)
- RR = 1:2 ✅

RULES:
- Jangan ambil trade kalau RR < 1:1.5
- Ideal RR untuk scalping: 1:2 atau 1:3
- Kalau bisa dapat 1:5, lebih bagus!
```

### Exit Strategy 3: TRAILING STOP

```
Untuk trade yang profit:
1. Move stop loss to breakeven (entry price) saat profit = 1:1
2. Trail stop setiap 5-10 pips profit
3. Biar profit jalan, stop loss ikut naik/turun
```

### Exit Strategy 4: REVERSE SIGNAL

```
Kalau lagi BUY:
- Muncul diamond MERAH di resistance = EXIT
- Jangan tunggu stop loss kena

Kalau lagi SELL:
- Muncul diamond HIJAU di support = EXIT
- Protect profit, jangan serakah
```

### Exit Strategy 5: TIME-BASED (Scalping)

```
Kalau trade di M5:
- Maksimal hold: 1-2 jam
- Kalau belum profit dalam 1 jam = review
- Kalau sideways 30 menit = exit breakeven

Kalau trade di M1:
- Maksimal hold: 15-30 menit
- Quick in, quick out
- Jangan hold overnight!
```

---

## 💰 Risk Management

### 1. Position Sizing

```
GOLDEN RULE: Risk maksimal 1-2% per trade

Contoh dengan account $1,000:
- Risk 1% = $10 per trade
- Stop loss 10 pips
- XAU: 1 pip = $1 (untuk 0.01 lot)
- Max loss = $10
- Position size: 0.01 lot ✅

Contoh dengan account $10,000:
- Risk 2% = $200 per trade
- Stop loss 15 pips
- XAU: 1 pip = $10 (untuk 0.1 lot)
- Max loss = $150
- Position size: 0.10 lot ✅
```

### 2. Stop Loss Rules

```
WAJIB:
✅ Stop loss SELALU beyond box edge
✅ Tambah buffer 5-10 pips (untuk spread/wick)
✅ JANGAN pernah move SL closer (biar trade breathe)
✅ Move SL to breakeven setelah profit 1:1

JANGAN:
❌ Trade tanpa stop loss
❌ Stop loss terlalu ketat (<5 pips untuk XAU)
❌ Move stop loss lebih dekat saat panik
```

### 3. Take Profit Rules

```
✅ Set TP di zone berikutnya
✅ Atau gunakan RR 1:2 minimum
✅ Partial TP: Close 50% di 1:1, biarkan 50% jalan
✅ Trail stop untuk maximize profit

❌ Jangan close profit terlalu cepat (less than 1:1)
❌ Jangan serakah (target unrealistic)
```

### 4. Trading Sessions (XAU)

```
✅ BEST SESSIONS (High Liquidity):
- London Open: 3:00 - 12:00 PM EST
- New York Open: 8:00 AM - 5:00 PM EST
- Overlap London-NY: 8:00 AM - 12:00 PM EST (TERBAIK!)

⚠️ AVOID:
- Asian Session: 7:00 PM - 4:00 AM EST (choppy, whipsaw)
- Major news events: NFP, FOMC, CPI
- Low volume hours: Lunch time, late night
```

### 5. Daily Limits

```
✅ Max trades per day: 3-5 trades
✅ Max loss per day: 3% of account (STOP trading kalau tembus!)
✅ Max win per day: Bebas, tapi review kenapa menang
✅ Max consecutive losses: 3 losses berturut = STOP, review strategy

BURNOUT PREVENTION:
- Trade 2-4 jam per hari
- Jangan stare at chart non-stop
- Break setiap 1 jam
```

---

## 💡 Tips Penting

### ✅ DO (Lakukan):

1. **Tunggu Diamond Muncul**
   - Diamond = trigger entry yang jelas
   - Jangan entry sebelum diamond muncul

2. **Cek Volume di Box**
   - Angka "Vol: XXX" di box
   - Makin tinggi volume = makin kuat zone
   - Trade high-volume zones first

3. **Multi-Timeframe Confirmation**
   - Cek M15 dulu (cari zona besar)
   - Eksekusi di M5 (timing)
   - Fine-tune di M1 (presisi)

4. **Trade Searah Trend HTF**
   - Kalau M15 uptrend, ambil BUY signals di M5
   - Kalau M15 downtrend, ambil SELL signals di M5
   - Jangan melawan trend besar

5. **Paper Trade Dulu**
   - Test strategi 1-2 minggu di demo
   - Catat: win rate, RR, best strategy
   - Baru real trading setelah konsisten profit

6. **Journal Semua Trade**
   - Screenshot entry
   - Alasan entry (strategy mana yang dipakai)
   - Result (win/loss, RR achieved)
   - Lesson learned

### ❌ DON'T (Jangan Lakukan):

1. **Jangan Entry Sebelum Touch Box**
   - Entry di "no man's land" = low probability
   - Tunggu harga MASUK zona dulu

2. **Jangan Trade Sentuhan 4+**
   - Zone sudah weak
   - Siap-siap breakout malah

3. **Jangan Trade Saat News Besar**
   - NFP (1st Friday monthly)
   - FOMC meetings
   - CPI/Inflation data
   - Close semua trade 30 menit sebelum news

4. **Jangan Revenge Trading**
   - Loss 1-2x berturut = stop dulu
   - Review kenapa loss
   - Clear head, baru trade lagi

5. **Jangan Overtrade**
   - Quality > Quantity
   - 1-2 setup bagus lebih baik dari 10 setup asal
   - Kalau tidak ada setup, jangan paksa

6. **Jangan Move SL Closer**
   - Biarkan trade breathe
   - Kalau takut, berarti position size terlalu besar
   - Reduce lot size, jangan adjust SL

---

## 📊 Contoh Trade Setup

### Example 1: BUY - First Touch

```
TIMEFRAME: M5
PAIR: XAUUSD

SETUP:
1. Box hijau muncul di 2,620.00 - 2,619.20
2. Volume: 850 (tinggi)
3. Harga turun dari 2,635, approach box
4. Candle masuk box di 2,620.50
5. Bullish pin bar muncul (wick panjang ke bawah)
6. Candle close di 2,621.00 (di atas box)
7. Diamond hijau ◆ muncul di bawah

ENTRY:
- Type: BUY
- Price: 2,621.00
- Stop Loss: 2,618.50 (di bawah box -0.70 pip buffer)
- Take Profit: 2,626.00 (resistance berikutnya)
- Risk: 2.50 pips
- Reward: 5.00 pips
- RR: 1:2 ✅

RESULT:
- TP hit di 2,626.00
- Profit: 5 pips
- Status: WIN ✅
```

### Example 2: SELL - Break & Retest

```
TIMEFRAME: M5
PAIR: XAUUSD

SETUP:
1. Box merah resistance di 2,640.00 - 2,640.80
2. Harga break di atas dengan strong candle
3. Label "Break Res" muncul
4. Box berubah jadi HIJAU + DASHED (sekarang support)
5. Harga naik ke 2,645, lalu pullback
6. Harga kembali touch box di 2,640.50
7. Bearish engulfing muncul
8. Diamond merah ◆ muncul di ATAS candle
9. KONFIRMASI: Resistance broken gagal jadi support

ENTRY:
- Type: SELL
- Price: 2,640.00
- Stop Loss: 2,641.50 (di atas box + buffer)
- Take Profit: 2,635.00 (support berikutnya)
- Risk: 1.50 pips
- Reward: 5.00 pips
- RR: 1:3.33 ✅

RESULT:
- TP hit di 2,635.00
- Profit: 5 pips
- Status: WIN ✅
```

### Example 3: SKIP - Low Probability

```
TIMEFRAME: M5
PAIR: XAUUSD

SETUP:
1. Box hijau support di 2,625.00
2. Sudah touch 4 kali dalam 2 jam
3. Volume: 120 (rendah)
4. No diamond muncul
5. Hanya doji candle (indecisive)
6. M15 shows downtrend (berlawanan)

DECISION: SKIP ❌

ALASAN:
- Touch ke-4 (zona weak)
- Low volume
- No diamond (no trigger)
- Against HTF trend
- Only 1 konfirmasi, kurang dari 3

RESULT:
- Harga break support 10 menit kemudian
- SAVED from loss! ✅
```

---

## 🔄 Workflow Harian

### Morning Routine (Sebelum Trading)

```
1. ☕ Buka TradingView (M15 chart)
2. 📊 Mark major S&R zones di M15
3. 📅 Check economic calendar (ada news besar?)
4. 🎯 Identify bias (bullish/bearish hari ini)
5. ⏰ Set alerts di zona-zona penting
6. ✅ Ready to trade
```

### Trading Session

```
1. 🔔 Alert bunyi (harga near zone)
2. 👀 Switch ke M5, check setup
3. ✅ Checklist confluence (min 3 konfirmasi)
4. 💎 Tunggu diamond muncul
5. 🚀 Entry saat signal confirmed
6. 📝 Set SL & TP immediately
7. 📱 Monitor di M1 (optional)
8. 💰 Manage trade (breakeven, trail stop)
9. 🎯 Exit di target / reverse signal
10. 📊 Journal the trade
```

### Post-Trading Review

```
1. 📊 Review semua trades hari ini
2. ✅ Win rate: XX%
3. 💰 RR average: 1:XX
4. 🔍 Best strategy today: XXX
5. ❌ Mistakes: XXX
6. 📝 Lessons learned: XXX
7. 🎯 Plan besok: XXX
```

---

## 🎓 Next Level: RBS Integration (Coming Soon)

**Setelah master strategi di atas, kita akan tambahkan:**

- **RBR (Rally-Base-Rally)** pattern di support = Strong BUY
- **DBD (Drop-Base-Drop)** pattern di resistance = Strong SELL
- **DBR (Drop-Base-Rally)** pattern di support = Reversal BUY
- **RBD (Rally-Base-Drop)** pattern di resistance = Reversal SELL

**RBS akan muncul HANYA di zona S&R = ultra-high probability setups!**

---

## 📞 Support & Updates

**File Locations:**
- Support & Resistance: `/Users/wahyusetiawan/Documents/tradingview/snd/supportandresistance.pine`
- Supply & Demand: `/Users/wahyusetiawan/Documents/tradingview/snd/supplyanddemand.pine`

**Settings Reminder:**
```
SCALPING OPTIMIZED (Current):
- Lookback Period: 10
- Delta Volume Filter: 2
- Box Width: 1.0

STRONG ZONES (Alternative):
- Lookback Period: 20
- Delta Volume Filter: 4
- Box Width: 0.8
```

---

## 🚀 Good Luck & Trade Safe!

**Remember:**
- 💎 **Diamond = Entry Trigger**
- 📊 **Volume = Zone Strength**
- 🎯 **RR 1:2 Minimum**
- 🛑 **Risk 1-2% Max**
- 📝 **Journal Everything**

**Konsisten profit > quick profit!** 🔥

---

*Last Updated: 2026-06-09*
*Version: 1.0 - Scalping Optimized*