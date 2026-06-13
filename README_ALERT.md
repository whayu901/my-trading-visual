# 🚨 FREE TradingView Alert System

> Dapat notifikasi trading GRATIS tanpa TradingView Premium!

## ⚡ QUICK START (15 Menit!)

### 1️⃣ Clone & Install
```bash
cd /Users/wahyusetiawan/Documents/tradingview/snd
npm install
```

### 2️⃣ Setup Telegram Bot
1. Buka Telegram
2. Chat **@BotFather**
3. Kirim `/newbot`
4. Beri nama bot (contoh: "MyTradingAlert")
5. **COPY TOKEN** yang diberikan

### 3️⃣ Dapatkan Chat ID
1. Chat **@userinfobot**
2. Kirim pesan apa saja
3. **COPY CHAT ID** yang diberikan

### 4️⃣ Run Setup
```bash
./quick-setup.sh
# Atau manual:
# - Edit .env file
# - Isi BOT_TOKEN dan CHAT_ID
```

### 5️⃣ Deploy ke Vercel (GRATIS!)
```bash
npm install -g vercel
vercel

# Ikuti prompt:
# - Setup new project? Yes
# - Link to existing? No
# - Project name: trading-alert
# - Directory: ./
# - Override settings? No
```

### 6️⃣ Setup di TradingView
1. Buka chart Anda
2. Add indicator: **supportAndResistance_FREE_ALERT.pine**
3. Klik Alert (jam alarm)
4. Settings:
   - Condition: `SR Free Alert` → `UNIVERSAL SIGNAL`
   - Webhook URL: `https://trading-alert.vercel.app/webhook`
5. Create Alert!

## ✅ DONE! Alert langsung ke HP Anda!

---

## 📱 Test Alert

Kirim test via curl:
```bash
curl -X POST https://your-app.vercel.app/webhook \
  -H "Content-Type: application/json" \
  -d '{"symbol":"XAUUSD","price":"2000","action":"BUY","message":"Test alert!"}'
```

---

## 🎯 Features

- ✅ **GRATIS 100%** - No subscription needed
- ✅ **Real-time** - Alert instant ke Telegram
- ✅ **All Signals** - 1 alert untuk semua signal
- ✅ **Mobile Ready** - Notifikasi langsung ke HP
- ✅ **Multiple Pairs** - Monitor banyak pair sekaligus

---

## 🔧 Troubleshooting

**Alert tidak masuk?**
- Check webhook URL benar
- Check bot token & chat ID
- Test manual dengan curl

**Vercel error?**
- Gunakan Railway.app atau Render.com
- Atau host di VPS gratis

---

## 💡 Pro Tips

1. **Maksimalkan 1 Alert:**
   ```pinescript
   // Gabung semua kondisi
   alertcondition(
     condition1 or condition2 or condition3,
     title="ALL SIGNALS"
   )
   ```

2. **Multi-Timeframe:**
   - 1 alert bisa monitor H1, H4, D1 sekaligus!

3. **Alert Rotation:**
   - Ganti pair tiap hari
   - Focus pada yang volatile

---

## 🚀 Advanced Features (Coming Soon)

- [ ] Discord integration
- [ ] Email alerts
- [ ] Auto-trading via exchange API
- [ ] Risk management calculator
- [ ] Multi-user support

---

## 🤝 Contributing

Fork, improve, and PR! Let's help trader yang belum mampu bayar subscription.

---

## 📞 Support

- Telegram Group: @freetradingalerts
- Issues: GitHub Issues
- Email: -

---

**Remember:** Profit konsisten > biaya subscription!
Tapi sambil nabung, pakai dulu yang gratis 😉

Happy Trading! 🚀💰