import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

SURA_NAMES = [
    "الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال", "التوبة", "يونس",
    "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف", "مريم", "طه",
    "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم",
    "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر",
    "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح", "الحجرات", "ق",
    "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد", "المجادلة", "الحشر", "الممتحنة",
    "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج",
    "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", "النازعات", "عبس",
    "التكوير", "الإنفطار", "المطففين", "الإنشقاق", "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد",
    "الشمس", "الليل", "الضحى", "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", "العاديات",
    "القارعة", "التكاثر", "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر",
    "المسد", "الإخلاص", "الفلق", "الناس"
]

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("الاستماع لسورة", callback_data='listen')],
        [InlineKeyboardButton("تحميل سورة", callback_data='download')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("مرحباً بك في بوت تلاوات الشيخ المنشاوي، اختر ما تريد:", reply_markup=reply_markup)

def choose_sura(update: Update, context: CallbackContext):
    query = update.callback_query
    choice = query.data
    query.answer()
    keyboard = []
    for i, name in enumerate(SURA_NAMES):
        num = f"{i+1:03}"
        keyboard.append([InlineKeyboardButton(name, callback_data=f"{choice}_{num}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="اختر السورة:", reply_markup=reply_markup)

def send_sura(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data
    action, sura_num = data.split('_')
    index = int(sura_num) - 1
    sura_name = SURA_NAMES[index]
    url = f"https://server8.mp3quran.net/minshawi/{sura_num}.mp3"
    if action == 'listen':
        query.message.reply_audio(audio=url, title=sura_name)
    elif action == 'download':
        query.message.reply_document(document=url, filename=f"{sura_name}.mp3")

def main():
    TOKEN = os.environ.get("BO7731557629:AAEcIIYj5f0C3S14ypob_pK51CDn_sIfk2M")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(choose_sura, pattern='^(listen|download)$'))
    dp.add_handler(CallbackQueryHandler(send_sura, pattern='^(listen|download)_\d{3}$'))
    updater.start_polling()
    print("البوت يعمل الآن...")
    updater.idle()

if __name__ == '__main__':
    main()
