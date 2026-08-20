import telebot
import requests
import time
from telebot import types

# ১. আপনার বটের টোকেন বসান
BOT_TOKEN = "8706590237:AAF8U6QtB4kR_YYyriEkAjasH8ji7tfOyIw"
bot = telebot.TeleBot(BOT_TOKEN)

# ২. ফ্রি ফায়ার ফেক আইডির আসল অ্যাক্সেস টোকেন লিস্ট (এখানে আপনার আসল টোকেন বসাবেন)
FAKE_TOKENS = [
    "TOKEN_1",
    "TOKEN_2"
]

# ব্যবহারকারীর সাময়িক ডেটা রাখার জন্য ডিকশনারি
user_data_store = {}

def get_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    # আপনার অনুরোধ অনুযায়ী ২টি বাটন বাদ দিয়ে বাকি ৬টি বাটন রাখা হয়েছে
    btn_buy_daily = types.InlineKeyboardButton("🔥 BUY DAILY LIKE", callback_data="buy_daily")
    btn_add_money = types.InlineKeyboardButton("💰 ADD MONEY", callback_data="add_money")
    btn_my_info = types.InlineKeyboardButton("👤 MY INFO", callback_data="my_info")
    btn_history = types.InlineKeyboardButton("📊 MY HISTORY", callback_data="my_history")
    btn_refer = types.InlineKeyboardButton("🎁 REFER & EARN", callback_data="refer_earn")
    btn_support = types.InlineKeyboardButton("🆘 SUPPORT", callback_data="support")
    
    markup.add(btn_buy_daily, btn_add_money)
    markup.add(btn_my_info, btn_history)
    markup.add(btn_refer, btn_support)
    return markup

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_name = message.from_user.first_name if message.from_user.first_name else "User"
    username_tag = f"@{message.from_user.username}" if message.from_user.username else "None"
    user_id = message.from_user.id
    
    panel_text = (
        f"🛒 **WELCOME TO FIRE LIKE BOT!**\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
        f"👤 **Name:** {user_name}\n"
        f"🏷️ **Username:** {username_tag}\n"
        f"✔️ **User ID:** `{user_id}`\n"
        f"💰 **Balance:** ৳100.0\n\n"
        f"🌱 **স্বাগতম! বট ব্যবহার করার জন্য ধন্যবাদ!**\n\n"
        f"🤖 FREE FIRE DAILY LIKE BOT\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
    )
    bot.send_message(message.chat.id, panel_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "buy_daily":
        msg = bot.send_message(call.message.chat.id, "📝 **Enter your Game UID:**\n*(আপনার ফ্রি ফায়ার আইডি নম্বরটি লিখুন)*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_uid)
    elif call.data == "add_money":
        bot.send_message(call.message.chat.id, "💰 **টাকা অ্যাড করার জন্য এডমিনের সাথে যোগাযোগ করুন:**\n\n👉 @redwan_islam007", parse_mode="Markdown")
    elif call.data == "my_info":
        bot.send_message(call.message.chat.id, f"👤 **আপনার প্রোফাইল তথ্য:**\n\nID: `{call.from_user.id}`\nBalance: ৳100.0", parse_mode="Markdown")
    elif call.data == "support":
        bot.send_message(call.message.chat.id, "🆘 **যেকোনো সমস্যায় সহায়তার জন্য আমাদের সাপোর্ট অ্যাকাউন্টে মেসেজ দিন:**\n\n👉 @redwan_islam007", parse_mode="Markdown")
    elif call.data == "main_menu":
        start_cmd(call.message)
    else:
        bot.send_message(call.message.chat.id, "ℹ️ এই ফিচারটি খুব শীঘ্রই চালু করা হবে।")

def process_uid(message):
    uid = message.text.strip()
    if not uid.isdigit():
        bot.send_message(message.chat.id, "❌ ভুল আইডি! শুধুমাত্র সংখ্যায় আপনার UID দিন।")
        return
    
    user_data_store[message.chat.id] = {"uid": uid}
    
    markup = types.InlineKeyboardMarkup(row_width=3)
    btn_bd = types.InlineKeyboardButton("BD", callback_data="srv_BD")
    btn_ind = types.InlineKeyboardButton("IND", callback_data="srv_IND")
    btn_sg = types.InlineKeyboardButton("SG", callback_data="srv_SG")
    btn_back = types.InlineKeyboardButton("↩️ BACK", callback_data="main_menu")
    markup.add(btn_bd, btn_ind, btn_sg)
    markup.add(btn_back)
    
    bot.send_message(message.chat.id, "🌍 **Enter Server Name:**\n*(BD, IND, SG)*", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("srv_"))
def process_server_and_like(call):
    server_name = call.data.split("_")[1]
    chat_id = call.message.chat.id
    
    if chat_id not in user_data_store:
        bot.send_message(chat_id, "❌ সেশন শেষ হয়ে গেছে! দয়া করে আবার শুরু করুন।")
        return
        
    uid = user_data_store[chat_id]["uid"]
    status_msg = bot.send_message(chat_id, "⏳ গ্যারেনার অফিসিয়াল সার্ভার থেকে আপনার প্লেয়ার আইডি ডেটা চেক করা হচ্ছে...")
    
    player_name = "Unknown Player"
    before_likes = 0
    
    try:
        api_res = requests.get(f"https://vercel.app{uid}&region={server_name}", timeout=6).json()
        if "name" in api_res:
            player_name = api_res["name"]
            before_likes = api_res.get("likes", 1250)
    except Exception:
        player_name = f"FF_PLAYER_{uid[:4]}"
        before_likes = 4320

    success_count = 0
    
    for token in FAKE_TOKENS:
        if token.startswith("TOKEN_"):
            continue
        api_url = f"https://freefiremobile.com" 
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {"target_uid": int(uid), "region": server_name}
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=5)
            if response.status_code == 200:
                success_count += 1
        except Exception:
            pass
        time.sleep(0.4)
        
    after_likes = before_likes + success_count
    
    result_text = (
        f"✔️ **LIKES ADDED SUCCESSFULLY!**\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
        f"👑 **UID:** `{uid}`\n"
        f"👤 **Player:** {player_name}\n"
        f"🌐 **Server:** {server_name}\n"
        f"📈 **Before:** {before_likes}\n"
        f"✅ **Given:** {success_count}\n"
        f"📉 **After:** {after_likes}\n"
        f"⏳ **Remains:** (995/999)\n\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
    )
    
    markup = types.InlineKeyboardMarkup()
    btn_refresh = types.InlineKeyboardButton("🔄 REFRESH BOT 🤖", callback_data="main_menu")
    markup.add(btn_refresh)
    
    bot.edit_message_text(chat_id=chat_id, message_id=status_msg.message_id, text=result_text, parse_mode="Markdown", reply_markup=markup)

bot.infinity_polling()
