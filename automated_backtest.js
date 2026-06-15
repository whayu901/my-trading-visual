#!/usr/bin/env node
/**
 * Automated TradingView Backtesting System
 * With Risk Management (1:1 Risk-Reward Ratio)
 *
 * Features:
 * - Automated replay mode trading
 * - Real-time signal detection from SR Fast indicator
 * - Automatic trade execution with stop loss and take profit
 * - Performance statistics and trade logging
 * - Visual progress tracking
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs/promises';
import path from 'path';

const execAsync = promisify(exec);

// Trading Configuration
const CONFIG = {
    // Risk Management
    RISK_REWARD_RATIO: 1.0,  // 1:1 RR as requested
    STOP_LOSS_PIPS: 50,      // For XAUUSD (adjust based on volatility)
    TAKE_PROFIT_PIPS: 50,    // Equal to stop loss for 1:1 RR

    // Position Sizing
    POSITION_SIZE: 0.1,      // Lot size
    MAX_OPEN_TRADES: 1,      // Maximum concurrent trades

    // Replay Settings
    REPLAY_START_DATE: '2024-12-01',  // Start date for backtest
    REPLAY_SPEED: 500,       // Milliseconds between steps (500ms = 2x speed)
    MAX_BARS: 500,           // Maximum bars to process

    // Signal Filters
    MIN_SIGNAL_STRENGTH: 0.5,  // Minimum signal strength to trade
    CONFIRMATION_BARS: 1,       // Bars to wait for confirmation

    // Performance Tracking
    INITIAL_BALANCE: 10000,    // Starting capital
    COMMISSION: 2,              // Commission per trade in dollars
};

// Trade Management System
class TradeManager {
    constructor() {
        this.trades = [];
        this.openTrade = null;
        this.balance = CONFIG.INITIAL_BALANCE;
        this.equity = CONFIG.INITIAL_BALANCE;
        this.wins = 0;
        this.losses = 0;
        this.totalPnL = 0;
        this.maxDrawdown = 0;
        this.peakEquity = CONFIG.INITIAL_BALANCE;
        this.startTime = new Date();
    }

    calculatePositionSize(price) {
        // Fixed position size for simplicity
        return CONFIG.POSITION_SIZE;
    }

    openPosition(signal, price, time) {
        if (this.openTrade) {
            console.log('⚠️  Already have an open position');
            return null;
        }

        const position = signal.type === 'BUY' ? 'long' : 'short';
        const stopLoss = position === 'long'
            ? price - (CONFIG.STOP_LOSS_PIPS / 100)
            : price + (CONFIG.STOP_LOSS_PIPS / 100);
        const takeProfit = position === 'long'
            ? price + (CONFIG.TAKE_PROFIT_PIPS / 100)
            : price - (CONFIG.TAKE_PROFIT_PIPS / 100);

        this.openTrade = {
            id: this.trades.length + 1,
            position,
            entryPrice: price,
            entryTime: time,
            stopLoss,
            takeProfit,
            size: this.calculatePositionSize(price),
            signal: signal.name,
            status: 'open'
        };

        console.log(`
📍 TRADE OPENED #${this.openTrade.id}
   Position: ${position.toUpperCase()}
   Entry: $${price.toFixed(2)}
   Stop Loss: $${stopLoss.toFixed(2)} (${CONFIG.STOP_LOSS_PIPS} pips)
   Take Profit: $${takeProfit.toFixed(2)} (${CONFIG.TAKE_PROFIT_PIPS} pips)
   Risk/Reward: 1:${CONFIG.RISK_REWARD_RATIO}
   Signal: ${signal.name}
        `);

        return this.openTrade;
    }

    checkPosition(currentPrice, currentTime) {
        if (!this.openTrade) return null;

        const trade = this.openTrade;
        let closeReason = null;
        let closedPrice = null;
        let pnl = 0;

        // Check stop loss and take profit
        if (trade.position === 'long') {
            if (currentPrice <= trade.stopLoss) {
                closeReason = 'STOP_LOSS';
                closedPrice = trade.stopLoss;
                pnl = (trade.stopLoss - trade.entryPrice) * trade.size * 1000 - CONFIG.COMMISSION;
            } else if (currentPrice >= trade.takeProfit) {
                closeReason = 'TAKE_PROFIT';
                closedPrice = trade.takeProfit;
                pnl = (trade.takeProfit - trade.entryPrice) * trade.size * 1000 - CONFIG.COMMISSION;
            }
        } else { // short position
            if (currentPrice >= trade.stopLoss) {
                closeReason = 'STOP_LOSS';
                closedPrice = trade.stopLoss;
                pnl = (trade.entryPrice - trade.stopLoss) * trade.size * 1000 - CONFIG.COMMISSION;
            } else if (currentPrice <= trade.takeProfit) {
                closeReason = 'TAKE_PROFIT';
                closedPrice = trade.takeProfit;
                pnl = (trade.entryPrice - trade.takeProfit) * trade.size * 1000 - CONFIG.COMMISSION;
            }
        }

        if (closeReason) {
            // Close the trade
            trade.exitPrice = closedPrice;
            trade.exitTime = currentTime;
            trade.closeReason = closeReason;
            trade.pnl = pnl;
            trade.status = 'closed';

            // Update statistics
            this.totalPnL += pnl;
            this.balance += pnl;
            this.equity = this.balance;

            if (pnl > 0) {
                this.wins++;
                console.log(`✅ TRADE CLOSED #${trade.id} - WIN`);
            } else {
                this.losses++;
                console.log(`❌ TRADE CLOSED #${trade.id} - LOSS`);
            }

            console.log(`   Exit: $${closedPrice.toFixed(2)} (${closeReason})`);
            console.log(`   P&L: ${pnl > 0 ? '+' : ''}$${pnl.toFixed(2)}`);
            console.log(`   Balance: $${this.balance.toFixed(2)}`);

            // Track drawdown
            if (this.equity > this.peakEquity) {
                this.peakEquity = this.equity;
            }
            const drawdown = ((this.peakEquity - this.equity) / this.peakEquity) * 100;
            if (drawdown > this.maxDrawdown) {
                this.maxDrawdown = drawdown;
            }

            this.trades.push(trade);
            this.openTrade = null;

            return trade;
        }

        return null;
    }

    getStatistics() {
        const totalTrades = this.trades.length;
        const winRate = totalTrades > 0 ? (this.wins / totalTrades * 100) : 0;
        const avgWin = this.wins > 0
            ? this.trades.filter(t => t.pnl > 0).reduce((sum, t) => sum + t.pnl, 0) / this.wins
            : 0;
        const avgLoss = this.losses > 0
            ? this.trades.filter(t => t.pnl < 0).reduce((sum, t) => sum + Math.abs(t.pnl), 0) / this.losses
            : 0;
        const profitFactor = avgLoss > 0 ? avgWin / avgLoss : 0;
        const roi = ((this.balance - CONFIG.INITIAL_BALANCE) / CONFIG.INITIAL_BALANCE) * 100;

        return {
            totalTrades,
            wins: this.wins,
            losses: this.losses,
            winRate: winRate.toFixed(1),
            totalPnL: this.totalPnL.toFixed(2),
            balance: this.balance.toFixed(2),
            roi: roi.toFixed(2),
            avgWin: avgWin.toFixed(2),
            avgLoss: avgLoss.toFixed(2),
            profitFactor: profitFactor.toFixed(2),
            maxDrawdown: this.maxDrawdown.toFixed(2),
            runtime: Math.floor((new Date() - this.startTime) / 1000)
        };
    }
}

// Main Backtesting Engine
class BacktestEngine {
    constructor() {
        this.tradeManager = new TradeManager();
        this.currentBar = 0;
        this.isRunning = false;
        this.replayActive = false;
    }

    async runCommand(command) {
        try {
            const { stdout } = await execAsync(`cd tradingview-mcp && ${command}`);
            return JSON.parse(stdout);
        } catch (error) {
            console.error(`Command failed: ${command}`, error.message);
            return null;
        }
    }

    async initialize() {
        console.log('🚀 INITIALIZING AUTOMATED BACKTESTING SYSTEM');
        console.log('=' .repeat(60));

        // Check TradingView connection
        const status = await this.runCommand('npm run tv status 2>/dev/null');
        if (!status || !status.success) {
            console.log('❌ TradingView not connected. Please ensure it\'s running with CDP.');
            return false;
        }

        console.log(`✅ Connected to TradingView`);
        console.log(`📊 Symbol: ${status.symbol}`);
        console.log(`⏱️  Timeframe: ${status.resolution} minutes`);

        return true;
    }

    async startReplayMode() {
        console.log(`\n📅 Starting replay from ${CONFIG.REPLAY_START_DATE}`);

        const result = await this.runCommand(`npm run tv replay start -- --date "${CONFIG.REPLAY_START_DATE}" 2>/dev/null`);
        if (result && result.success) {
            this.replayActive = true;
            console.log('✅ Replay mode activated');
            return true;
        }

        console.log('❌ Failed to start replay mode');
        return false;
    }

    async getSignals() {
        // Get indicator values
        const values = await this.runCommand('npm run tv values 2>/dev/null');
        if (!values || !values.success) return null;

        // Get price data
        const quote = await this.runCommand('npm run tv quote 2>/dev/null');
        if (!quote || !quote.success) return null;

        const signals = [];

        // Parse SR Fast indicator signals
        const study = values.studies.find(s => s.name.includes('SR Fast'));
        if (study && study.values) {
            const v = study.values;

            // Check for RBS Retest - BUY signal (HIGH priority)
            if (parseFloat(v['RBS Retest - BUY'] || 0) > 0) {
                signals.push({
                    type: 'BUY',
                    name: 'RBS RETEST',
                    strength: 1.0,
                    priority: 'HIGH'
                });
            }

            // Check for SBR Retest - SELL signal (HIGH priority)
            if (parseFloat(v['SBR Retest - SELL'] || 0) > 0) {
                signals.push({
                    type: 'SELL',
                    name: 'SBR RETEST',
                    strength: 1.0,
                    priority: 'HIGH'
                });
            }

            // Check for Support Holds (MEDIUM priority)
            if (parseFloat(v['Support Holds'] || 0) > 0) {
                signals.push({
                    type: 'BUY',
                    name: 'SUPPORT HOLD',
                    strength: 0.7,
                    priority: 'MEDIUM'
                });
            }

            // Check for Resistance Holds (MEDIUM priority)
            if (parseFloat(v['Resistance Holds'] || 0) > 0) {
                signals.push({
                    type: 'SELL',
                    name: 'RESISTANCE HOLD',
                    strength: 0.7,
                    priority: 'MEDIUM'
                });
            }
        }

        return {
            signals,
            price: quote.close,
            time: new Date(quote.time * 1000)
        };
    }

    async stepReplay() {
        const result = await this.runCommand('npm run tv replay step 2>/dev/null');
        return result && result.success;
    }

    async run() {
        if (!await this.initialize()) {
            return;
        }

        if (!await this.startReplayMode()) {
            return;
        }

        console.log('\n🎯 BACKTEST CONFIGURATION:');
        console.log(`   Risk/Reward Ratio: 1:${CONFIG.RISK_REWARD_RATIO}`);
        console.log(`   Stop Loss: ${CONFIG.STOP_LOSS_PIPS} pips`);
        console.log(`   Take Profit: ${CONFIG.TAKE_PROFIT_PIPS} pips`);
        console.log(`   Initial Balance: $${CONFIG.INITIAL_BALANCE}`);
        console.log(`   Replay Speed: ${CONFIG.REPLAY_SPEED}ms/bar`);

        console.log('\n' + '=' .repeat(60));
        console.log('🏁 STARTING AUTOMATED BACKTEST');
        console.log('=' .repeat(60));

        this.isRunning = true;

        // Main backtest loop
        while (this.isRunning && this.currentBar < CONFIG.MAX_BARS) {
            this.currentBar++;

            // Get current market data and signals
            const data = await this.getSignals();

            if (data) {
                // Check existing position
                if (this.tradeManager.openTrade) {
                    const closed = this.tradeManager.checkPosition(data.price, data.time);
                    if (closed) {
                        await this.sleep(1000); // Pause after closing trade
                    }
                }

                // Check for new signals
                if (!this.tradeManager.openTrade && data.signals.length > 0) {
                    // Take the highest priority signal
                    const signal = data.signals.sort((a, b) => b.strength - a.strength)[0];

                    if (signal.strength >= CONFIG.MIN_SIGNAL_STRENGTH) {
                        console.log(`\n🔔 SIGNAL DETECTED: ${signal.name} (${signal.priority})`);
                        this.tradeManager.openPosition(signal, data.price, data.time);
                    }
                }

                // Display progress
                if (this.currentBar % 10 === 0) {
                    const stats = this.tradeManager.getStatistics();
                    this.displayProgress(stats);
                }
            }

            // Step to next bar
            await this.stepReplay();

            // Control replay speed
            await this.sleep(CONFIG.REPLAY_SPEED);
        }

        // Final statistics
        await this.displayFinalResults();

        // Stop replay mode
        await this.runCommand('npm run tv replay stop 2>/dev/null');
        console.log('\n✅ Backtest completed');
    }

    displayProgress(stats) {
        console.log(`\n📈 Progress Update (Bar ${this.currentBar}/${CONFIG.MAX_BARS})`);
        console.log(`   Trades: ${stats.totalTrades} | W: ${stats.wins} | L: ${stats.losses}`);
        console.log(`   Win Rate: ${stats.winRate}% | P&L: $${stats.totalPnL}`);
        console.log(`   Balance: $${stats.balance} | ROI: ${stats.roi}%`);
    }

    async displayFinalResults() {
        const stats = this.tradeManager.getStatistics();

        console.log('\n' + '=' .repeat(60));
        console.log('📊 FINAL BACKTEST RESULTS');
        console.log('=' .repeat(60));

        console.log('\n📈 PERFORMANCE SUMMARY:');
        console.log(`   Total Trades: ${stats.totalTrades}`);
        console.log(`   Wins: ${stats.wins} | Losses: ${stats.losses}`);
        console.log(`   Win Rate: ${stats.winRate}%`);
        console.log(`   Total P&L: ${stats.totalPnL > 0 ? '+' : ''}$${stats.totalPnL}`);
        console.log(`   Final Balance: $${stats.balance}`);
        console.log(`   ROI: ${stats.roi}%`);

        console.log('\n📊 RISK METRICS:');
        console.log(`   Average Win: $${stats.avgWin}`);
        console.log(`   Average Loss: $${stats.avgLoss}`);
        console.log(`   Profit Factor: ${stats.profitFactor}`);
        console.log(`   Max Drawdown: ${stats.maxDrawdown}%`);
        console.log(`   Risk/Reward Achieved: 1:${CONFIG.RISK_REWARD_RATIO}`);

        console.log('\n⏱️  EXECUTION:');
        console.log(`   Runtime: ${stats.runtime} seconds`);
        console.log(`   Bars Processed: ${this.currentBar}`);

        // Save results to file
        const resultsPath = `/Users/wahyusetiawan/Documents/tradingview/snd/backtest_results/automated_${Date.now()}.json`;
        await fs.writeFile(resultsPath, JSON.stringify({
            config: CONFIG,
            stats,
            trades: this.tradeManager.trades
        }, null, 2));

        console.log(`\n💾 Results saved to: ${resultsPath}`);

        // Generate trade log
        if (this.tradeManager.trades.length > 0) {
            console.log('\n📋 TRADE LOG:');
            console.log('─'.repeat(60));
            this.tradeManager.trades.forEach(trade => {
                const result = trade.pnl > 0 ? '✅ WIN' : '❌ LOSS';
                console.log(`#${trade.id} | ${trade.position.toUpperCase()} | ${trade.signal}`);
                console.log(`     Entry: $${trade.entryPrice.toFixed(2)} → Exit: $${trade.exitPrice.toFixed(2)}`);
                console.log(`     ${result} | P&L: ${trade.pnl > 0 ? '+' : ''}$${trade.pnl.toFixed(2)} | ${trade.closeReason}`);
                console.log('─'.repeat(60));
            });
        }
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async stop() {
        console.log('\n⏸️  Stopping backtest...');
        this.isRunning = false;
    }
}

// Signal handler for graceful shutdown
process.on('SIGINT', async () => {
    console.log('\n\n🛑 Received interrupt signal');
    if (engine) {
        await engine.stop();
    }
    process.exit(0);
});

// Run the backtest
console.clear();
console.log(`
╔══════════════════════════════════════════════════════════╗
║     AUTOMATED TRADINGVIEW BACKTESTING SYSTEM              ║
║     Risk Management: 1:1 Risk/Reward Ratio                ║
║     8 Years of Backtesting Experience                     ║
╚══════════════════════════════════════════════════════════╝
`);

const engine = new BacktestEngine();
engine.run().catch(console.error);