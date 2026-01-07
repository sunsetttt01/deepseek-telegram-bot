import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TELEGRAM_BOT_TOKEN = os.getenv("6988750351:AAHiJgmS7tqRJnnrgPGsIN0mVIF-ybaXL-g")
DEEPSEEK_API_KEY = os.getenv("sk-1fe7c103afb3415ea126bad0c3b68d11")

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    headers = {
        "Authorization": f"Bearer {sk-1fe7c103afb3415ea126bad0c3b68d11}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": user_text}
        ]
    }

    resp = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=30)
    result = resp.json()

    answer = result["choices"][0]["message"]["content"]
    await update.message.reply_text(answer)

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("Bot is running...")
app.run_polling()
