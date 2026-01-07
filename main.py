import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Бот онлайн ✅"

def run():
    app.run(host="0.0.0.0", port=8080)

t = Thread(target=run)
t.start()

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

if not TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN environment variable is not set")
    exit(1)

# Все товары
products = {
    "1": {"name": "Буст Андроид", "price": 40, "link": "https://telegra.ph/Optimizaciya-bust-FPS-ANDROID-05-22"},
    "2": {"name": "Буст IOS", "price": 40, "link": "https://telegra.ph/Optimizaciya-bust-FPS-IPHONE-05-22"},
    "3": {"name": "Буст ПК", "price": 100, "link": "https://telegra.ph/Povyshenie-FPS-Vo-Vseh-Igrah-05-06"},
    # … Добавь остальные товары
}

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛍 Каталог", callback_data="catalog")],
        [InlineKeyboardButton(text="ℹ️ Информация", callback_data="info")]
    ])

# Каталог товаров
def catalog_menu():
    keyboard = []
    for pid, p in products.items():
        keyboard.append([InlineKeyboardButton(
            text=f"🛒 {p['name']} — {p['price']}⭐",
            callback_data=f"buy_{pid}"
        )])
    keyboard.append([InlineKeyboardButton(text="⬅ Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Стартовая команда
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Здесь вы можете купить цифровые товары за Telegram ⭐️\n\n"
        "Выберите действие 👇",
        reply_markup=main_menu()
    )

# Каталог
@dp.callback_query(lambda c: c.data == "catalog")
async def catalog(callback: types.CallbackQuery):
    await callback.message.answer(
        "🛍 Каталог товаров:",
        reply_markup=catalog_menu()
    )

# Информация
@dp.callback_query(lambda c: c.data == "info")
async def info(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 ЛС", url="https://t.me/BussinesBrain")],
        [InlineKeyboardButton(text="📢 Канал", url="https://t.me/Business_W_ideas")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="back")]
    ])
    await callback.message.answer(
        "ℹ️ Информация:\n\n"
        "Оплата происходит через Telegram Stars.\n"
        "После оплаты товар приходит автоматически.\n\n"
        "Вы можете связаться с поддержкой или подписаться на канал:",
        reply_markup=keyboard
    )

# Назад в меню
@dp.callback_query(lambda c: c.data == "back")
async def back(callback: types.CallbackQuery):
    await callback.message.answer(
        "Главное меню:",
        reply_markup=main_menu()
    )

# Покупка товара
@dp.callback_query(lambda c: c.data.startswith("buy_"))
async def buy(callback: types.CallbackQuery):
    pid = callback.data.split("_")[1]
    product = products[pid]

    prices = [LabeledPrice(label=product['name'], amount=product['price'])]
    await bot.send_invoice(
        callback.from_user.id,
        title=product['name'],
        description="Цифровой товар",
        payload=pid,
        currency="XTR",
        prices=prices
    )

# Предоплата
@dp.pre_checkout_query()
async def checkout(q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(q.id, ok=True)

# Успешная оплата
@dp.message(lambda m: m.successful_payment)
async def success(msg: types.Message):
    pid = msg.successful_payment.invoice_payload
    link = products[pid]['link']
    await msg.answer(f"✅ Оплата успешна!\n\nВот ваш товар:\n{link}")

# Основной цикл
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

