import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("❌ Токен не найден. Добавьте его в .env")
    exit()

total_numbers = 60
free_numbers = set()
used_numbers = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я бот для случайного выбора номеров.\n"
        "/total 60 — установить общее количество (умолчание 60)\n"
        "/free — выбрать свободные номера\n"
        "/random — выбрать номер\n"
        "/restart — сбросить"
    )

async def set_total(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global total_numbers, used_numbers, free_numbers
    try:
        total_numbers = int(context.args[0])
        used_numbers.clear()
        free_numbers.clear()
        await update.message.reply_text(f"✅ Установлено общее количество: {total_numbers}")
    except:
        await update.message.reply_text("❗ Пример: /total 65")

async def set_free(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global free_numbers
    try:
        nums = {int(n) for n in context.args}
        free_numbers = nums
        await update.message.reply_text(f"🆓 Свободные номера: {sorted(free_numbers)}")
    except:
        await update.message.reply_text("❗ Пример: /free 5 10 15")

async def pick_random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global total_numbers, free_numbers, used_numbers
    all_numbers = set(range(1, total_numbers + 1))
    available = all_numbers - free_numbers - used_numbers
    if not available:
        await update.message.reply_text("❌ Больше нет доступных номеров.")
        return
    choice = random.choice(list(available))
    used_numbers.add(choice)
    await update.message.reply_text(f"🎲 Выбран номер: {choice}")

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global total_numbers, free_numbers, used_numbers
    total_numbers = 60
    free_numbers.clear()
    used_numbers.clear()
    await update.message.reply_text("🔄 Всё сброшено.")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("total", set_total))
app.add_handler(CommandHandler("free", set_free))
app.add_handler(CommandHandler("random", pick_random))
app.add_handler(CommandHandler("restart", restart))

print("✅ Бот запущен.")
app.run_polling()
