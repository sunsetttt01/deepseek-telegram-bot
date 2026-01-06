import os
import time
import requests
from flask import Flask, request
from telegram import Bot

app = Flask(__name__)

# 从环境变量读取（Koyeb 会用到）
TELEGRAM_TOKEN = os.environ["6988750351:AAHiJgmS7tqRJnnrgPGsIN0mVIF-ybaXL-g"]
DEEPSEEK_API_KEY = os.environ["sk-1fe7c103afb3415ea126bad0c3b68d11"]

bot = Bot(token=TELEGRAM_TOKEN)

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# 简单限频（个人防刷）
last_call = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    message = data.get("message")
    if not message:
        return "ok"

    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip()
    if not text:
        return "ok"

    # 限频：3 秒 1 次
    now = time.time()
    if chat_id in last_call and now - last_call[chat_id] < 3:
        bot.send_message(chat_id, "慢一点，我在想 🤖")
        return "ok"
    last_call[chat_id] = now

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是我的私人助理，回答简洁、实用。"},
            {"role": "user", "content": text}
        ],
        "temperature": 0.7
    }

    try:
        resp = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        result = resp.json()
        reply = result["choices"][0]["message"]["content"]
    except Exception:
        reply = "出错了，稍后再试。"

    # Telegram 单条 4096 字限制
    for i in range(0, len(reply), 4000):
        bot.send_message(chat_id, reply[i:i+4000])

    return "ok"

@app.route("/")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
