import os
import telebot
import requests
from flask import Flask
from threading import Thread

TELEGRAM_TOKEN = "8295287160:AAE9rfnel80CPLKMKK3fhQe0hd3NxIV3T4U"
bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Nazar is Online!"

def run():
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080))

@bot.message_handler(func=lambda message: True)
def get_nazar(message):
    if "نزار" in message.text or "مكان" in message.text:
        try:
            data = requests.get("https://rdonazar.com/api/v1/location").json()
            loc_name = data['location']['name']
            img_url = data['location']['image']
            bot.send_photo(message.chat.id, img_url, caption=f"📍 نزار اليوم في: {loc_name}")
        except:
            bot.reply_to(message, "السيرفر معلق شوي، جربي بعد دقيقة!")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.polling(none_stop=True)
