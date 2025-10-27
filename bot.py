import telebot
import random

# 🧩 حط توكن البوت بتاعك هنا
BOT_TOKEN = "7669001756:AAGF6Yrz0wofOX7H_QN8c9HBENUp3rgb4Hk"
bot = telebot.TeleBot(BOT_TOKEN)

# 👑 مطور وصاحب اللعبة
CREATOR = "@G3_J6"

# 🎭 سيناريوهات اللعبة
scenarios = [
    {
        "situation": "صحيت متأخر النهارده.. تروح الشغل ولا تزوغ؟",
        "choices": ["اروح الشغل", "أزوغ وأكمل نوم"],
        "results": ["المدير مبسوط منك 👏", "اتخصم منك يوم 😅"]
    },
    {
        "situation": "صاحبك عرض عليك تدخل معاه مشروع صغير.. تعمل إيه؟",
        "choices": ["أشارك", "أرفض"],
        "results": ["كسبت أول 10 آلاف جنيه 💰", "المشروع نجح من غيرك 😢"]
    },
    {
        "situation": "جالك عرض تسافر برة.. بس هتسيب حبيبتك 😬",
        "choices": ["أسافر", "أبقى معاها"],
        "results": ["بقيت ناجح جدًا برا 💼", "العلاقة انتهت بعد سنة 💔"]
    },
    {
        "situation": "لقيت محفظة فيها فلوس في الشارع 😯",
        "choices": ["أرجعها", "آخدها"],
        "results": ["ربنا كرمك بعد كده 🙏", "اتقفشت في الكاميرات 😅"]
    },
    {
        "situation": "قررت تبدأ دايت.. تلتزم ولا لأ؟",
        "choices": ["ألتزم", "أفشل"],
        "results": ["بقيت فورمة 🔥", "زيدت 5 كيلو 😂"]
    },
    {
        "situation": "حد شتمك في الشارع.. ترد ولا تتجاهل؟",
        "choices": ["أتجاهل", "أرد عليه"],
        "results": ["الناس احترمتك 👏", "خناقة ونقطة شرطة 🥴"]
    },
]

# 🧾 تقدم كل مستخدم
user_progress = {}

@bot.message_handler(commands=['start'])
def start_game(message):
    user_id = message.from_user.id
    user_progress[user_id] = {"step": 0, "story": []}
    bot.send_message(
        message.chat.id,
        f"👋 أهلاً بيك في لعبة *حياة جديدة | New Life*!\n"
        f"كل قرار هيغير مصيرك 💫\n\n"
        f"👨‍💻 مطور وصاحب اللعبة: {CREATOR}"
    )
    send_next_step(message.chat.id, user_id)

def send_next_step(chat_id, user_id):
    step = user_progress[user_id]["step"]
    if step < len(scenarios):
        s = scenarios[step]
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for choice in s["choices"]:
            markup.add(choice)
        bot.send_message(chat_id, f"🌀 {s['situation']}", reply_markup=markup)
    else:
        ending = random.choice([
            "أصبحت مليونير 💸",
            "دخلت السجن 🏛️",
            "بقيت مشهور 🕶️",
            "اتجوزت واتطلقت مرتين 😂",
            "سافرت وبدأت حياة جديدة ✈️"
        ])
        bot.send_message(chat_id, f"🏁 نهاية رحلتك:\n{ending}\n\n👨‍💻 المطور: {CREATOR}")
        del user_progress[user_id]

@bot.message_handler(func=lambda m: True)
def handle_choice(message):
    user_id = message.from_user.id
    if user_id not in user_progress:
        bot.send_message(message.chat.id, "اكتب /start عشان تبدأ اللعبة 🎮")
        return
    step = user_progress[user_id]["step"]
    s = scenarios[step]
    if message.text in s["choices"]:
        idx = s["choices"].index(message.text)
        result = s["results"][idx]
        bot.send_message(message.chat.id, f"📜 النتيجة: {result}")
        user_progress[user_id]["step"] += 1
        send_next_step(message.chat.id, user_id)
    else:
        bot.send_message(message.chat.id, "اختار من الاختيارات اللي قدامك يا نجم 😎")

print("🤖 Bot is running...")
bot.polling()