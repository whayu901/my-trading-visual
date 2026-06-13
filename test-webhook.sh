#!/bin/bash

echo "🧪 Testing Webhook Server"
echo "========================="
echo ""

# Default URL
URL="https://my-trading-visual.vercel.app"

# Check if custom URL provided
if [ "$1" ]; then
    URL="$1"
fi

echo "📍 Testing URL: $URL"
echo ""

# Test 1: Health Check
echo "1️⃣ Health Check (GET /)..."
curl -s "$URL" | python3 -m json.tool
echo ""

# Test 2: Webhook Endpoint
echo "2️⃣ Testing Webhook (POST /webhook)..."
response=$(curl -s -X POST "$URL/webhook" \
    -H "Content-Type: application/json" \
    -d '{
        "symbol": "XAUUSD",
        "price": "2000.50",
        "action": "BUY",
        "message": "Test alert from script!"
    }')

echo "$response" | python3 -m json.tool
echo ""

# Check response
if echo "$response" | grep -q "success.*true"; then
    echo "✅ Webhook test SUCCESSFUL!"
    echo "📱 Check your Telegram for notification!"
else
    echo "❌ Webhook test FAILED!"
    echo ""
    echo "Possible issues:"
    echo "1. Environment variables not set (BOT_TOKEN, CHAT_ID)"
    echo "2. Wrong bot token or chat ID"
    echo "3. Server not deployed properly"
    echo ""
    echo "Fix dengan:"
    echo "- Set env variables di Vercel dashboard"
    echo "- Redeploy: vercel --prod"
fi