from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
# Создаем объекты инлайн-кнопок для функции privateRequest
button_market = InlineKeyboardButton(
        text='Рыночная',
)
button_limit = InlineKeyboardButton(
        text='Лимитная',
)
# Создаем объект инлайн-клавиатуры для функции privateRequest
keyboard_private_request = InlineKeyboardMarkup(inline_keyboard=[[button_market], [button_limit]])