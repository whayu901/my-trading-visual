# 🔧 S&R Indicator Installation Guide for MT5 Mac

## Quick Installation Steps

---

## 📥 STEP 1: Install MT5 (if not yet)

**Download MT5 for Mac:**
```
https://www.xm.com/mt5/mac

1. Download XMTrading.dmg
2. Open file
3. Drag to Applications
4. Open from Applications
5. Create demo account
```

**Time:** ~10 minutes

---

## 📂 STEP 2: Locate MQL5 Indicators Folder

### Method 1: Using MT5 Menu (EASIEST)

```
1. Open MT5
2. Menu: File → Open Data Folder
3. Folder opens → Navigate to: MQL5 → Indicators
4. Keep this folder window open!
```

### Method 2: Direct Path (Mac)

```bash
# Open Finder
# Press: Cmd+Shift+G (Go to Folder)
# Paste this path:

~/Library/Application Support/MetaQuotes/Terminal

# Then find subfolder with random name (like D0E8209F77C8CF37AD8BF550E51FF075)
# Go to: MQL5 → Indicators
```

**Path looks like:**
```
/Users/[YourName]/Library/Application Support/MetaQuotes/Terminal/[RANDOM_ID]/MQL5/Indicators/
```

---

## 📋 STEP 3: Copy Indicator File

**1. Locate Downloaded File:**
```
/Users/wahyusetiawan/Documents/tradingview/snd/SupportResistance.mq5
```

**2. Copy to Indicators Folder:**
```
Method A - Drag & Drop:
- Find SupportResistance.mq5 in Finder
- Drag file to Indicators folder (from Step 2)
- Drop!

Method B - Terminal:
# Open Terminal app
cd ~/Documents/tradingview/snd
cp SupportResistance.mq5 ~/Library/Application\ Support/MetaQuotes/Terminal/*/MQL5/Indicators/
```

**Confirm:** You should see `SupportResistance.mq5` in the Indicators folder!

---

## ⚙️ STEP 4: Compile Indicator

### Open MetaEditor

```
In MT5:
1. Menu: Tools → MetaEditor (or press F4)
2. MetaEditor window opens
```

### Compile the Indicator

```
1. MetaEditor → File → Open
2. Navigate to: Indicators folder
3. Select: SupportResistance.mq5
4. Click Open

5. Code appears in editor
6. Click "Compile" button (or press F7)
7. Check "Errors" tab at bottom:
   ✅ Should show: "0 error(s), 0 warning(s)"
   ✅ Message: "Successfully compiled"

8. Close MetaEditor
```

**If errors appear:** Screenshot and send to me!

---

## 📊 STEP 5: Add Indicator to Chart

### Refresh Navigator

```
1. Back to MT5 main window
2. Menu: View → Navigator (or Cmd+N)
3. Navigator panel appears (usually left side)
```

### Load Indicator

```
1. In Navigator:
   - Expand: Indicators
   - Expand: Custom (or Examples)
   - Find: SupportResistance

2. Drag "SupportResistance" to chart
   or
   Double-click "SupportResistance"

3. Settings dialog appears:
```

### Configure Settings

```
╔═══════════════════════════════════════════════╗
║  SupportResistance Settings                   ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  Settings - Optimized for Scalping:          ║
║  ├─ Lookback Period: 10                       ║
║  ├─ Delta Volume Filter: 2                    ║
║  └─ Adjust Box Width: 1.0                     ║
║                                               ║
║  Display Options:                             ║
║  ├─ Show Boxes: ✅                            ║
║  ├─ Show Signals: ✅                          ║
║  ├─ Support Color: Green                      ║
║  └─ Resistance Color: Red                     ║
║                                               ║
║  [OK]  [Cancel]                               ║
╚═══════════════════════════════════════════════╝

Click OK!
```

---

## ✅ STEP 6: Verify Installation

### Check if Working

**You should see:**

1. **Green boxes** appearing at support levels
2. **Red boxes** appearing at resistance levels
3. **Diamond symbols (◆)** at rejection points:
   - Green diamonds below = BUY signals
   - Red diamonds above = SELL signals
4. **"Break Res"** / **"Break Sup"** labels when zones break

### Troubleshooting

**Problem 1: Indicator not in Navigator**
```
Solution:
1. Close MT5
2. Reopen MT5
3. Check Navigator → Indicators → Custom
```

**Problem 2: No boxes appearing**
```
Solution:
1. Check chart has enough bars (need 200+ bars)
2. Check settings: "Show Boxes" = true
3. Try different timeframe (M5 or M15)
4. Scroll chart to left (load more history)
```

**Problem 3: Compilation errors**
```
Solution:
1. Screenshot error message
2. Send to me for fix
3. Or download latest version
```

**Problem 4: Boxes not extending right**
```
This is normal - MT5 boxes update on each bar.
The indicator redraws boxes to current time automatically.
```

---

## 🎮 STEP 7: Setup for Backtesting

### Open Strategy Tester

```
1. MT5 Menu: View → Strategy Tester (Cmd+R)
2. Strategy Tester panel opens at bottom
```

### Configure Tester

```
Tab: Settings

Symbol: XAUUSD (or your preferred pair)
Period: M5 (or M15)
Mode: Every tick (most accurate)

Date range:
├─ From: 2024-01-01
└─ To: 2024-12-31

Visual Mode: ✅ ENABLED (Important!)
Delay: 10 ms

Optimization: Disabled
```

### Start Visual Backtesting

```
1. Click "Start" button
2. Visual mode chart opens
3. Indicator auto-loads on chart
4. Control playback:
   ├─ Space: Pause/Resume
   ├─ +: Speed up
   └─ -: Slow down

5. Watch for signals:
   ├─ Green ◆ below = BUY
   └─ Red ◆ above = SELL

6. Track results in spreadsheet!
```

---

## ⚙️ OPTIONAL: Customize Settings

### For Different Trading Styles

**M1 Ultra-Fast Scalping:**
```
Lookback Period: 7
Volume Filter: 1-2
Box Width: 0.8
```

**M5 Scalping (Default - Recommended):**
```
Lookback Period: 10
Volume Filter: 2
Box Width: 1.0
```

**M15 Swing Trading:**
```
Lookback Period: 20
Volume Filter: 4
Box Width: 0.8
```

**XAU High Volatility:**
```
Lookback Period: 10
Volume Filter: 2
Box Width: 1.2-1.5
```

### Change Settings

```
1. Right-click chart
2. "Indicators List"
3. Select "SupportResistance"
4. Click "Edit"
5. Adjust parameters
6. OK
```

---

## 📊 Understanding the Signals

### Box Colors

```
🟢 GREEN BOX (Solid border):
   - Support zone
   - Price likely to bounce UP
   - Entry: BUY when rejection appears

🔴 RED BOX (Solid border):
   - Resistance zone
   - Price likely to reject DOWN
   - Entry: SELL when rejection appears

🟢 GREEN BOX (was red):
   - Broken resistance → now support
   - Wait for retest
   - Entry: BUY on pullback

🔴 RED BOX (was green):
   - Broken support → now resistance
   - Wait for retest
   - Entry: SELL on pullback
```

### Diamond Signals

```
◆ GREEN DIAMOND BELOW candle:
   Signal: BUY
   Meaning: Support holds OR broken resistance retested
   Action: Enter LONG
   SL: Below box edge
   TP: Next resistance OR 1:2 RR

◆ RED DIAMOND ABOVE candle:
   Signal: SELL
   Meaning: Resistance holds OR broken support retested
   Action: Enter SHORT
   SL: Above box edge
   TP: Next support OR 1:2 RR
```

### Labels

```
"Break Res" (green):
   - Resistance broken
   - Wait for pullback
   - BUY when price retests

"Break Sup" (red):
   - Support broken
   - Wait for pullback
   - SELL when price retests
```

---

## 🎯 Next Steps

**After Installation:**

1. ✅ Run 1 week backtest (visual mode)
2. ✅ Track all signals in spreadsheet
3. ✅ Calculate win rate & RR
4. ✅ Compare with your signal provider
5. ✅ Adjust settings if needed
6. ✅ Ready for demo trading!
7. ✅ Then live trading with micro lots

**Remember:**
- Paper trade 1-2 weeks first
- Test different timeframes
- Find your optimal settings
- Risk 1-2% max per trade

---

## 🆘 Need Help?

**Common Issues:**

1. **Can't find Indicators folder**
   → Use: File → Open Data Folder

2. **Compilation errors**
   → Screenshot and report

3. **No signals appearing**
   → Check minimum bars (need 200+)
   → Scroll chart left to load history

4. **Boxes look weird**
   → Normal - they redraw each bar
   → This is how MT5 works

5. **Want to change colors**
   → Right-click chart → Indicators List → Edit

---

## 📁 File Locations

**Indicator file:**
```
/Users/wahyusetiawan/Documents/tradingview/snd/SupportResistance.mq5
```

**After installation:**
```
~/Library/Application Support/MetaQuotes/Terminal/[RANDOM]/MQL5/Indicators/SupportResistance.mq5
```

**Compiled file (auto-created):**
```
~/Library/Application Support/MetaQuotes/Terminal/[RANDOM]/MQL5/Indicators/SupportResistance.ex5
```

---

**Installation Time: ~10 minutes**
**Ready to backtest!** 🚀

Good luck bro!
