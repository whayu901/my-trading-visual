#!/bin/bash

echo "🔍 Quick Bot Token Verifier"
echo "============================"
echo ""

read -p "Paste Bot Token: " TOKEN
echo ""

echo "Checking bot..."
RESPONSE=$(curl -s "https://api.telegram.org/bot$TOKEN/getMe")

if echo "$RESPONSE" | grep -q '"ok":true'; then
    echo "✅ TOKEN VALID!"
    echo ""
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
    echo ""
    echo "Bot Details:"
    echo "- Name: $(echo "$RESPONSE" | grep -o '"first_name":"[^"]*' | cut -d'"' -f4)"
    echo "- Username: $(echo "$RESPONSE" | grep -o '"username":"[^"]*' | cut -d'"' -f4)"
    echo ""

    read -p "Now paste Chat ID: " CHAT_ID
    echo ""
    echo "Sending test message..."

    MSG_RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
        -d "chat_id=$CHAT_ID" \
        -d "text=✅ Bot Connected! Ready for trading alerts!")

    if echo "$MSG_RESPONSE" | grep -q '"ok":true'; then
        echo "✅ MESSAGE SENT! Check Telegram!"
        echo ""
        echo "SAVE THESE:"
        echo "BOT_TOKEN=$TOKEN"
        echo "CHAT_ID=$CHAT_ID"
    else
        echo "❌ Failed to send message"
        echo "Response: $MSG_RESPONSE"
        echo ""
        echo "Make sure you:"
        echo "1. Started the bot (send /start)"
        echo "2. Chat ID is correct"
    fi
else
    echo "❌ TOKEN INVALID!"
    echo "Response: $RESPONSE"
    echo ""
    echo "Please:"
    echo "1. Create bot with @BotFather"
    echo "2. Copy token correctly (no spaces)"
fi