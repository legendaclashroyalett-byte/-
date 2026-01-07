import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# --- Flask для проверки работы бота онлайн ---
app = Flask('')

@app.route('/')
def home():
    return "Бот онлайн ✅"

def run():
    app.run(host="0.0.0.0", port=8080)

t = Thread(target=run)
t.start()

# --- Токен бота из переменных окружения ---
import os
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
if not TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN environment variable is not set")
    exit(1)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Балансы пользователей ---
user_stars = {}  # {user_id: количество звезд}

# --- Словарь товаров ---
products = {
    "1": {"name": "Буст Андроид", "price": 40, "link": "https://telegra.ph/Optimizaciya-bust-FPS-ANDROID-05-22"},
    "2": {"name": "Буст IOS", "price": 40, "link": "https://telegra.ph/Optimizaciya-bust-FPS-IPHONE-05-22"},
    "3": {"name": "Буст ПК", "price": 100, "link": "https://telegra.ph/Povyshenie-FPS-Vo-Vseh-Igrah-05-06"},
    # добавляй остальные товары по такому же принципу
}

# --- Главное меню ---
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛍 Каталог", callback_data="catalog")],
        [InlineKeyboardButton(text="ℹ️ Информация", callback_data="info")]
    ])

# --- Каталог товаров ---
def catalog_menu():
    keyboard = []
    for pid, p in products.items():
        keyboard.append([InlineKeyboardButton(
            text=f"🛒 {p['name']} — {p['price']}⭐",
            callback_data=f"buy_{pid}"
        )])
    keyboard.append([InlineKeyboardButton(text="⬅ Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# --- Стартовый хендлер ---
@dp.message(Command("start"))
async def start(message: types.Message):
    user_stars.setdefault(message.from_user.id, 100)  # каждый новый юзер получает 100⭐
    await message.answer(
        f"👋 Добро пожаловать!\nУ вас {user_stars[message.from_user.id]}⭐\n\n"
        "Выберите действие 👇",
        reply_markup=main_menu()
    )

# --- Каталог ---
@dp.callback_query(Text("catalog"))
async def catalog(callback: types.CallbackQuery):
    await callback.message.answer(
        f"🛍 Каталог товаров:\nУ вас {user_stars.get(callback.from_user.id,0)}⭐",
        reply_markup=catalog_menu()
    )

# --- Назад в главное меню ---
@dp.callback_query(Text("back"))
async def back(callback: types.CallbackQuery):
    await callback.message.answer(
        f"Вы вернулись в главное меню 👇\nУ вас {user_stars.get(callback.from_user.id,0)}⭐",
        reply_markup=main_menu()
    )

# --- Информация ---
@dp.callback_query(Text("info"))
async def info(callback: types.CallbackQuery):
    await callback.message.answer(
        "ℹ️ Информация:\n\n"
        "💌 Поддержка: @BussinesBrain\n"
        "📢 Канал: @Business_W_ideas\n\n"
        "Покупка товаров осуществляется за Telegram ⭐"
    )

# --- Покупка товаров за звезды ---
@dp.callback_query(Text(startswith="buy_"))
async def buy(callback: types.CallbackQuery):
    pid = callback.data.split("_")[1]
    product = products.get(pid)
    if not product:
        await callback.message.answer("❌ Товар не найден")
        return

    user_id = callback.from_user.id
    user_balance = user_stars.get(user_id, 0)
    if user_balance < product['price']:
        await callback.message.answer(f"❌ У вас недостаточно ⭐. У вас {user_balance}⭐")
        return

    # списываем звёзды
    user_stars[user_id] -= product['price']

    await callback.message.answer(
        f"✅ Вы купили {product['name']} за {product['price']}⭐!\n"
        f"Ваш текущий баланс: {user_stars[user_id]}⭐\n\n"
        f"Вот ваш товар: {product['link']}"
    )

# --- Запуск бота ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
