import telebot
from datetime import datetime, timedelta
import pytz
from flask import Flask
import threading
import os

API_TOKEN = '7098418043:AAGU6F4iL7iX82y8uXj0F4Uf_Uv6G5v_hS8'
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is Live"

def get_status():
    tz = pytz.timezone('Asia/Riyadh')
    now = datetime.now(tz)
    target = now.replace(hour=9, minute=0, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    diff = target - now
    h, rem = divmod(diff.seconds, 3600)
    m, _ = divmod(rem, 60)
    return h, m

@bot.message_handler(func=lambda m: m.text in ["نزار", "مكان نزار", "موقع نزار"])
def send_info(message):
    try:
        h, m = get_status()
        img = "https://jeanropke.github.io/RDR2CollectorsMap/assets/images/nazar_location.png"
        
        text = (
            "📍 *موقع نزار الحالي*\n\n"
            f"⏳ *الوقت المتبقي:* {h} ساعة و {m} دقيقة\n"
            "🕒 يتغير الموقع 9:00 AM بتوقيت السعودية"
        )
        bot.send_photo(message.chat.id, img, caption=text, parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ الخريطة تتحدث حالياً، جرب كمان شوي.")

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    threading.Thread(target=run).start()
    bot.polling(none_stop=True)
