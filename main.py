import logging
import datetime
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters
)


ASK_TASK, ASK_PURPOSE = range(2)


user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Selam! Şu an ne yapıyorsun?")
    return ASK_TASK


async def ask_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data['task'] = update.message.text
    await update.message.reply_text("Peki, bununla neyi başarıyorsun?")
    return ASK_PURPOSE


async def ask_purpose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    purpose = update.message.text
    task = user_data.get('task', 'Bilinmiyor')
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{now}] Yapılan: {task} | Amaç: {purpose}\n"

    with open("gunluk.txt", "a", encoding="utf-8") as f:
        f.write(entry)

    await update.message.reply_text("Kaydettim kardeşim. 45 dakika sonra yine soracağım.")
    return ConversationHandler.END


async def main():
    logging.basicConfig(level=logging.INFO)

 
    TOKEN = "7489334035:AAFmANAoc0PTV6T84htegHZHVncPzg7vdWI"

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_task)],
            ASK_PURPOSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_purpose)],
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
