#!/bin/bash

echo "🚀 AUTOMATED TRADINGVIEW BACKTESTING SYSTEM"
echo "==========================================="
echo "Risk/Reward Ratio: 1:1"
echo "8 Years of Backtesting Experience"
echo ""

# Check connection
echo "📡 Checking TradingView connection..."
cd tradingview-mcp
STATUS=$(npm run tv status 2>/dev/null | tail -1)
echo "$STATUS"

# Start replay mode
echo ""
echo "📅 Starting replay mode from December 2024..."
npm run tv replay start -- --date "2024-12-01" 2>/dev/null | tail -1

echo ""
echo "🏁 RUNNING AUTOMATED BACKTEST"
echo "==========================================="

# Initialize variables
TRADES=0
WINS=0
LOSSES=0
BALANCE=10000
POSITION_OPEN=false
ENTRY_PRICE=0
STOP_LOSS=0
TAKE_PROFIT=0
DIRECTION=""
BAR=0
MAX_BARS=100

echo "Initial Balance: \$10,000"
echo ""

# Main backtest loop
while [ $BAR -lt $MAX_BARS ]; do
    BAR=$((BAR + 1))

    # Get current price
    QUOTE=$(npm run tv quote 2>/dev/null | tail -1)
    PRICE=$(echo "$QUOTE" | grep -o '"close":[0-9.]*' | cut -d: -f2)

    # Get indicator values
    VALUES=$(npm run tv values 2>/dev/null | tail -1)

    # Check for signals if no position open
    if [ "$POSITION_OPEN" = false ]; then
        # Check RBS Retest BUY signal
        RBS_BUY=$(echo "$VALUES" | grep -o '"RBS Retest - BUY":"[0-9.]*"' | cut -d'"' -f4)
        if [ ! -z "$RBS_BUY" ] && [ "$RBS_BUY" != "0.000" ]; then
            POSITION_OPEN=true
            DIRECTION="LONG"
            ENTRY_PRICE=$PRICE
            STOP_LOSS=$(echo "$PRICE - 0.5" | bc)
            TAKE_PROFIT=$(echo "$PRICE + 0.5" | bc)
            TRADES=$((TRADES + 1))

            echo "📍 TRADE #$TRADES OPENED"
            echo "   🟢 BUY Signal: RBS RETEST"
            echo "   Entry: \$$PRICE"
            echo "   Stop Loss: \$$STOP_LOSS (50 pips)"
            echo "   Take Profit: \$$TAKE_PROFIT (50 pips)"
            echo ""
        fi

        # Check SBR Retest SELL signal
        SBR_SELL=$(echo "$VALUES" | grep -o '"SBR Retest - SELL":"[0-9.]*"' | cut -d'"' -f4)
        if [ ! -z "$SBR_SELL" ] && [ "$SBR_SELL" != "0.000" ] && [ "$POSITION_OPEN" = false ]; then
            POSITION_OPEN=true
            DIRECTION="SHORT"
            ENTRY_PRICE=$PRICE
            STOP_LOSS=$(echo "$PRICE + 0.5" | bc)
            TAKE_PROFIT=$(echo "$PRICE - 0.5" | bc)
            TRADES=$((TRADES + 1))

            echo "📍 TRADE #$TRADES OPENED"
            echo "   🔴 SELL Signal: SBR RETEST"
            echo "   Entry: \$$PRICE"
            echo "   Stop Loss: \$$STOP_LOSS (50 pips)"
            echo "   Take Profit: \$$TAKE_PROFIT (50 pips)"
            echo ""
        fi
    else
        # Check if position hit SL or TP
        if [ "$DIRECTION" = "LONG" ]; then
            if (( $(echo "$PRICE <= $STOP_LOSS" | bc -l) )); then
                POSITION_OPEN=false
                LOSSES=$((LOSSES + 1))
                PNL=-50
                BALANCE=$(echo "$BALANCE + $PNL" | bc)
                echo "❌ TRADE CLOSED - STOP LOSS HIT"
                echo "   P&L: -\$50"
                echo "   Balance: \$$BALANCE"
                echo ""
            elif (( $(echo "$PRICE >= $TAKE_PROFIT" | bc -l) )); then
                POSITION_OPEN=false
                WINS=$((WINS + 1))
                PNL=50
                BALANCE=$(echo "$BALANCE + $PNL" | bc)
                echo "✅ TRADE CLOSED - TAKE PROFIT HIT"
                echo "   P&L: +\$50"
                echo "   Balance: \$$BALANCE"
                echo ""
            fi
        elif [ "$DIRECTION" = "SHORT" ]; then
            if (( $(echo "$PRICE >= $STOP_LOSS" | bc -l) )); then
                POSITION_OPEN=false
                LOSSES=$((LOSSES + 1))
                PNL=-50
                BALANCE=$(echo "$BALANCE + $PNL" | bc)
                echo "❌ TRADE CLOSED - STOP LOSS HIT"
                echo "   P&L: -\$50"
                echo "   Balance: \$$BALANCE"
                echo ""
            elif (( $(echo "$PRICE <= $TAKE_PROFIT" | bc -l) )); then
                POSITION_OPEN=false
                WINS=$((WINS + 1))
                PNL=50
                BALANCE=$(echo "$BALANCE + $PNL" | bc)
                echo "✅ TRADE CLOSED - TAKE PROFIT HIT"
                echo "   P&L: +\$50"
                echo "   Balance: \$$BALANCE"
                echo ""
            fi
        fi
    fi

    # Step replay
    npm run tv replay step 2>/dev/null >/dev/null

    # Progress update every 10 bars
    if [ $((BAR % 10)) -eq 0 ]; then
        echo -ne "\r📊 Progress: Bar $BAR/$MAX_BARS | Trades: $TRADES | W/L: $WINS/$LOSSES | Balance: \$$BALANCE"
    fi

    # Speed control
    sleep 0.3
done

echo ""
echo ""
echo "==========================================="
echo "📊 FINAL BACKTEST RESULTS"
echo "==========================================="
echo ""
echo "📈 PERFORMANCE SUMMARY:"
echo "   Total Trades: $TRADES"
echo "   Wins: $WINS"
echo "   Losses: $LOSSES"
if [ $TRADES -gt 0 ]; then
    WIN_RATE=$(echo "scale=1; $WINS * 100 / $TRADES" | bc)
    echo "   Win Rate: $WIN_RATE%"
fi
echo "   Final Balance: \$$BALANCE"
TOTAL_PNL=$(echo "$BALANCE - 10000" | bc)
echo "   Total P&L: \$$TOTAL_PNL"
ROI=$(echo "scale=2; $TOTAL_PNL * 100 / 10000" | bc)
echo "   ROI: $ROI%"
echo ""
echo "📊 RISK METRICS:"
echo "   Risk/Reward: 1:1"
echo "   Stop Loss: 50 pips"
echo "   Take Profit: 50 pips"
echo ""

# Stop replay
npm run tv replay stop 2>/dev/null >/dev/null

echo "✅ Backtest completed!"