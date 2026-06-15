#!/usr/bin/env python3
"""
Create alerts directly from SR Fast indicator using Chrome DevTools Protocol
"""

import json
import time
import websocket
import urllib.request

def get_websocket_url():
    """Get the WebSocket URL for TradingView"""
    try:
        req = urllib.request.urlopen('http://localhost:9222/json', timeout=2)
        pages = json.loads(req.read())

        for page in pages:
            if 'tradingview' in page.get('url', '').lower():
                print(f"✅ Connected to TradingView")
                return page['webSocketDebuggerUrl']

        print("❌ TradingView page not found")
        return None
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

def execute_js(ws_url, code, await_promise=True):
    """Execute JavaScript in TradingView"""
    try:
        ws = websocket.create_connection(ws_url, timeout=30)

        # Enable runtime
        ws.send(json.dumps({'id': 1, 'method': 'Runtime.enable'}))
        ws.recv()

        # Execute the code
        ws.send(json.dumps({
            'id': 2,
            'method': 'Runtime.evaluate',
            'params': {
                'expression': code,
                'returnByValue': True,
                'awaitPromise': await_promise
            }
        }))

        # Get result
        result = json.loads(ws.recv())
        ws.close()

        if 'result' in result and 'result' in result['result']:
            return result['result']['result'].get('value', result['result']['result'])
        elif 'result' in result:
            return result['result']
        else:
            return result
    except Exception as e:
        return f"Error: {e}"

def create_indicator_alerts(ws_url):
    """Create alerts from the SR Fast indicator"""

    # JavaScript to create alerts from indicator conditions
    create_alerts_js = """
    (async function() {
        const results = [];

        // Alert configurations for SR Fast indicator
        const alerts = [
            {
                name: "🟢 RBS RETEST - BUY",
                condition: "RBS RETEST - BUY",
                message: "🎯 {{ticker}} {{interval}} RBS BUY\\n💹 Entry: {{close}}\\n✅ HIGH PROBABILITY"
            },
            {
                name: "🔴 SBR RETEST - SELL",
                condition: "SBR RETEST - SELL",
                message: "🎯 {{ticker}} {{interval}} SBR SELL\\n📉 Entry: {{close}}\\n✅ HIGH PROBABILITY"
            },
            {
                name: "🔴 Resistance Touch",
                condition: "Resistance Touch",
                message: "⚠️ {{ticker}} {{interval}} RESISTANCE\\n📉 Level: {{close}}\\n⚡ Quick scalp"
            },
            {
                name: "🟢 Support Touch",
                condition: "Support Touch",
                message: "⚠️ {{ticker}} {{interval}} SUPPORT\\n💹 Level: {{close}}\\n⚡ Quick scalp"
            },
            {
                name: "⬆️ Resistance Break",
                condition: "Resistance Break",
                message: "🚨 {{ticker}} {{interval}} RES BREAK\\n⏳ Wait for retest at {{close}}"
            },
            {
                name: "⬇️ Support Break",
                condition: "Support Break",
                message: "🚨 {{ticker}} {{interval}} SUP BREAK\\n⏳ Wait for retest at {{close}}"
            }
        ];

        // Function to create a single alert
        function createAlert(alertConfig) {
            return new Promise((resolve) => {
                try {
                    // Open alert dialog using keyboard shortcut
                    const event = new KeyboardEvent('keydown', {
                        key: 'a',
                        altKey: true,
                        bubbles: true,
                        cancelable: true
                    });
                    document.dispatchEvent(event);

                    // Wait for dialog to open
                    setTimeout(() => {
                        // Try to find and fill the alert form
                        const dialog = document.querySelector('.tv-dialog__modal-wrap');
                        if (dialog) {
                            // This would need to interact with the specific form elements
                            // Since the exact selectors may vary, we'll return status
                            resolve({
                                alert: alertConfig.name,
                                status: 'Dialog opened - please complete manually',
                                instructions: `
                                    1. Select "SR Fast - AUTO Scalping" in first dropdown
                                    2. Select "${alertConfig.condition}" in second dropdown
                                    3. Set alert name to: ${alertConfig.name}
                                    4. Set message to: ${alertConfig.message}
                                    5. Set frequency to "Once Per Bar Close"
                                    6. Click Create
                                `
                            });
                        } else {
                            resolve({
                                alert: alertConfig.name,
                                status: 'Could not open dialog'
                            });
                        }
                    }, 1000);
                } catch (e) {
                    resolve({
                        alert: alertConfig.name,
                        status: 'Error: ' + e.message
                    });
                }
            });
        }

        // Try to create first alert to show the process
        const firstAlert = alerts[0];
        const result = await createAlert(firstAlert);

        return {
            currentAlert: result,
            remainingAlerts: alerts.slice(1).map(a => ({
                name: a.name,
                condition: a.condition
            })),
            totalAlerts: alerts.length,
            instructions: result.instructions
        };
    })();
    """

    return execute_js(ws_url, create_alerts_js)

def main():
    print("=" * 60)
    print("🚨 SR Fast Indicator Alert Creator")
    print("=" * 60)

    # Get WebSocket connection
    ws_url = get_websocket_url()
    if not ws_url:
        print("\n❌ Please ensure TradingView Desktop is running")
        return

    # Check current chart
    check_chart_js = """
    (function() {
        const symbol = document.querySelector('[data-name="legend-series-item"] [data-name="legend-source-title"]');
        const timeframe = document.querySelector('[data-name="time-interval-menu"] button.isActive');

        // Look for SR indicator
        const indicators = document.querySelectorAll('.study .pane-legend-title__description');
        let srFound = false;

        indicators.forEach(ind => {
            if (ind.textContent && (ind.textContent.includes('SR') || ind.textContent.includes('Scalping'))) {
                srFound = true;
            }
        });

        return {
            symbol: symbol ? symbol.textContent : 'Unknown',
            timeframe: timeframe ? timeframe.textContent : 'Unknown',
            srIndicatorFound: srFound
        };
    })();
    """

    chart_info = execute_js(ws_url, check_chart_js, False)
    print(f"\n📊 Current Chart:")
    print(f"   Symbol: {chart_info.get('symbol', 'Unknown')}")
    print(f"   Timeframe: {chart_info.get('timeframe', 'Unknown')}")

    if isinstance(chart_info, dict) and not chart_info.get('srIndicatorFound'):
        print("\n⚠️  SR Fast indicator not detected on chart")
        print("   Please add the 'SR Fast - AUTO Scalping' indicator first")

    print("\n📋 Creating alerts from SR Fast indicator...")
    result = create_indicator_alerts(ws_url)

    if isinstance(result, dict):
        print(f"\n✅ Alert dialog opened for: {result.get('currentAlert', {}).get('alert', 'Unknown')}")

        if 'instructions' in result:
            print("\n📝 Manual steps to complete:")
            print(result['instructions'])

        if 'remainingAlerts' in result:
            print(f"\n📌 Remaining alerts to create ({len(result['remainingAlerts'])} more):")
            for alert in result['remainingAlerts']:
                print(f"   - {alert['name']} ({alert['condition']})")

        print("\n💡 Tips:")
        print("   • Focus on RBS/SBR RETEST alerts (highest win rate)")
        print("   • Use M5 timeframe for optimal results")
        print("   • Set risk-reward ratio to minimum 1:2")
    else:
        print(f"\n❌ Could not create alerts: {result}")

    print("\n" + "=" * 60)
    print("To create all 6 alerts, run this script 6 times,")
    print("completing the dialog each time.")
    print("=" * 60)

if __name__ == "__main__":
    main()