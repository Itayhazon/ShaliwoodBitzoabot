print("=== MAIN.PY LOADED 2002===")

import logging
import os
import tempfile
import openai
import telegram  # For debugging path
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Debug path to telegram module
print(">>> TELEGRAM MODULE LOCATION:", telegram.__file__)

# Load secrets from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Your bot's token from BotFather
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Your OpenAI API key
openai.api_key = OPENAI_API_KEY  # Set API key for use in openai package

# Set logging level to INFO (for debugging and tracking)
logging.basicConfig(level=logging.INFO)

# Define the handler for voice messages
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        voice = update.message.voice
        file = await context.bot.get_file(voice.file_id)

        # Save voice file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_audio:
            await file.download_to_drive(temp_audio.name)

            # Send the file to Whisper (OpenAI) to transcribe the speech to text
            with open(temp_audio.name, "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)

            text = transcript["text"]

        # Send the transcribed text back to the user
        await update.message.reply_text(f"Recognized text:\n{text}")

    except Exception as e:
        # If something goes wrong, log and send the error
        logging.error(f"Error: {e}")
        await update.message.reply_text(f"Error occurred while processing:\n{e}")

# Initialize the bot application and run it
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.VOICE, handle_voice))  # Set handler for voice messages
app.run_polling()  # Start polling (wait for messages)
