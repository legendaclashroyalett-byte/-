import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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

# Вставь сюда свой токен бота
TOKEN = "8512796088:AAGA4zGQJ_sS2QOs6Xv2AyHETxwjGyO0ZYA"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Все товары
products = {
    "1": {"name": "Буст Андроид", "link": "https://telegra.ph/Optimizaciya-bust-FPS-ANDROID-05-22"},
    "2": {"name": "Буст IOS", "link": "https://telegra.ph/Optimizaciya-bust-FPS-IPHONE-05-22"},
    "3": {"name": "Буст ПК", "link": "https://telegra.ph/Povyshenie-FPS-Vo-Vseh-Igrah-05-06"},
    "4": {"name": "Все приложения от Adobe", "link": "https://telegra.ph/Vse-prilozheniya-ot-Adobe-12-21"},
    "5": {"name": "Накрутка Часов в Steam + Открытие всех достижений", "link": "https://docs.google.com/document/d/1dGeuBe0JXkmkg07qD41mB5g_ZSUIpXxmLZ1d1eBK9e4/edit?usp=sharing"},
    "6": {"name": "Отдача в PUBG MOBILE", "link": "https://docs.google.com/document/d/1sO04gtjn0vpzs2nTchc0rVHIA495WHY-5U70bDT56GE/edit?usp=drivesdk"},
    "7": {"name": "59 способов фармить валюту на funtime", "link": "https://telegra.ph/59-sposobov-zarabotka-Funtime-03-01"},
    "8": {"name": "Способы получения 7 значков в Discord", "link": "https://telegra.ph/SPOSOBY-POLUCHENIYA-7-ZNACHKOV-V-DISCORD-02-15"},
    "9": {"name": "Как распиарить свой Discord", "link": "https://telegra.ph/Kak-raspiarit-svoj-diskord-server-03-01"},
    "10": {"name": "Смена голоса в реальном времени", "link": "https://telegra.ph/Smena-golosa-v-realnom-vremeni-05-18"},
    "11": {"name": "Как сделать невидимый ник в Brawl Stars и других играх", "link": "https://telegra.ph/%D0%9Aak-sdelat-nevidimyj-nik-v-Brawl-Stars-i-drugih-igrah-05-18"},
    "12": {"name": "Гайд как играть без ВПН и лагов в Brawl Stars", "link": "https://telegra.ph/Gajd-kak-igrat-bez-VPN-i-lagov-v-Brawl-Stars-05-18"},
    "13": {"name": "Способ, как написать в поддержку Supercell в РФ/РБ", "link": "https://telegra.ph/Support-Supercell-RF-RB-05-18"},
    "14": {"name": "Сборка модов на BeamNG.Drive", "link": "https://disk.yandex.ru/d/tjLjXo2fZnt-fA"},
    "15": {"name": "Сборка модов 2.0 на BeamNG.Drive", "link": "https://disk.yandex.ru/d/XSwnu4b0CCOhrQ"},
    "16": {"name": "99к игр STEAM", "link": "https://telegra.ph/Steam-05-22-24"}
}

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
            text=f"🛒 {p['name']}",
            callback_data=f"buy_{pid}"
        )])
    keyboard.append([InlineKeyboardButton(text="⬅ Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Стартовая команда
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Здесь вы можете посмотреть цифровые товары.\n\n"
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
    await callback.message.answer(
        "ℹ️ Информация о боте:\n\n"
        "ЛС для поддержки: https://t.me/BussinesBrain\n"
        "Канал: https://t.me/Business_W_ideas"
    )

# Назад в главное меню
@dp.callback_query(lambda c: c.data == "back")
async def back(callback: types.CallbackQuery):
    await callback.message.answer(
        "Вы вернулись в главное меню 👇",
        reply_markup=main_menu()
    )

# Покупка товара (отправка ссылки)
@dp.callback_query(lambda c: c.data.startswith("buy_"))
async def buy(callback: types.CallbackQuery):
    pid = callback.data.split("_")[1]
    product = products.get(pid)

    if not product:
        await callback.message.answer("❌ Товар не найден.")
        return

    await callback.message.answer(
        f"🛒 Вы выбрали: {product['name']}\n"
        f"Ссылка на товар: {product['link']}"
    )

# Основной цикл
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
