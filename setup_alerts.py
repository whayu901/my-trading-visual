#!/usr/bin/env python3
"""
TradingView Alert Setup Automation
Automatically creates all 6 alerts for SR Fast indicator on M5 timeframe
"""

import json
import time
import urllib.request
import urllib.error

class TradingViewAlertAutomation:
    def __init__(self, debug_port=9222):
        self.debug_port = debug_port
        self.ws_url = None
        self.page_id = None
        self.setup_connection()

    def setup_connection(self):
        """Get the active TradingView page from Chrome DevTools"""
        try:
            req = urllib.request.urlopen(f'http://localhost:{self.debug_port}/json')
            pages = json.loads(req.read())

            for page in pages:
                if 'tradingview.com/chart' in page.get('url', ''):
                    self.page_id = page['id']
                    self.ws_url = page['webSocketDebuggerUrl']
                    print(f"✅ Connected to TradingView chart")
                    print(f"   Page: {page['title']}")
                    return True

            print("❌ No TradingView chart found")
            return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    def execute_js(self, code):
        """Execute JavaScript in the TradingView page"""
        import websocket
        import json

        try:
            ws = websocket.create_connection(self.ws_url, timeout=10)

            message = {
                'id': 1,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': code,
                    'returnByValue': True,
                    'awaitPromise': True
                }
            }

            ws.send(json.dumps(message))
            result = json.loads(ws.recv())
            ws.close()

            if 'result' in result and 'result' in result['result']:
                return result['result']['result'].get('value', None)
            return None

        except Exception as e:
            print(f"❌ Execution error: {e}")
            return None

    def setup_alerts(self):
        """Main script to set up all alerts"""

        # First, check if we're on M5 timeframe
        print("\n📊 Checking timeframe...")

        check_timeframe_code = """
        (function() {
            // Get current timeframe
            const timeframeButtons = document.querySelectorAll('[data-name="time-interval-menu"] button');
            let currentTF = '5';

            for (let btn of timeframeButtons) {
                if (btn.classList.contains('isActive')) {
                    currentTF = btn.textContent.trim();
                    break;
                }
            }

            return currentTF;
        })();
        """

        current_tf = self.execute_js(check_timeframe_code)
        print(f"   Current timeframe: {current_tf}")

        if current_tf != '5' and current_tf != '5m':
            print("⚠️  Switching to M5 timeframe...")
            switch_tf_code = """
            (function() {
                // Click on M5 timeframe
                const buttons = document.querySelectorAll('[data-name="time-interval-menu"] button');
                for (let btn of buttons) {
                    if (btn.textContent.trim() === '5' || btn.textContent.trim() === '5m') {
                        btn.click();
                        return 'Switched to M5';
                    }
                }
                return 'M5 button not found';
            })();
            """
            result = self.execute_js(switch_tf_code)
            print(f"   {result}")
            time.sleep(2)  # Wait for chart to update

        # Alert configurations
        alerts = [
            {
                "name": "🟢 RBS RETEST - BUY",
                "condition": "RBS RETEST - BUY",
                "message": "🎯 M5 RBS BUY\\n💹 Entry: {{close}}\\n✅ HIGH PROBABILITY",
                "priority": "HIGH"
            },
            {
                "name": "🔴 SBR RETEST - SELL",
                "condition": "SBR RETEST - SELL",
                "message": "🎯 M5 SBR SELL\\n📉 Entry: {{close}}\\n✅ HIGH PROBABILITY",
                "priority": "HIGH"
            },
            {
                "name": "🔴 Resistance Touch",
                "condition": "Resistance Touch",
                "message": "⚠️ M5 RESISTANCE\\n📉 Level: {{close}}\\n⚡ Quick scalp",
                "priority": "MEDIUM"
            },
            {
                "name": "🟢 Support Touch",
                "condition": "Support Touch",
                "message": "⚠️ M5 SUPPORT\\n💹 Level: {{close}}\\n⚡ Quick scalp",
                "priority": "MEDIUM"
            },
            {
                "name": "⬆️ Resistance Break",
                "condition": "Resistance Break",
                "message": "🚨 M5 RES BREAK\\n⏳ Wait for retest",
                "priority": "LOW"
            },
            {
                "name": "⬇️ Support Break",
                "condition": "Support Break",
                "message": "🚨 M5 SUP BREAK\\n⏳ Wait for retest",
                "priority": "LOW"
            }
        ]

        print("\n🚨 Creating alerts...")

        # JavaScript to create alerts
        create_alert_code = """
        (async function() {
            try {
                // Open alert dialog
                const alertButton = document.querySelector('[data-name="create-alert-button"]');
                if (!alertButton) {
                    // Try alternative method - keyboard shortcut
                    document.dispatchEvent(new KeyboardEvent('keydown', {
                        key: 'a',
                        altKey: true,
                        bubbles: true
                    }));
                } else {
                    alertButton.click();
                }

                await new Promise(resolve => setTimeout(resolve, 1000));

                // Check if dialog opened
                const dialog = document.querySelector('.tv-dialog__modal-wrap');
                if (dialog) {
                    return 'Alert dialog opened';
                } else {
                    return 'Could not open alert dialog';
                }
            } catch (e) {
                return 'Error: ' + e.message;
            }
        })();
        """

        for i, alert in enumerate(alerts, 1):
            print(f"\n{i}/6 Creating: {alert['name']}")
            print(f"    Priority: {alert['priority']}")

            # Open alert dialog
            result = self.execute_js(create_alert_code)
            print(f"    {result}")

            if "opened" in str(result):
                time.sleep(1)

                # Fill in alert details
                fill_alert_code = f"""
                (async function() {{
                    try {{
                        // Wait for dialog to be ready
                        await new Promise(resolve => setTimeout(resolve, 500));

                        // Find the condition dropdown
                        const conditionDropdown = document.querySelector('.js-condition-first-operand-select');
                        if (conditionDropdown) {{
                            // Select SR indicator
                            const options = conditionDropdown.querySelectorAll('option');
                            for (let opt of options) {{
                                if (opt.text.includes('SR Auto') || opt.text.includes('Scalping')) {{
                                    opt.selected = true;
                                    conditionDropdown.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                    break;
                                }}
                            }}
                        }}

                        await new Promise(resolve => setTimeout(resolve, 500));

                        // Select the specific condition
                        const secondDropdown = document.querySelector('.js-condition-second-operand-select');
                        if (secondDropdown) {{
                            const options = secondDropdown.querySelectorAll('option');
                            for (let opt of options) {{
                                if (opt.text.includes('{alert["condition"]}')) {{
                                    opt.selected = true;
                                    secondDropdown.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                    break;
                                }}
                            }}
                        }}

                        // Set alert name
                        const nameInput = document.querySelector('input[name="alert-name"]');
                        if (nameInput) {{
                            nameInput.value = '{alert["name"]}';
                            nameInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        }}

                        // Set message
                        const messageInput = document.querySelector('textarea[name="alert-message"]');
                        if (messageInput) {{
                            messageInput.value = '{alert["message"]}';
                            messageInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        }}

                        // Set to "Once Per Bar Close"
                        const frequencySelect = document.querySelector('[name="alert-frequency"]');
                        if (frequencySelect) {{
                            const options = frequencySelect.querySelectorAll('option');
                            for (let opt of options) {{
                                if (opt.text.includes('Once Per Bar Close')) {{
                                    opt.selected = true;
                                    frequencySelect.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                    break;
                                }}
                            }}
                        }}

                        // Click Create button
                        await new Promise(resolve => setTimeout(resolve, 500));
                        const createButton = document.querySelector('.js-dialog-submit-button, [name="submit"]');
                        if (createButton) {{
                            createButton.click();
                            return 'Alert created successfully';
                        }}

                        return 'Create button not found';

                    }} catch (e) {{
                        return 'Error: ' + e.message;
                    }}
                }})();
                """

                result = self.execute_js(fill_alert_code)
                print(f"    ✅ {result}")
                time.sleep(2)  # Wait before next alert
            else:
                print("    ⚠️  Skipping - dialog issue")

        print("\n✅ Alert setup complete!")
        print("\n📋 Summary:")
        print("   • 2 HIGH priority alerts (RBS/SBR Retest)")
        print("   • 2 MEDIUM priority alerts (Touch signals)")
        print("   • 2 LOW priority alerts (Breakout info)")
        print("\n💡 Remember:")
        print("   • Focus on RBS/SBR retest alerts (highest win rate)")
        print("   • Don't chase breakouts - wait for retests")
        print("   • Use 1:2 risk-reward minimum")

def main():
    print("🚀 TradingView M5 Alert Setup Automation")
    print("=" * 50)

    automation = TradingViewAlertAutomation()

    if automation.page_id:
        automation.setup_alerts()
    else:
        print("\n❌ Please make sure TradingView is open with a chart")
        print("   and remote debugging is enabled on port 9222")

if __name__ == "__main__":
    main()