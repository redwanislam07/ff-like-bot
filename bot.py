import telebot
import requests
import time
from telebot import types

# ১. আপনার বটের টোকেন বসান
BOT_TOKEN = "8706590237:AAF8U6QtB4kR_YYyriEkAjasH8ji7tfOyIw"
bot = telebot.TeleBot(BOT_TOKEN)

# ২. ফ্রি ফায়ার ফেক আইডির আসল অ্যাক্সেস টোকেন লিস্ট (এখানে আসল টোকেন বসাবেন)
FAKE_TOKENS = [
    "TOKEN_1",
    "TOKEN_2"
]

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_name = message.from_user.first_name if message.from_user.first_name else "User"
    username_tag = f"@{message.from_user.username}" if message.from_user.username else "None"
    user_id = message.from_user.id
    
    # স্ক্রিনশটের মতো সাজানো মেসেজের ফরম্যাট
    panel_text = (
        f"🛒 **WELCOME TO FIRE LIKE BOT!**\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
        f"👤 **Name:** {user_name}\n"
        f"🏷️ **Username:** {username_tag}\n"
        f"✔️ **User ID:** `{user_id}`\n"
        f"💰 **Balance:** ৳100.0\n\n"
        f"🌱 **স্বাগতম! বট ব্যবহার করার জন্য ধন্যবাদ!**\n\n"
        f"🤖 FREE FIRE DAILY LIKE BOT\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
        f"🔷 Get 100+ Likes Daily\n"
        f"⚡ Auto Like Service\n"
        f"⚡ Instant Delivery\n"
        f"🛡️ 100% Trusted\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
    )
    
    # ইনলাইন বাটন (Inline Buttons) তৈরি
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_like = types.InlineKeyboardButton("🚀 GET LIKES INSTANT", callback_data="get_likes")
    markup.add(btn_like)
    
    # আপনি চাইলে এখানে আপনার বটের পিকচার লিংক বসাতে পারেন (ঐচ্ছিক)
    # bot.send_photo(message.chat.id, "IMAGE_URL_HERE", caption=panel_text, parse_mode="Markdown", reply_markup=markup)
    
    bot.send_message(message.chat.id, panel_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "get_likes")
def callback_query(call):
    msg = bot.send_message(call.message.chat.id, "📝 **Enter your Game UID:**\n*(আপনার ফ্রি ফায়ার আইডি নম্বরটি লিখুন)*", parse_mode="Markdown")
    bot.register_next_step_handler(msg, send_bulk_likes)

def send_bulk_likes(message):
    uid = message.text.strip()
    if not uid.isdigit():
        bot.send_message(message.chat.id, "❌ ভুল আইডি! শুধুমাত্র সংখ্যায় আপনার UID দিন।")
        return

    status_msg = bot.send_message(message.chat.id, "⏳ আপনার আইডি গ্যারেনা সার্ভারে প্রসেস করা হচ্ছে...")
    success_count = 0
    
    for token in FAKE_TOKENS:
        if token.startswith("TOKEN_"): # ডামি টোকেন থাকলে স্কিপ করবে
            continue
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
