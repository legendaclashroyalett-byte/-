import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    LabeledPrice,
    PreCheckoutQuery,
)
from aiogram.filters import Command
from flask import Flask
from threading import Thread

# -------------------- Flask (чтобы сервис не засыпал) --------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is online"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run_flask, daemon=True).start()

# -------------------- BOT --------------------
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN not set")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# -------------------- ТОВАРЫ --------------------
products = {
    "1": {"name": "Буст Android", "price": 40, "link": "https://telegra.ph/Optimizaciya-bust-FPS-ANDROID-05-22"},
    "2": {"name": "Буст iOS", "price": 40, "link": "https://telegra.ph/Optimizaciya-bust-FPS-IPHONE-05-22"},
    "3": {"name": "Буст ПК", "price": 100, "link": "https://telegra.ph/Povyshenie-FPS-Vo-Vseh-Igrah-05-06"},
    "4": {"name": "Все приложения Adobe", "price": 20, "link": "https://telegra.ph/Vse-prilozheniya-ot-Adobe-12-21"},
    "5": {"name": "Steam часы + достижения", "price": 50, "link": "https://docs.google.com/document/d/1dGeuBe0JXkmkg07qD41mB5g_ZSUIpXxmLZ1d1eBK9e4/edit"},
    "6": {"name": "Отдача PUBG Mobile", "price": 40, "link": "https://docs.google.com/document/d/1sO04gtjn0vpzs2nTchc0rVHIA495WHY-5U70bDT56GE/edit"},
    "7": {"name": "59 способов фарма Funtime", "price": 25, "link": "https://telegra.ph/59-sposobov-zarabotka-Funtime-03-01"},
    "8": {"name": "7 значков Discord", "price": 40, "link": "https://telegra.ph/SPOSOBY-POLUCHENIYA-7-ZNACHKOV-V-DISCORD-02-15"},
    "9": {"name": "Раскрутка Discord", "price": 30, "link": "https://telegra.ph/Kak-raspiarit-svoj-diskord-server-03-01"},
    "10": {"name": "Смена голоса", "price": 30, "link": "https://telegra.ph/Smena-golosa-v-realnom-vremeni-05-18"},
    "11": {"name": "Невидимый ник Brawl Stars", "price": 50, "link": "https://telegra.ph/Kak-sdelat-nevidimyj-nik-v-Brawl-Stars-05-18"},
    "12": {"name": "Brawl Stars без VPN", "price": 40, "link": "https://telegra.ph/Gajd-kak-igrat-bez-VPN-i-lagov-v-Brawl-Stars-05-18"},
    "13": {"name": "Поддержка Supercell", "price": 20, "link": "https://telegra.ph/Support-Supercell-RF-RB-05-18"},
    "14": {"name": "BeamNG моды", "price": 30, "link": "https://disk.yandex.ru/d/tjLjXo2fZnt-fA"},
    "15": {"name": "BeamNG моды 2.0", "price": 30, "link": "https://disk.yandex.ru/d/XSwnu4b0CCOhrQ"},
    "16": {"name": "99k игр Steam", "price": 500, "link": "https://telegra.ph/Steam-05-22-24"},
}

# -------------------- КНОПКИ --------------------
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛍 Каталог", callback_data="catalog")],
        [InlineKeyboardButton(text="ℹ️ Информация", callback_data="info")]
    ])

def catalog_menu():
    kb = []
    for pid, p in products.items():
        kb.append([
            InlineKeyboardButton(
                text=f"{p['name']} — {p['price']} ⭐",
                callback_data=f"buy:{pid}"
            )
        ])
    kb.append([InlineKeyboardButton(text="⬅ Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

# -------------------- ХЕНДЛЕРЫ --------------------
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Покупка цифровых товаров за ⭐ Telegram Stars",
        reply_markup=main_menu()
    )

@dp.callback_query(F.data == "catalog")
async def catalog(cb: CallbackQuery):
    await cb.message.edit_text("🛍 Каталог товаров:", reply_markup=catalog_menu())
    await cb.answer()

@dp.callback_query(F.data == "back")
async def back(cb: CallbackQuery):
    await cb.message.edit_text("Главное меню 👇", reply_markup=main_menu())
    await cb.answer()

@dp.callback_query(F.data == "info")
async def info(cb: CallbackQuery):
    await cb.message.edit_text(
        "ℹ️ Информация\n\n"
        "💌 Поддержка: @BussinesBrain\n"
        "📢 Канал: @Business_W_ideas\n\n"
        "Оплата через Telegram ⭐",
        reply_markup=main_menu()
    )
    await cb.answer()

# -------------------- ПОКУПКА (STARS) --------------------
@dp.callback_query(F.data.startswith("buy:"))
async def buy(cb: CallbackQuery):
    pid = cb.data.split(":")[1]
    product = products.get(pid)

    if not product:
        await cb.answer("Товар не найден", show_alert=True)
        return

    prices = [LabeledPrice(label=product["name"], amount=product["price"])]

    await bot.send_invoice(
        chat_id=cb.from_user.id,
        title=product["name"],
        description="Цифровой товар",
        payload=pid,
        currency="XTR",
        prices=prices
    )
    await cb.answer()

@dp.pre_checkout_query()
async def pre_checkout(q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(q.id, ok=True)

@dp.message(F.successful_payment)
async def success(msg: Message):
    pid = msg.successful_payment.invoice_payload
    link = products[pid]["link"]
    await msg.answer(f"✅ Оплата прошла!\n\n🔗 Ваш товар:\n{link}")

# -------------------- ЗАПУСК --------------------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
