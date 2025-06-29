import os

# Не нужно load_dotenv для Render (он нужен только локально)
# from dotenv import load_dotenv
# load_dotenv()

# Пробуем получить токен
TOKEN = os.getenv("TOKEN")

# Отладка: покажем токен
if not TOKEN:
    print("❌ Токен не найден. Убедитесь, что он задан в Render → Environment → TOKEN")
    exit()
else:
    print(f"✅ Найден токен: {TOKEN[:5]}... (обрезан для безопасности)")
