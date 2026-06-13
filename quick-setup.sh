#!/bin/bash

echo "🚀 TradingView Free Alert Setup"
echo "================================"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Get Telegram credentials
echo ""
echo "📱 Telegram Setup:"
echo "1. Buka Telegram, chat @BotFather"
echo "2. Buat bot baru dengan /newbot"
echo "3. Copy token yang diberikan"
echo ""
read -p "Paste Bot Token: " BOT_TOKEN

echo ""
echo "4. Chat @userinfobot di Telegram"
echo "5. Copy Chat ID yang diberikan"
echo ""
read -p "Paste Chat ID: " CHAT_ID

# Create .env file
echo "BOT_TOKEN=$BOT_TOKEN" > .env
echo "CHAT_ID=$CHAT_ID" >> .env

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📝 Next Steps:"
echo "1. Deploy ke Vercel: vercel deploy"
echo "2. Copy URL yang diberikan"
echo "3. Paste ke TradingView webhook"
echo ""
echo "Happy Trading! 💰"