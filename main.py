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
    return "Nazar Bot is Online"

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

@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    text_in = message.text
    if any(word in text_in for word in ["نزار", "مكان", "موقع"]):
        try:
            h, m = get_status()
            img_url = "https://jeanropke.github.io/RDR2CollectorsMap/assets/images/nazar_location.png"
            caption_text = f"📍 *موقع نزار الحالي*\n\n⏳ *الوقت المتبقي:* {h} ساعة و {m} دقيقة\n🕒 التغيير 9:00 AM بتوقيت السعودية"
            bot.send_photo(message.chat.id, img_url, caption=caption_text, parse_mode="Markdown")
        except:
            bot.reply_to(message, "⚠️ الخريطة تتحدث من المصدر، جرب بعد دقيقة.")

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    threading.Thread(target=run).start()
    bot.polling(none_stop=True)
