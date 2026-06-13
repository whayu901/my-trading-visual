# 📊 TradingView Setup Guide

## ✅ Checklist Setup

### 1️⃣ Pine Script
- [ ] Copy script dari `FINAL_PINE_WITH_WEBHOOK.pine`
- [ ] Paste ke Pine Editor
- [ ] Click "Add to Chart"
- [ ] Lihat tabel status (kanan atas) show "ACTIVE"

### 2️⃣ Alert Setup
- [ ] Click icon Alarm ⏰
- [ ] Create Alert
- [ ] Pilih indicator: `SR + Webhook Alert [FREE]`
- [ ] Pilih condition: `WEBHOOK SIGNAL`
- [ ] Set Webhook URL: `https://my-trading-visual.vercel.app/webhook`
- [ ] Create (1x saja!)

### 3️⃣ Verify Working
- [ ] Tunggu ada diamond signal
- [ ] Check Telegram dapat notification
- [ ] Check format message benar

---

## 📱 Notification Format

Saat signal muncul, Anda akan dapat di Telegram:

```
🟢 🚨 TRADING ALERT 🚨

📊 Symbol: XAUUSD
💰 Price: 2650.50
🎯 Action: BUY
📝 Signal: RBS RETEST - Old resistance now support
⏰ Time: 13/06/2026 20:45:30
```

---

## 🎯 Trading Rules

### BUY Signal (Green ◆)
1. **Support Hold**: Price bounce dari support
2. **RBS Retest**: Old resistance jadi support (BEST!)

### SELL Signal (Red ◆)
1. **Resistance Hold**: Price rejected dari resistance
2. **SBR Retest**: Old support jadi resistance (BEST!)

### WAIT Signal (Orange Zone)
- Lihat label "SBR ⚠" atau "RBS ⚠"
- TUNGGU pullback & retest
- Entry saat diamond muncul

---

## 🔧 Troubleshooting

**Q: Alert tidak masuk ke Telegram?**
- Check webhook URL benar (ada /webhook)
- Check bot token & chat ID sudah di-set
- Test manual: `curl -X POST...`

**Q: Diamond muncul tapi tidak ada alert?**
- Check alert condition benar
- Check webhook URL aktif
- Restart alert (delete & create baru)

**Q: Dapat alert tapi format aneh?**
- Update Pine Script ke versi terbaru
- Check message format di alert settings

---

## 📈 Tips Maksimal

1. **Timeframe Terbaik**:
   - M5 untuk scalping
   - M15 untuk day trading
   - H1 untuk swing trading

2. **Pair Recommended**:
   - XAUUSD (Gold) - high volatility
   - EURUSD - stable trends
   - GBPUSD - good momentum

3. **Best Entry**:
   - RBS/SBR retest (orange zone → diamond)
   - Confluence dengan trendline
   - Volume confirmation

4. **Risk Management**:
   - SL: Beyond box + 10 pips
   - TP: Next S/R atau 1:2 RR minimum
   - Max 2% risk per trade

---

## 🚀 Advanced Setup

### Multiple Pairs Monitoring
1. Add script ke multiple charts
2. 1 alert per pair (free account limit)
3. Atau rotate daily

### Custom Filters
Edit Pine Script untuk:
- Filter by time session
- Minimum volume threshold
- ADX/RSI confirmation

---

## 📞 Need Help?

- Check `TROUBLESHOOTING.md`
- Test dengan `test-webhook.sh`
- Verify bot dengan `verify-bot.sh`

Happy Trading! 💰