import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from threading import Thread
from flask import Flask

# --- Flask для проверки работы бота онлайн ---
app = Flask('')

@app.route('/')
def home():
    return "Бот онлайн ✅"

def run():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run).start()

# --- Токен бота ---
TOKEN = "8512796088:AAGA4zGQJ_sS2QOs6Xv2AyHETxwjGyO0ZYA"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Словарь товаров ---
products = {
    "1": {"name": "Буст Андроид", "price": 40, "link": "https://telegra.ph/Optimizaciya-bust-FPS-ANDROID-05-22"},
    "2": {"name": "Буст IOS", "price": 40, "link": "https://telegra.ph/Optimizaciya-bust-FPS-IPHONE-05-22"},
    "3": {"name": "Буст ПК", "price": 100, "link": "https://telegra.ph/Povyshenie-FPS-Vo-Vseh-Igrah-05-06"},
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
    await message.answer("👋 Добро пожаловать!\nВыберите действие 👇", reply_markup=main_menu())

# --- Каталог ---
@dp.callback_query(lambda c: c.data == "catalog")
async def catalog(callback: types.CallbackQuery):
    await callback.message.answer("🛍 Каталог товаров:", reply_markup=catalog_menu())

# --- Назад в главное меню ---
@dp.callback_query(lambda c: c.data == "back")
async def back(callback: types.CallbackQuery):
    await callback.message.answer("Вы вернулись в главное меню 👇", reply_markup=main_menu())

# --- Информация ---
@dp.callback_query(lambda c: c.data == "info")
async def info(callback: types.CallbackQuery):
    await callback.message.answer(
        "ℹ️ Информация:\n\n"
        "💌 Поддержка: @BussinesBrain\n"
        "📢 Канал: @Business_W_ideas\n\n"
        "Оплата товаров осуществляется через Telegram Stars"
    )

# --- Покупка товаров ---
@dp.callback_query(lambda c: c.data.startswith("buy_"))
async def buy(callback: types.CallbackQuery):
    pid = callback.data.split("_")[1]
    product = products.get(pid)
    if not product:
        await callback.message.answer("❌ Товар не найден")
        return

    prices = [LabeledPrice(label=product["name"], amount=product["price"])]
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=product["name"],
        description="Цифровой товар",
        payload=pid,
        currency="XTR",          # ⭐ Telegram Stars
        prices=prices,
        provider_token=""        # оставляем пустым для Stars
    )

# --- Предоплата ---
@dp.pre_checkout_query()
async def checkout(q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(q.id, ok=True)

# --- Успешная оплата ---
@dp.message(lambda m: m.successful_payment)
async def success(msg: types.Message):
    pid = msg.successful_payment.invoice_payload
    link = products[pid]["link"]
    await msg.answer(f"✅ Оплата успешна!\nВот ваш товар:\n{link}")

# --- Запуск бота ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

