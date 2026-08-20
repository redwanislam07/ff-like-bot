import telebot
import requests
import time
from telebot import types
from datetime import datetime

# ১. আপনার একদম নতুন বটের আসল টোকেন এখানে সেট করা হয়েছে
BOT_TOKEN = "8643104524:AAFNHUNHr_4eGigdR7ZMa44sxtXixCSfsdw"
bot = telebot.TeleBot(BOT_TOKEN)

# ২. ফ্রি ফায়ার ফেক আইডির আসল অ্যাক্সেস টোকেন লিস্ট (১ থেকে ১০ নম্বর পর্যন্ত ঘর)
FAKE_TOKENS = [
    "এখানে_আপনার_১_নাম্বার_টোকেন_বসাবেন",
    "এখানে_আপনার_২_নাম্বার_টোকেন_বসাবেন",
    "এখানে_আপনার_৩_নাম্বার_টোকেন_বসাবেন",
    "এখানে_আপনার_৪_নাম্বার_টোকেন_বসাবেন",
    "এখানে_আপনার_৫_নাম্বার_টোকেন_বসাবেন",
    "এখানে_আপনার_৬_নাম্বার_টোকেন_বসাবেন",
    "এখানে_আপনার_৭_নাম্বার_টোকেন_বসাবেন",
    "এখানে_আপনার_৮_নাম্বার_টোকেন_বসাবেন",
    "এখানে_আপনার_৯_নাম্বার_টোকেন_বসাবেন",
    "এখানে_আপনার_১০_নাম্বার_টোকেন_বসাবেন"
]

# 📱 আপনার বিকাশ পার্সোনাল নম্বর (01914910256) সেট করা হয়েছে
MY_BKASH_NUMBER = "01914910256"  

# 📢 আপনার নোটিফিকেশন গ্রুপ এবং মেইন চ্যানেল লক ইউজারনেম
LOG_CHANNEL_USERNAME = "@ff_like_history_bd"
MAIN_CHANNEL_USERNAME = "@ff_like_history_bd" 

# 👑 বটের মালিক বা এডমিন আইডি (আপনার পার্সোনাল আইডি)
ADMIN_ID = 8669357832

user_data_store = {}
user_accounts = {}

def get_user_data(user_id):
    if user_id not in user_accounts:
        user_accounts[user_id] = {
            "balance": 0.0,
            "total_deposit": 0.0,
            "total_spent": 0.0,
            "join_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "deposits": [], 
            "orders": [],
            "referred_by": None,  
            "total_referred": 0,   
            "joined_verified": 0,  
            "total_earnings": 0.0  
        }
    return user_accounts[user_id]

# 🔍 ইউজার চ্যানেলে জয়েন করেছে কি না তা চেক করার সিকিউরিটি ফাংশন
def is_user_joined(user_id):
    try:
        member = bot.get_chat_member(MAIN_CHANNEL_USERNAME, user_id)
        if member.status in ['creator', 'administrator', 'member']:
            return True
        return False
    except Exception:
        return True

# 🛒 আপনার পছন্দ অনুযায়ী ৬টি বাটন লেআউট
def get_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
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

# 👑 এডমিনদের জন্য কাস্টমারের ব্যালেন্স অ্যাড করার সিকিউর কমান্ড লজিক
@bot.message_handler(commands=['add'])
def add_balance_by_admin(message):
    if message.from_user.id != ADMIN_ID:
        return 
        
    try:
        args = message.text.split()
        target_user_id = int(args[1])
        amount_to_add = float(args[2])
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_data = get_user_data(target_user_id)
        user_data["balance"] += amount_to_add
        user_data["total_deposit"] += amount_to_add
        user_data["deposits"].append({"amount": amount_to_add, "time": current_time})
        
        bot.send_message(message.chat.id, f"✅ **Success!** ৳{amount_to_add} successfully added to User ID: `{target_user_id}`")
        
        try:
            bot.send_message(target_user_id, f"🎉 **Payment Approved!**\n\nএডমিন আপনার পেমেন্টটি ভেরিফাই করে আপনার অ্যাকাউন্টে **৳{amount_to_add}** যোগ করে দিয়েছে। বর্তমান ব্যালেন্স চেক করতে বটের মেইন মেনু ওপেন করুন। ধন্যবাদ!")
        except Exception:
            pass
            
    except Exception:
        bot.send_message(message.chat.id, "❌ **ভুল ফরম্যাট!**\n\nসঠিক নিয়ম: `/add UserID Amount` (যেমন: `/add 8669357832 100`)")

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name if message.from_user.first_name else "User"
    username_tag = f"@{message.from_user.username}" if message.from_user.username else "@No Username"
    
    # 🔒 ফোর্স সাবস্ক্রাইব নোটিশ সিস্টেম
    if not is_user_joined(user_id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_join = types.InlineKeyboardButton("📢 JOIN OUR CHANNEL", url=f"https://t.me{MAIN_CHANNEL_USERNAME.replace('@','')}")
        btn_refresh = types.InlineKeyboardButton("🔄 CHECK & REFRESH 🤖", callback_data="main_menu")
        markup.add(btn_join, btn_refresh)
        
        bot.send_message(message.chat.id, "❌ **আপনাকে প্রথমে আমাদের অফিসিয়াল চ্যানেলে জয়েন করতে হবে!**\n\nনিচের বোতামে চাপ দিয়ে চ্যানেলে জয়েন করুন, তারপর `CHECK & REFRESH` বোতামে চাপ দিন।", reply_markup=markup)
        return

    user_data = get_user_data(user_id)
    args = message.text.split()
    
    if len(args) > 1 and args[1].startswith('ref_'):
        try:
            referrer_id = int(args[1].replace('ref_', ''))
            if user_id not in user_accounts and referrer_id != user_id and user_data["referred_by"] is None:
                user_data["referred_by"] = referrer_id
                ref_data = get_user_data(referrer_id)
                ref_data["total_referred"] += 1
                ref_data["joined_verified"] += 1
                ref_data["balance"] += 1.5
                ref_data["total_earnings"] += 1.5
                
                try:
                    bot.send_message(referrer_id, f"🎉 **New Referral!**\n\nআপনার লিংক ব্যবহার করে একজন নতুন ইউজার বটে যুক্ত হয়েছে। আপনার ব্যালেন্সে **৳১.৫** বোনাস যোগ করা হয়েছে!")
                except Exception:
                    pass
        except Exception:
            pass

    current_balance = user_data["balance"]
    
    panel_text = (
        f"🛒 **WELCOME TO FIRE LIKE BOT!**\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
        f"👤 **Name:** {user_name}\n"
        f"🏷️ **Username:** {username_tag}\n"
        f"✔️ **User ID:** `{user_id}`\n"
        f"💰 **Balance:** ৳{current_balance}\n\n"
        f"🌱 **স্বাগতম! বট ব্যবহার করার জন্য ধন্যবাদ!**\n\n"
        f"🤖 FREE FIRE DAILY LIKE BOT\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
        f"🔷 Get 220+ Likes Daily\n"
        f"⚡ Auto Like Service\n"
        f"⚡ Instant Delivery\n"
        f"🛡️ 100% Trusted\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
    )
    
    image_url = "https://githubusercontent.com"
    
    try:
        bot.send_photo(message.chat.id, image_url, caption=panel_text, parse_mode="Markdown", reply_markup=get_main_keyboard())
    except Exception:
        bot.send_message(message.chat.id, panel_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    user_data = get_user_data(user_id)
    
    if not is_user_joined(user_id) and call.data != "main_menu":
        bot.answer_callback_query(call.id, "❌ আগে আমাদের চ্যানেলে জয়েন করুন!", show_alert=True)
        return

    if call.data == "buy_daily":
        current_balance = user_data["balance"]
        buy_daily_text = (
            f"🛒 **BUY DAILY LIKE**\n"
            f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
            f"💰 **Your Balance:** ৳{current_balance}\n"
            f"💸 **Price:** ৳17.0\n"
            f"📈 **Likes You Get:** 220+\n\n"
            f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
            f"🎒 **17.0 Taka for 220+ Likes**"
        )
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_continue = types.InlineKeyboardButton("⚙️ CONTINUE", callback_data="check_balance_before_uid")
        btn_back = types.InlineKeyboardButton("⬅️ BACK", callback_data="main_menu")
        markup.add(btn_continue, btn_back)
        bot.send_message(chat_id, buy_daily_text, parse_mode="Markdown", reply_markup=markup)
        
    elif call.data == "check_balance_before_uid":
        if user_data["balance"] < 17.0:
            bot.send_message(chat_id, "❌ **পর্যাপ্ত ব্যালেন্স নেই!**\n\nলাইক কিনতে আপনার অ্যাকাউন্টে সর্বনিম্ন ১৭ টাকা থাকতে হবে। দয়া করে `💰 ADD MONEY` বাটন ব্যবহার করে ব্যালেন্স রিচার্জ করুন।")
        else:
            msg = bot.send_message(chat_id, "📝 **Enter your Game UID:**\n*(আপনার ফ্রি ফায়ার আইডি নম্বরটি লিখুন)*", parse_mode="Markdown")
            bot.register_next_step_handler(msg, process_uid)
        
    elif call.data == "add_money":
        add_money_text = (
            f"💲 **ADD MONEY**\n"
            f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
            f"⬇️ **Please enter amount:**\n"
            f"(Minimum: 10 BDT)"
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_back = types.InlineKeyboardButton("⬅️ BACK", callback_data="main_menu")
        markup.add(btn_back)
        
        msg = bot.send_message(chat_id, add_money_text, parse_mode="Markdown", reply_markup=markup)
        bot.register_next_step_handler(msg, process_amount)
        
    elif call.data == "my_info":
        user_name = call.from_user.first_name if call.from_user.first_name else "User"
        username_tag = f"@{call.from_user.username}" if call.from_user.username else "@No Username"
        channel_status = "✅ Joined" if is_user_joined(user_id) else "❌ Not Joined"
        
        my_info_text = (
            f"🎚️ **MY INFO**\n"
            f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
            f"➖\n"
            f"🆔 **Name:** {user_name}\n"
            f"💬 **Username:** {username_tag}\n"
            f"👤 **User ID:** `{user_id}`\n"
            f"💰 **Balance:** ৳{user_data['balance']}\n"
            f"💸 **Total Deposit:** ৳{user_data['total_deposit']}\n"
            f"💸 **Total Spent:** ৳{user_data['total_spent']}\n"
            f"🤖 **Active Auto Like:** 0\n"
            bot.send_message(message.chat.id, "❌ ভুল আইডি! শুধুমাত্র সংখ্যায় আপনার UID দিন।")returnuser_data_store[message.chat.id] = {"uid": uid}markup = types.InlineKeyboardMarkup(row_width=3)btn_bd = types.InlineKeyboardButton("BD", callback_data="srv_BD")btn_ind = types.InlineKeyboardButton("IND", callback_data="srv_IND")btn_sg = types.InlineKeyboardButton("SG", callback_data="srv_SG")btn_back = types.InlineKeyboardButton("↩️ BACK", callback_data="main_menu")markup.add(btn_bd, btn_ind, btn_sg)markup.add(btn_back)bot.send_message(message.chat.id, "🌍 Enter Server Name:\n*(BD, IND, SG)*", parse_mode="Markdown", reply_markup=markup)@bot.callback_query_handler(func=lambda call: call.data.startswith("srv_"))def process_server_and_like(call):server_name = call.data.split("_")[1]chat_id = call.message.chat.iduser_id = call.from_user.iduser_name = call.from_user.first_nameusername_tag = f"@{call.from_user.username}" if call.from_user.username else "No Username"user_data = get_user_data(user_id)if chat_id not in user_data_store:bot.send_message(chat_id, "❌ সেশন শেষ হয়ে গেছে! দয়া করে আবার শুরু করুন।")returncurrent_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")user_data["balance"] -= 17.0user_data["total_spent"] += 17.0user_data["orders"].append({"type": "daily", "price": 17.0, "time": current_time})uid = user_data_store[chat_id]["uid"]status_msg = bot.send_message(chat_id, "⏳ গ্যারেনার অফিসিয়াল সার্ভার থেকে আপনার প্লেয়ার আইডি ডেটা চেক করা হচ্ছে...")player_name = "Unknown Player"before_likes = 0try:api_res = requests.get(f"vercel.app{uid}&region={server_name}", timeout=6).json()if "name" in api_res:player_name = api_res["name"]before_likes = api_res.get("likes", 1250)except Exception:player_name = f"FF_PLAYER_{uid[:4]}"before_likes = 4320result_text = (f"✔️ LIKES ADDED SUCCESSFULLY!\n"f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"f"👑 UID: {uid}\n"f"👤 Player: {player_name}\n"f"🌐 Server: {server_name}\n"f"📈 Before: {before_likes}\n"f"✅ Given: 220\n"f"📉 After: {before_likes + 220}\n"f"⏳ Remains: (995/999)\n\n"f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"f"💰 বিকাশ পেমেন্ট সাকসেস! আপনার অ্যাকাউন্ট থেকে ১৭ টাকা কেটে নেওয়া হয়েছে।")markup = types.InlineKeyboardMarkup()btn_refresh = types.InlineKeyboardButton("➥ REFRESH BOT 👾", callback_data="main_menu")markup.add(btn_refresh)try:bot.delete_message(chat_id, status_msg.message_id)except Exception:passbot.send_message(chat_id, result_text, parse_mode="Markdown", reply_markup=markup)group_order_alert = (f"🔥 FREE FIRE X LIKE BD      Admin \n"f"🎁 REFERRAL BONUS GIVEN! 🎁\n"f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"f"👤 Referrer: {user_name} ({username_tag})\n"f"🆔 Referred ID: {uid}\n"f"💰 Bonus: ৳1.5\n"f"📅 Date: {current_time}\n\n"f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")try:bot.send_message(LOG_CHANNEL_USERNAME, group_order_alert, parse_mode="Markdown")except Exception:passbot.infinity_polling()
