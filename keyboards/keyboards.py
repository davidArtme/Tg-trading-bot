from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON
#-------Создаем клавиатуру с кнопками, реагирующую на команду /start-------

# Создание кнопок с командами
button_get_price= KeyboardButton(text=LEXICON['get price'])
button_get_balance= KeyboardButton(text=LEXICON['get balance'])
button_set_market_order = KeyboardButton(text=LEXICON['set market order'])
button_set_limit_order = KeyboardButton(text=LEXICON['set limit order'])

# Инициализация билдера для клавиатуры
kb_builder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с аргументом width=2
kb_builder.row(button_get_price, button_get_balance, button_set_market_order, button_set_limit_order, width=2)

# Создаем клавиатуру с кнопками
kb: ReplyKeyboardMarkup = kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)


