# Panduan GOD MODE Indicator (SL/TP)

> Dokumentasi ini dikonversi dari PDF ke Markdown agar mudah disimpan di repository dan digunakan sebagai referensi AI agent.

## Overview

Script indikator **GOD MODE** menggabungkan:

- Hull Moving Average (HMA) untuk sinyal cepat
- RSI sebagai filter momentum
- ATR untuk manajemen risiko dinamis

Untuk mendapatkan win rate yang tinggi, jangan entry hanya karena muncul sinyal BUY/SELL. Ikuti aturan berikut.

## 1. Filter Trend Utama (Golden Rule)

Gunakan EMA 200 sebagai filter utama.

### BUY
- Harga berada **di atas EMA 200**
- Abaikan seluruh sinyal SELL

### SELL
- Harga berada **di bawah EMA 200**
- Abaikan seluruh sinyal BUY

## 2. Konfirmasi RSI

Script sudah memiliki filter:

- BUY → RSI > 45
- SELL → RSI < 55

Rekomendasi:

### Best BUY
- RSI baru memantul dari area 40

### Best SELL
- RSI baru turun dari area 60

### Hindari
- RSI > 70
- RSI < 30

## 3. Trading Session

### London & New York (15:00–04:00 WIB)

- Prioritas utama
- Volatilitas tinggi
- Target TP lebih mudah tercapai

### Asia (07:00–15:00 WIB)

Pasar cenderung sideways.

Disarankan:

- Signal Strength (SlowLen) = 21

## 4. Risk Management

Gunakan Box TP/SL otomatis.

### Risk Reward

- Default RR = 1.5
- Jangan gunakan RR < 1

### Exit Area

Jika label EXIT muncul sebelum TP:

- Amankan profit
- atau pindahkan SL ke Breakeven

---

# Checklist Sebelum Entry

| Komponen | BUY | SELL |
|----------|------|------|
| EMA 200 | Harga di atas EMA | Harga di bawah EMA |
| Signal | 💎 BUY | 💎 SELL |
| RSI | >45 dan mengarah naik | <55 dan mengarah turun |
| Session | London / New York | London / New York |

## Jika Sinyal Terlalu Cepat

Naikkan parameter:

```text
FastLen  = 9-10
SlowLen  = 21
```
