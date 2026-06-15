#!/usr/bin/env python3
"""
Automated TradingView Backtesting System
With Risk Management (1:1 Risk-Reward Ratio)
8 Years of Experience in Automated Trading
"""

import json
import time
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import os

class Colors:
    """Terminal colors for better visualization"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class TradeManager:
    """Manages trades with 1:1 Risk-Reward ratio"""

    def __init__(self, initial_balance=10000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.trades = []
        self.open_trade = None
        self.wins = 0
        self.losses = 0
        self.total_pnl = 0
        self.max_drawdown = 0
        self.peak_equity = initial_balance

        # Risk Management Settings (1:1 RR)
        self.risk_reward = 1.0
        self.stop_loss_pips = 50  # For XAUUSD
        self.take_profit_pips = 50  # Equal for 1:1 RR
        self.position_size = 0.1  # Lot size

    def open_position(self, signal_type: str, price: float, signal_name: str) -> Dict:
        """Open a new position with proper risk management"""
        if self.open_trade:
            return None

        direction = 'LONG' if signal_type == 'BUY' else 'SHORT'

        if direction == 'LONG':
            stop_loss = price - (self.stop_loss_pips / 100)
            take_profit = price + (self.take_profit_pips / 100)
        else:
            stop_loss = price + (self.stop_loss_pips / 100)
            take_profit = price - (self.take_profit_pips / 100)

        self.open_trade = {
            'id': len(self.trades) + 1,
            'direction': direction,
            'entry_price': price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'size': self.position_size,
            'signal': signal_name,
            'entry_time': datetime.now()
        }

        print(f"\n{Colors.BOLD}📍 TRADE OPENED #{self.open_trade['id']}{Colors.END}")
        print(f"   Direction: {Colors.GREEN if direction == 'LONG' else Colors.RED}{direction}{Colors.END}")
        print(f"   Entry: ${price:.2f}")
        print(f"   Stop Loss: ${stop_loss:.2f} ({self.stop_loss_pips} pips)")
        print(f"   Take Profit: ${take_profit:.2f} ({self.take_profit_pips} pips)")
        print(f"   Risk/Reward: 1:{self.risk_reward}")
        print(f"   Signal: {signal_name}")

        return self.open_trade

    def check_position(self, current_price: float) -> Optional[Dict]:
        """Check if position hit SL or TP"""
        if not self.open_trade:
            return None

        trade = self.open_trade
        closed = False
        pnl = 0

        if trade['direction'] == 'LONG':
            if current_price <= trade['stop_loss']:
                pnl = (trade['stop_loss'] - trade['entry_price']) * trade['size'] * 1000
                trade['exit_price'] = trade['stop_loss']
                trade['exit_reason'] = 'STOP LOSS'
                closed = True
            elif current_price >= trade['take_profit']:
                pnl = (trade['take_profit'] - trade['entry_price']) * trade['size'] * 1000
                trade['exit_price'] = trade['take_profit']
                trade['exit_reason'] = 'TAKE PROFIT'
                closed = True
        else:  # SHORT
            if current_price >= trade['stop_loss']:
                pnl = (trade['entry_price'] - trade['stop_loss']) * trade['size'] * 1000
                trade['exit_price'] = trade['stop_loss']
                trade['exit_reason'] = 'STOP LOSS'
                closed = True
            elif current_price <= trade['take_profit']:
                pnl = (trade['entry_price'] - trade['take_profit']) * trade['size'] * 1000
                trade['exit_price'] = trade['take_profit']
                trade['exit_reason'] = 'TAKE PROFIT'
                closed = True

        if closed:
            trade['pnl'] = pnl
            self.total_pnl += pnl
            self.balance += pnl

            if pnl > 0:
                self.wins += 1
                result_color = Colors.GREEN
                result_text = "WIN"
            else:
                self.losses += 1
                result_color = Colors.RED
                result_text = "LOSS"

            print(f"\n{result_color}{'✅' if pnl > 0 else '❌'} TRADE CLOSED #{trade['id']} - {result_text}{Colors.END}")
            print(f"   Exit: ${trade['exit_price']:.2f} ({trade['exit_reason']})")
            print(f"   P&L: {'+' if pnl > 0 else ''}${pnl:.2f}")
            print(f"   Balance: ${self.balance:.2f}")

            # Update drawdown
            if self.balance > self.peak_equity:
                self.peak_equity = self.balance
            drawdown = ((self.peak_equity - self.balance) / self.peak_equity) * 100
            if drawdown > self.max_drawdown:
                self.max_drawdown = drawdown

            self.trades.append(trade)
            self.open_trade = None

            return trade

        return None

    def get_statistics(self) -> Dict:
        """Get trading statistics"""
        total_trades = len(self.trades)
        win_rate = (self.wins / total_trades * 100) if total_trades > 0 else 0
        roi = ((self.balance - self.initial_balance) / self.initial_balance) * 100

        return {
            'total_trades': total_trades,
            'wins': self.wins,
            'losses': self.losses,
            'win_rate': win_rate,
            'total_pnl': self.total_pnl,
            'balance': self.balance,
            'roi': roi,
            'max_drawdown': self.max_drawdown
        }

class BacktestEngine:
    """Main backtesting engine with TradingView integration"""

    def __init__(self):
        self.trade_manager = TradeManager()
        self.current_bar = 0
        self.max_bars = 200  # Limit for demo
        self.replay_speed = 0.5  # Seconds between bars
        self.is_running = False

    def run_tv_command(self, command: str) -> Optional[Dict]:
        """Execute TradingView CLI command"""
        try:
            result = subprocess.run(
                f"cd tradingview-mcp && {command}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0 and result.stdout:
                # Try to parse JSON from stdout
                lines = result.stdout.strip().split('\n')
                for line in reversed(lines):
                    if line.strip().startswith('{'):
                        return json.loads(line)
            return None
        except Exception as e:
            return None

    def check_connection(self) -> bool:
        """Check if TradingView is connected"""
        status = self.run_tv_command("npm run tv status")
        if status and status.get('success'):
            print(f"{Colors.GREEN}✅ Connected to TradingView{Colors.END}")
            print(f"   Symbol: {status.get('symbol', 'Unknown')}")
            print(f"   Timeframe: {status.get('resolution', 'Unknown')} min")
            return True
        return False

    def start_replay(self, start_date: str) -> bool:
        """Start replay mode"""
        print(f"\n{Colors.CYAN}📅 Starting replay from {start_date}{Colors.END}")
        result = self.run_tv_command(f'npm run tv replay start -- --date "{start_date}"')
        if result and result.get('success'):
            print(f"{Colors.GREEN}✅ Replay mode activated{Colors.END}")
            return True
        return False

    def get_signals(self) -> Optional[Tuple[List[Dict], float]]:
        """Get trading signals from SR Fast indicator"""
        # Get indicator values
        values = self.run_tv_command("npm run tv values")
        if not values or not values.get('success'):
            return None

        # Get current price
        quote = self.run_tv_command("npm run tv quote")
        if not quote or not quote.get('success'):
            return None

        signals = []
        current_price = quote.get('close', 0)

        # Parse SR Fast signals
        for study in values.get('studies', []):
            if 'SR Fast' in study.get('name', ''):
                vals = study.get('values', {})

                # High priority signals
                if float(vals.get('RBS Retest - BUY', 0)) > 0:
                    signals.append({
                        'type': 'BUY',
                        'name': '🟢 RBS RETEST (HIGH)',
                        'strength': 1.0
                    })

                if float(vals.get('SBR Retest - SELL', 0)) > 0:
                    signals.append({
                        'type': 'SELL',
                        'name': '🔴 SBR RETEST (HIGH)',
                        'strength': 1.0
                    })

                # Medium priority signals
                if float(vals.get('Support Holds', 0)) > 0:
                    signals.append({
                        'type': 'BUY',
                        'name': '🟢 SUPPORT HOLD (MED)',
                        'strength': 0.7
                    })

                if float(vals.get('Resistance Holds', 0)) > 0:
                    signals.append({
                        'type': 'SELL',
                        'name': '🔴 RESISTANCE HOLD (MED)',
                        'strength': 0.7
                    })

        return signals, current_price

    def step_replay(self) -> bool:
        """Advance one bar in replay"""
        result = self.run_tv_command("npm run tv replay step")
        return result and result.get('success')

    def display_header(self):
        """Display backtest header"""
        print("\n" + "="*60)
        print(f"{Colors.BOLD}🤖 AUTOMATED TRADINGVIEW BACKTESTING SYSTEM{Colors.END}")
        print(f"{Colors.CYAN}8 Years of Backtesting Experience{Colors.END}")
        print("="*60)
        print(f"\n{Colors.YELLOW}⚙️  CONFIGURATION:{Colors.END}")
        print(f"   Risk/Reward: 1:{self.trade_manager.risk_reward}")
        print(f"   Stop Loss: {self.trade_manager.stop_loss_pips} pips")
        print(f"   Take Profit: {self.trade_manager.take_profit_pips} pips")
        print(f"   Initial Balance: ${self.trade_manager.initial_balance:,.2f}")
        print(f"   Position Size: {self.trade_manager.position_size} lot")

    def display_progress(self):
        """Display progress bar and stats"""
        stats = self.trade_manager.get_statistics()
        progress = (self.current_bar / self.max_bars) * 100

        # Progress bar
        bar_length = 40
        filled = int(bar_length * self.current_bar / self.max_bars)
        bar = '█' * filled + '░' * (bar_length - filled)

        print(f"\r{Colors.CYAN}Progress: [{bar}] {progress:.1f}% | "
              f"Trades: {stats['total_trades']} | "
              f"W/L: {stats['wins']}/{stats['losses']} | "
              f"P&L: ${stats['total_pnl']:.2f}{Colors.END}", end='')

    def display_final_results(self):
        """Display final backtest results"""
        stats = self.trade_manager.get_statistics()

        print("\n\n" + "="*60)
        print(f"{Colors.BOLD}{Colors.GREEN}📊 FINAL BACKTEST RESULTS{Colors.END}")
        print("="*60)

        print(f"\n{Colors.YELLOW}📈 PERFORMANCE:{Colors.END}")
        print(f"   Total Trades: {stats['total_trades']}")
        print(f"   Wins: {Colors.GREEN}{stats['wins']}{Colors.END}")
        print(f"   Losses: {Colors.RED}{stats['losses']}{Colors.END}")
        print(f"   Win Rate: {stats['win_rate']:.1f}%")

        pnl_color = Colors.GREEN if stats['total_pnl'] > 0 else Colors.RED
        print(f"   Total P&L: {pnl_color}{'+' if stats['total_pnl'] > 0 else ''}${stats['total_pnl']:.2f}{Colors.END}")
        print(f"   Final Balance: ${stats['balance']:.2f}")

        roi_color = Colors.GREEN if stats['roi'] > 0 else Colors.RED
        print(f"   ROI: {roi_color}{stats['roi']:.2f}%{Colors.END}")
        print(f"   Max Drawdown: {Colors.YELLOW}{stats['max_drawdown']:.2f}%{Colors.END}")

        # Trade log
        if self.trade_manager.trades:
            print(f"\n{Colors.YELLOW}📋 TRADE LOG:{Colors.END}")
            print("-"*60)
            for trade in self.trade_manager.trades[-5:]:  # Show last 5 trades
                pnl = trade['pnl']
                color = Colors.GREEN if pnl > 0 else Colors.RED
                print(f"#{trade['id']} {trade['direction']} | {trade['signal']}")
                print(f"   Entry: ${trade['entry_price']:.2f} → Exit: ${trade['exit_price']:.2f}")
                print(f"   {color}{'✅' if pnl > 0 else '❌'} {trade['exit_reason']} | P&L: ${pnl:.2f}{Colors.END}")
                print("-"*60)

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backtest_results/auto_backtest_{timestamp}.json"
        os.makedirs("backtest_results", exist_ok=True)

        with open(filename, 'w') as f:
            json.dump({
                'stats': stats,
                'trades': self.trade_manager.trades,
                'config': {
                    'risk_reward': self.trade_manager.risk_reward,
                    'stop_loss_pips': self.trade_manager.stop_loss_pips,
                    'take_profit_pips': self.trade_manager.take_profit_pips
                }
            }, f, indent=2, default=str)

        print(f"\n💾 Results saved to: {filename}")

    def run(self):
        """Main backtest loop"""
        self.display_header()

        # Check connection
        if not self.check_connection():
            print(f"\n{Colors.RED}❌ TradingView not connected!{Colors.END}")
            print("Please ensure TradingView is running with CDP on port 9222")
            return

        # Start replay mode
        if not self.start_replay("2024-12-01"):
            print(f"\n{Colors.RED}❌ Failed to start replay mode{Colors.END}")
            return

        print(f"\n{Colors.GREEN}🏁 STARTING AUTOMATED BACKTEST{Colors.END}")
        print("="*60)

        self.is_running = True

        try:
            while self.is_running and self.current_bar < self.max_bars:
                self.current_bar += 1

                # Get signals and price
                signal_data = self.get_signals()
                if signal_data:
                    signals, price = signal_data

                    # Check existing position
                    if self.trade_manager.open_trade:
                        closed = self.trade_manager.check_position(price)
                        if closed:
                            time.sleep(1)  # Pause for visual effect

                    # Check for new signals (only if no open trade)
                    if not self.trade_manager.open_trade and signals:
                        # Take the strongest signal
                        best_signal = max(signals, key=lambda x: x['strength'])
                        if best_signal['strength'] >= 0.7:  # Min threshold
                            print(f"\n\n🔔 {Colors.YELLOW}SIGNAL DETECTED: {best_signal['name']}{Colors.END}")
                            self.trade_manager.open_position(
                                best_signal['type'],
                                price,
                                best_signal['name']
                            )
                            time.sleep(1)

                # Step replay
                self.step_replay()

                # Update progress
                if self.current_bar % 5 == 0:
                    self.display_progress()

                # Control speed
                time.sleep(self.replay_speed)

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}⏸️  Backtest interrupted{Colors.END}")
        finally:
            # Stop replay
            self.run_tv_command("npm run tv replay stop")

            # Display results
            self.display_final_results()
            print(f"\n{Colors.GREEN}✅ Backtest completed!{Colors.END}\n")

def main():
    """Main entry point"""
    # Clear screen
    os.system('clear' if os.name == 'posix' else 'cls')

    # Create and run backtest
    engine = BacktestEngine()
    engine.run()

if __name__ == "__main__":
    main()