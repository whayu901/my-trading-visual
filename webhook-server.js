// WEBHOOK SERVER untuk TradingView Alert → Telegram
// Bisa di-host GRATIS di Vercel/Railway/Render

const express = require('express');
const axios = require('axios');
const app = express();
app.use(express.json());

// CONFIG - Menggunakan environment variables untuk keamanan
require('dotenv').config();
const TELEGRAM_BOT_TOKEN = process.env.BOT_TOKEN || 'YOUR_BOT_TOKEN';
const TELEGRAM_CHAT_ID = process.env.CHAT_ID || 'YOUR_CHAT_ID';

// Endpoint untuk terima webhook dari TradingView
app.post('/webhook', async (req, res) => {
    try {
        const { symbol, price, action, message } = req.body;

        // Format pesan untuk Telegram
        let alertMessage = `🚨 *TRADING ALERT* 🚨\n\n`;
        alertMessage += `📊 Symbol: *${symbol}*\n`;
        alertMessage += `💰 Price: *${price}*\n`;
        alertMessage += `🎯 Action: *${action}*\n`;
        alertMessage += `📝 Signal: ${message}\n`;
        alertMessage += `⏰ Time: ${new Date().toLocaleString('id-ID', {timeZone: 'Asia/Jakarta'})}`;

        // Tambah emoji berdasarkan action
        if (action.includes('BUY')) {
            alertMessage = '🟢 ' + alertMessage;
        } else if (action.includes('SELL')) {
            alertMessage = '🔴 ' + alertMessage;
        }

        // Kirim ke Telegram
        await axios.post(
            `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`,
            {
                chat_id: TELEGRAM_CHAT_ID,
                text: alertMessage,
                parse_mode: 'Markdown'
            }
        );

        res.json({ success: true, message: 'Alert sent to Telegram!' });
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ success: false, error: error.message });
    }
});

// Health check endpoint
app.get('/', (req, res) => {
    res.json({
        status: 'running',
        message: 'Webhook server is running! 🚀',
        endpoints: {
            webhook: '/webhook (POST)',
            health: '/ (GET)'
        },
        usage: 'POST to /webhook with JSON: {symbol, price, action, message}'
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});