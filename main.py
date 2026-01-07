import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, Text
from aiogram.utils import executor

API_TOKEN = '8512796088:AAGA4zGQJ_sS2QOs6Xv2AyHETxwjGyO0ZYA'  # Твой токен
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Установим уровень логирования
logging.basicConfig(level=logging.INFO)

# Список товаров и их цен в звездах
products = {
    "Буст Андроид": 83,
    "Буст IOS": 83,
    "Буст ПК": 165,
    "Все приложения от Adobe": 66,
    "Накрутка Часов в Steam + Открытие всех достижений": 165,
    "Отдача в PUBG MOBILE": 50,
    "59 способов фармить валюту на funtime": 50,
    "Способы получения 7 значков в Discord": 165,
    "Как распиарить свой Discord": 66,
    "Смена голоса в реальном времени": 83,
    "Невидимый ник в Brawl Stars и других играх": 83,
    "Гайд как играть без ВПН и лагов в Brawl Stars и другие игры": 83,
    "Способ, как написать в поддержку Supercell в РФ/РБ": 50,
    "Сборка модов на BeamNG.Drive": 50,
    "99к игр STEAM": 1155,
}

# Приветственное сообщение
@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await message.answer("Привет! Добро пожаловать в магазин товаров за звезды!\n\n"
                         "Вот доступные товары и их цена в звездах:\n" + "\n".join([f"{item}: {price} звезд" for item, price in products.items()]))

# Обработка покупки
@dp.message_handler(Text(equals="Покупка"))
async def start_purchase(message: Message):
    await message.answer("Напиши название товара, который хочешь купить, или 'отмена', чтобы отменить.")

# Проверка на товары
@dp.message_handler(lambda message: message.text in products)
async def confirm_purchase(message: Message):
    product = message.text
    stars_required = products[product]
    await message.answer(f"Ты выбрал {product}. Для покупки нужно {stars_required} звезд.\n"
                         "Отправь мне столько звезд, чтобы завершить покупку.")

# Завершение покупки
@dp.message_handler(lambda message: message.text.isdigit())
async def complete_purchase(message: Message):
    stars_sent = int(message.text)
    if stars_sent >= 1:  # Тут можно настроить логику с проверкой на количество звезд
        await message.answer(f"Покупка успешна! Ты приобрел товар за {stars_sent} звезд!")
    else:
        await message.answer("Неверное количество звезд. Попробуй снова.")

# Отмена покупки
@dp.message_handler(Text(equals="отмена"))
async def cancel_purchase(message: Message):
    await message.answer("Покупка отменена.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
