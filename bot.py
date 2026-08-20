import telebot
import requests
import time
from telebot import types

# ১. এখানে BotFather থেকে পাওয়া আপনার বটের API Token-টি বসান
BOT_TOKEN = "8706590237:AAF8U6QtB4kR_YYyriEkAjasH8ji7tfOyIw"
bot = telebot.TeleBot(BOT_TOKEN)

# ২. আপনার ফেক আইডির অ্যাক্সেস টোকেন লিস্ট (এখানে ১০০ বা ২০০ পর্যন্ত বসাতে পারবেন)
FAKE_TOKENS = [
    "TOKEN_1",
    "TOKEN_2",
    "TOKEN_3"
]

@bot.message_handler(commands=['start'])
def start_cmd(message):
    welcome_text = "🔥 **WELCOME TO FREE FIRE LIKE BOT!** 🔥\n\n👇 লাইক নিতে নিচের বাটনে চাপ দিন।"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("🚀 GET 10 LIKES INSTANT"))
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🚀 GET 10 LIKES INSTANT")
def ask_uid(message):
    msg = bot.send_message(message.chat.id, "📝 **Enter your Game UID:**\n*(আপনার ফ্রি ফায়ার আইডি নম্বরটি লিখুন)*", parse_mode="Markdown")
    bot.register_next_step_handler(msg, send_bulk_likes)

def send_bulk_likes(message):
    uid = message.text.strip()
    if not uid.isdigit():
        bot.send_message(message.chat.id, "❌ ভুল আইডি! শুধুমাত্র সংখ্যায় আপনার UID দিন।")
        return

    status_msg = bot.send_message(message.chat.id, "⏳ আপনার আইডি প্রসেস করা হচ্ছে...")
    success_count = 0
    
    for token in FAKE_TOKENS:
        if success_count >= 10: # প্রতি ক্লিকে ১০টি করে লাইক পাঠানোর লিমিট
            break
        api_url = f"https://freefiremobile.com" 
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {"target_uid": int(uid), "region": "BD"}
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=5)
            if response.status_code == 200:
                success_count += 1
        except Exception:
            pass
        time.sleep(0.5)
    
    bot.edit_message_text(chat_id=message.chat.id, message_id=status_msg.message_id, text=f"✅ **SUCCESS!**\n\n🎯 আপনার আইডি `{uid}`-তে সফলভাবে **{success_count}টি লাইক** পাঠানো হয়েছে!", parse_mode="Markdown")

bot.infinity_polling()

