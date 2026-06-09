# 🍎 MT5 Setup Guide for Mac

## Complete Installation & Backtesting Tutorial

---

## 📥 STEP 1: Download & Install MT5

### Recommended: XM Trading (Best Mac Support)

**1. Go to XM Website:**
```
https://www.xm.com/mt5/mac
```

**2. Download:**
- Click "Download MT5 for Mac"
- File downloaded: `XMTrading.dmg` (~50MB)

**3. Install:**
```bash
1. Open XMTrading.dmg
2. Drag "XMTrading" to Applications folder
3. Close installer
4. Go to Applications
5. Double-click "XMTrading"
```

**4. Fix Security (if needed):**
```
If you see "Cannot open because developer cannot be verified":

1. System Settings (or System Preferences)
2. Privacy & Security
3. Scroll down to "Security"
4. Click "Open Anyway" next to XMTrading
5. Confirm "Open"
```

---

## 🔑 STEP 2: Create Demo Account

**1. Launch MT5**
- First time akan auto-open account wizard

**2. Create Demo:**
```
1. Window shows: "Open an account"
2. Find server: "XMTrading-Demo"
3. Click "Next"

Fill form:
- Name: [Your name or fake]
- Email: [Your email]
- Phone: [Your phone or fake]
- Account Type: Standard
- Deposit: 100,000 (virtual money)
- Leverage: 1:100
- Currency: USD

4. Click "Next"
5. Save login & password!
   Login: 12345678
   Password: abc123xyz
   Server: XMTrading-Demo
```

**3. Login:**
```
- MT5 akan auto-login
- Kalau tidak, klik:
  File → Login to Trade Account
  Enter login/password
```

---

## 📊 STEP 3: Setup Chart untuk Backtesting

**1. Add XAUUSD Chart:**
```
1. Market Watch (Cmd+M or View → Market Watch)
2. Right-click in Market Watch
3. Click "Symbols"
4. Find "XAUUSD" or "GOLD"
5. Click "Show"
6. Double-click "XAUUSD" → chart opens
```

**2. Set Timeframe:**
```
Top toolbar: Click "M5" (5 minutes)
or
Charts → Timeframe → M5
```

**3. Chart Setup:**
```
Right-click chart → Properties (Cmd+E):
✅ Show OHLC
✅ Show Ask line
✅ Show Period separators
✅ Show Grid
Chart: Black or White (your preference)
Candles: Green up, Red down
```

---

## 🔧 STEP 4: Install S&R Indicator (MQL5 Version)

### Method A: Manual Installation

**1. Open MQL5 Folder:**
```bash
Finder → Go → Go to Folder (Cmd+Shift+G)

Paste this path:
~/Library/Application Support/MetaQuotes/Terminal/[RANDOM_ID]/MQL5/Indicators

or easier:
In MT5: File → Open Data Folder
Then: MQL5 → Indicators
```

**2. Copy Indicator File:**
```
- Copy supportandresistance.mq5 to Indicators folder
- (I'll provide this file after setup!)
```

**3. Compile & Load:**
```
1. MT5: Tools → MetaEditor (or F4)
2. File → Open → supportandresistance.mq5
3. Click "Compile" button (F7)
4. Check "Errors" tab (should be 0 errors)
5. Close MetaEditor

Back to MT5:
6. Navigator (Cmd+N)
7. Indicators → Custom
8. Find "supportandresistance"
9. Drag to chart
10. Settings popup → OK
```

---

## 🎮 STEP 5: Strategy Tester (Backtesting)

### Visual Mode (Manual Backtesting)

**1. Open Strategy Tester:**
```
View → Strategy Tester (Cmd+R)
or
Tools → Strategy Tester
```

**2. Settings:**
```
Tab: "Settings"

Symbol: XAUUSD
Period: M5 (or M15)
Mode: "Every tick" (most accurate)
Optimization: Disabled

Date Range:
- From: 2024-01-01
- To: 2024-12-31
(atau pilih range yang lu mau)

Visual Mode: ✅ ENABLED (Important!)
Delay: 10 ms (untuk speed control)
```

**3. Add Indicator to Tester:**
```
PENTING: Indicator harus di-attach ke chart SEBELUM run tester!

1. Click "Start" di Strategy Tester
2. Visual mode chart akan muncul
3. Drag indicator dari Navigator ke visual chart
4. Set parameters (lookback=10, dll)
```

**4. Control Replay:**
```
Bottom panel controls:

⏸️ Pause/Play
⏩ Speed up (klik multiple times)
⏪ Speed down
⏹️ Stop

Speed options: 1x, 2x, 4x, 8x, 16x, 32x

Keyboard shortcuts:
Space: Pause/Resume
+ : Speed up
- : Speed down
```

---

## 📝 STEP 6: Manual Backtesting Process

### Trading Journal Method

**1. Setup Spreadsheet:**
```
Google Sheets atau Excel dengan kolom:
- Date/Time
- Setup Type (First Touch, Break&Retest, dll)
- Entry Price
- Stop Loss
- Take Profit
- Result (Win/Loss)
- Pips
- RR
- Notes
```

**2. Backtesting Flow:**
```
1. Run visual mode
2. Watch candles form
3. When diamond appears:

   GREEN ◆ below = BUY signal:
   - Pause (Space)
   - Screenshot
   - Note entry price (crosshair tool)
   - Calculate SL (below box edge)
   - Calculate TP (next resistance or 1:2 RR)
   - Resume
   - Track result

   RED ◆ above = SELL signal:
   - Same process

4. Log ke spreadsheet
5. Continue replay
```

**3. Example Entry Log:**
```
Date: 2024-03-15 10:30
Setup: Break & Retest (Resistance → Support)
Signal: Green diamond at 2,315
Entry: 2,316.00
SL: 2,311.00 (5 pips below box)
TP: 2,326.00 (10 pips = 1:2 RR)
Result: WIN
Pips: +10
RR: 1:2
Notes: Clean retest, strong volume
```

---

## 🎯 STEP 7: Advanced Features

### Historical Data Download

**1. Get More Data:**
```
1. Market Watch → Right-click symbol
2. "Charts" → Period → M5
3. Scroll chart to very left (older data)
4. MT5 auto-downloads
5. Wait until "Download complete" message
```

**2. Data Range:**
```
Most brokers:
- XM: 2-3 years M5 data
- IC Markets: 3-5 years
- More than enough for backtesting!
```

### Multiple Timeframe Analysis

**1. Open Multiple Charts:**
```
File → New Chart → XAUUSD

Setup 3 windows:
- Chart 1: M15 (spotting)
- Chart 2: M5 (execution)
- Chart 3: M1 (timing)

Window → Tile Vertically
```

**2. Sync Time:**
```
Right-click chart → Chart Sync → Group 1
Do for all charts → all sync together!
```

---

## 🔍 TROUBLESHOOTING

### Issue 1: Indicator Not Showing
```
Solution:
1. Check compilation errors (MetaEditor)
2. Restart MT5
3. Re-drag indicator to chart
4. Check settings: "Show Boxes" = true
```

### Issue 2: No Historical Data
```
Solution:
1. Market Watch → Right-click XAUUSD
2. "Chart Window"
3. Scroll left to load data
4. Wait for download
```

### Issue 3: Visual Mode Laggy
```
Solution:
1. Close other apps
2. Reduce tester speed
3. Disable other indicators
4. Use simpler chart theme
```

### Issue 4: Can't Find MQL5 Folder
```
Run in Terminal:
open ~/Library/Application\ Support/MetaQuotes/

or

MT5: File → Open Data Folder
```

---

## 📊 NEXT STEPS

After setup complete:

1. ✅ I'll convert your Pine Script to MQL5
2. ✅ You install indicator
3. ✅ Run 1 month backtest
4. ✅ Compare with signal provider results
5. ✅ Optimize settings if needed
6. ✅ Ready for live trading!

---

## 🆘 NEED HELP?

**Common Questions:**

**Q: MT5 crashes on Mac?**
A: Update to latest MacOS, or use WebTerminal instead

**Q: Indicator errors?**
A: Send me screenshot, I'll fix

**Q: Demo account expired?**
A: Create new one (unlimited demo accounts)

**Q: Missing data?**
A: Use different broker (IC Markets has more historical data)

---

## 🎁 BONUS: Keyboard Shortcuts

```
Essential MT5 Shortcuts:

Cmd+M : Market Watch
Cmd+N : Navigator
Cmd+T : Terminal (trades)
Cmd+R : Strategy Tester
Cmd+E : Chart properties
F1    : Help
F4    : MetaEditor
Space : Pause/Resume (in tester)
+/-   : Speed control

Chart Tools:
Cmd+I : Indicators list
Cmd+B : Objects list
Cmd+G : Grid on/off
```

---

**Setup time: ~15 minutes**
**Ready for serious backtesting!** 🚀

Good luck bro!
