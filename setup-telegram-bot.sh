#!/bin/bash

echo "🤖 TELEGRAM BOT SETUP GUIDE"
echo "============================"
echo ""

echo "📱 STEP 1: Buat Bot di Telegram"
echo "--------------------------------"
echo "1. Buka Telegram"
echo "2. Cari dan chat: @BotFather"
echo "3. Kirim: /newbot"
echo "4. Beri nama bot (contoh: My Trading Alert)"
echo "5. Beri username bot (contoh: mytradingalert_bot)"
echo "6. COPY TOKEN yang diberikan (format: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz)"
echo ""
read -p "Paste Bot Token here: " BOT_TOKEN

echo ""
echo "📱 STEP 2: Dapatkan Chat ID"
echo "---------------------------"
echo "1. Start bot Anda (click START di chat bot)"
echo "2. Cari dan chat: @userinfobot"
echo "3. Bot akan kirim Chat ID Anda"
echo "4. COPY Chat ID (format: 123456789)"
echo ""
read -p "Paste Chat ID here: " CHAT_ID

echo ""
echo "✅ STEP 3: Verifying..."
echo "------------------------"

# Test bot token
echo "Testing bot token..."
RESPONSE=$(curl -s "https://api.telegram.org/bot$BOT_TOKEN/getMe")

if echo "$RESPONSE" | grep -q '"ok":true'; then
    echo "✅ Bot token VALID!"
    BOT_NAME=$(echo "$RESPONSE" | grep -o '"first_name":"[^"]*' | cut -d'"' -f4)
    echo "Bot name: $BOT_NAME"
else
    echo "❌ Bot token INVALID!"
    echo "Response: $RESPONSE"
    echo ""
    echo "Please check:"
    echo "1. Token copied correctly (no spaces)"
    echo "2. Bot created successfully"
    exit 1
fi

echo ""
echo "📤 STEP 4: Setting Environment Variables"
echo "----------------------------------------"
echo "Choose deployment platform:"
echo "1) Vercel"
echo "2) Local (.env file)"
read -p "Choose (1 or 2): " CHOICE

if [ "$CHOICE" = "1" ]; then
    echo ""
    echo "Setting Vercel environment variables..."
    vercel env add BOT_TOKEN production <<< "$BOT_TOKEN"
    vercel env add CHAT_ID production <<< "$CHAT_ID"

    echo ""
    echo "🔄 Redeploying to Vercel..."
    vercel --prod --force

    echo ""
    echo "⏳ Waiting for deployment..."
    sleep 10

    URL="https://my-trading-visual.vercel.app"
else
    echo "BOT_TOKEN=$BOT_TOKEN" > .env
    echo "CHAT_ID=$CHAT_ID" >> .env
    echo "✅ Saved to .env file"
    URL="http://localhost:3000"
fi

echo ""
echo "🧪 STEP 5: Testing Webhook"
echo "--------------------------"
echo "Sending test message..."

WEBHOOK_RESPONSE=$(curl -s -X POST "$URL/webhook" \
    -H "Content-Type: application/json" \
    -d "{
        \"symbol\": \"TEST\",
        \"price\": \"100\",
        \"action\": \"SETUP_SUCCESS\",
        \"message\": \"Bot setup successful! Ready for trading alerts!\"
    }")

echo "Response: $WEBHOOK_RESPONSE"

if echo "$WEBHOOK_RESPONSE" | grep -q '"success":true'; then
    echo ""
    echo "🎉 SUCCESS! Check your Telegram!"
    echo ""
    echo "📊 TradingView Setup:"
    echo "Webhook URL: $URL/webhook"
else
    echo ""
    echo "⚠️ Webhook test failed"
    echo "Debugging info:"
    echo "- Bot Token: ${BOT_TOKEN:0:10}..."
    echo "- Chat ID: $CHAT_ID"
    echo "- URL: $URL/webhook"
fi

echo ""
echo "📝 Your Credentials (SAVE THIS!):"
echo "================================="
echo "BOT_TOKEN=$BOT_TOKEN"
echo "CHAT_ID=$CHAT_ID"
echo "WEBHOOK_URL=$URL/webhook"
echo "================================="