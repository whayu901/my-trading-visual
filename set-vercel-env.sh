#!/bin/bash

echo "🔧 Setting Vercel Environment Variables"
echo "========================================"
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not installed"
    echo "Install dengan: npm i -g vercel"
    exit 1
fi

echo "📝 Setting environment variables..."

# Set BOT_TOKEN
read -p "Enter Telegram Bot Token: " BOT_TOKEN
vercel env add BOT_TOKEN production <<< "$BOT_TOKEN"

# Set CHAT_ID
read -p "Enter Telegram Chat ID: " CHAT_ID
vercel env add CHAT_ID production <<< "$CHAT_ID"

echo ""
echo "✅ Environment variables set!"
echo ""
echo "🔄 Redeploying dengan env baru..."
vercel --prod

echo ""
echo "🎉 DONE! Test dengan:"
echo "curl -X POST https://my-trading-visual.vercel.app/webhook \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"symbol\":\"XAUUSD\",\"price\":\"2000\",\"action\":\"BUY\",\"message\":\"Test!\"}'"