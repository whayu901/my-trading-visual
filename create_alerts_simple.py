#!/usr/bin/env python3
"""
Simple TradingView Alert Creation Script
Creates alerts for SR Fast indicator using direct CDP connection
"""

import json
import time
import websocket
import urllib.request

def get_ws_url():
    """Get WebSocket URL for TradingView"""
    try:
        # Try different ports if 9222 doesn't work
        for port in [9222, 9223, 9224]:
            try:
                req = urllib.request.urlopen(f'http://localhost:{port}/json', timeout=2)
                pages = json.loads(req.read())

                for page in pages:
                    if 'tradingview' in page.get('url', '').lower():
                        print(f"✅ Found TradingView on port {port}")
                        return page['webSocketDebuggerUrl']
            except:
                continue

        print("❌ Could not find TradingView. Make sure it's running with debug port.")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def execute_js(ws_url, code):
    """Execute JavaScript code in TradingView"""
    try:
        ws = websocket.create_connection(ws_url, timeout=10)

        # Enable runtime
        ws.send(json.dumps({
            'id': 1,
            'method': 'Runtime.enable'
        }))
        ws.recv()

        # Execute the code
        ws.send(json.dumps({
            'id': 2,
            'method': 'Runtime.evaluate',
            'params': {
                'expression': code,
                'returnByValue': True,
                'awaitPromise': True
            }
        }))

        result = json.loads(ws.recv())
        ws.close()

        if 'result' in result and 'result' in result['result']:
            return result['result']['result'].get('value', 'No value returned')
        elif 'result' in result and 'exceptionDetails' in result['result']:
            return f"Error: {result['result']['exceptionDetails']['text']}"
        else:
            return str(result)

    except Exception as e:
        return f"Execution error: {e}"

def main():
    print("🚨 TradingView Alert Creation Tool")
    print("=" * 50)

    # Get WebSocket URL
    ws_url = get_ws_url()
    if not ws_url:
        print("\n⚠️  Please start TradingView with debug port:")
        print("   Mac/Linux: /Applications/TradingView.app/Contents/MacOS/TradingView --remote-debugging-port=9222")
        print("   Windows: TradingView.exe --remote-debugging-port=9222")
        return

    print("\n📊 Checking current chart...")

    # Check current symbol and timeframe
    check_chart = """
    (function() {
        const symbol = document.querySelector('[data-name="legend-series-item"] [data-name="legend-source-title"]');
        const tf = document.querySelector('[data-name="time-interval-menu"] button.isActive');

        return {
            symbol: symbol ? symbol.textContent : 'Unknown',
            timeframe: tf ? tf.textContent : 'Unknown'
        };
    })();
    """

    chart_info = execute_js(ws_url, check_chart)
    print(f"   Chart: {chart_info}")

    print("\n🎯 Alert configurations for SR Fast indicator:")
    print("   1. 🟢 RBS RETEST - BUY (HIGH priority)")
    print("   2. 🔴 SBR RETEST - SELL (HIGH priority)")
    print("   3. 🔴 Resistance Touch (MEDIUM priority)")
    print("   4. 🟢 Support Touch (MEDIUM priority)")
    print("   5. ⬆️ Resistance Break (LOW priority)")
    print("   6. ⬇️ Support Break (LOW priority)")

    print("\n💡 Instructions to create alerts manually:")
    print("\n1. Click the Alert button (Alt+A) or clock icon in toolbar")
    print("2. In the first dropdown, select 'SR Fast - AUTO Scalping'")
    print("3. In the second dropdown, select one of the conditions above")
    print("4. Set 'Alert name' to match the condition")
    print("5. Set 'Frequency' to 'Once Per Bar Close'")
    print("6. Add a message template like:")
    print("   🎯 {{ticker}} {{interval}}")
    print("   💹 Price: {{close}}")
    print("   Signal: [condition name]")
    print("7. Click 'Create'")
    print("8. Repeat for all 6 conditions")

    print("\n📋 Recommended alert messages:")
    print("\nRBS RETEST - BUY:")
    print("🎯 {{ticker}} {{interval}} RBS BUY\\n💹 Entry: {{close}}\\n✅ HIGH PROBABILITY")

    print("\nSBR RETEST - SELL:")
    print("🎯 {{ticker}} {{interval}} SBR SELL\\n📉 Entry: {{close}}\\n✅ HIGH PROBABILITY")

    print("\nResistance Touch:")
    print("⚠️ {{ticker}} {{interval}} RESISTANCE\\n📉 Level: {{close}}\\n⚡ Quick scalp")

    print("\nSupport Touch:")
    print("⚠️ {{ticker}} {{interval}} SUPPORT\\n💹 Level: {{close}}\\n⚡ Quick scalp")

    print("\nResistance Break:")
    print("🚨 {{ticker}} {{interval}} RES BREAK\\n⏳ Wait for retest at {{close}}")

    print("\nSupport Break:")
    print("🚨 {{ticker}} {{interval}} SUP BREAK\\n⏳ Wait for retest at {{close}}")

    # Try automated approach
    print("\n" + "=" * 50)
    print("🤖 Attempting automated alert creation...")

    # Try to open alert dialog
    open_alert = """
    (function() {
        // Try keyboard shortcut first
        document.dispatchEvent(new KeyboardEvent('keydown', {
            key: 'a',
            altKey: true,
            bubbles: true
        }));

        return 'Alert dialog triggered via Alt+A';
    })();
    """

    result = execute_js(ws_url, open_alert)
    print(f"   {result}")

    print("\n✅ If the alert dialog opened, follow the manual instructions above.")
    print("   If not, use the Alert button in the toolbar or press Alt+A.")

if __name__ == "__main__":
    main()