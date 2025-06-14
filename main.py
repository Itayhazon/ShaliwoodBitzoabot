import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = "YOUR_TELEGRAM_TOKEN_HERE"

logging.basicConfig(level=logging.INFO)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("קיבלתי את ההקלטה! הפיצ'ר של עיבוד קולי ייכנס כאן.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.VOICE, handle_voice))
app.run_polling()
