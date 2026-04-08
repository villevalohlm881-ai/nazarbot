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
    return "Nazar Bot is Running"

def get_nazar_status():
    saudi_tz = pytz.timezone('Asia/Riyadh')
    now = datetime.now(saudi_tz)
    target = now.replace(hour=9, minute=0, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    diff = target - now
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return hours, minutes

@bot.message_handler(func=lambda m: m.text in ["نزار", "مكان نزار", "موقع نزار"])
def send_nazar_info(message):
    try:
        hours, minutes = get_nazar_status()
        map_url = "https://jeanropke.github.io/RDR2CollectorsMap/assets/images/nazar_location.png"
        
        caption = (
            "📍 *موقع السيدة نزار الحالي:*\n"
            "_(تحديث تلقائي من الخريطة العالمية)_\n\n"
            f"⏳ *الوقت المتبقي لتغيير المكان:*\n"
            f"*{hours}* ساعة و *{minutes}* دقيقة\n\n"
            "🕒 يتغير الموقع يومياً الساعة *9:00 AM* بتوقيت السعودية."
        )
        bot.send_photo(message.chat.id, map_url, caption=caption, parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, "⚠️ الخريطة قيد التحديث من المصدر، حاول مجدداً لاحقاً.")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    threading.Thread(target=run_server).start()
    bot.polling(none_stop=True)
