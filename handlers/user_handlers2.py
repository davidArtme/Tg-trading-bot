from aiogram import F, Router, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from keyboards.keyboards import kb
from lexicon.lexicon import LEXICON
from functions import get_price, get_wallet_balance, get_market_order_bybit, get_limit_order_bybit
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from services.inline_buttons import keyboard_private_request
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()
class States(StatesGroup):
    main_menu = State()
    ticker_price = State() # функция get price
    balance = State() # функция get wallet balance
    setMarketOrder = State() # функция get_private_market_order_binance
    setLimitOrder = State() # функция get_private_limit_order_binance

async def on_start():
    await bot.send_message(chat_id=ADMIN_ID, text="Бот запущен! Нажмите /start")
# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await state.set_state(States.main_menu)
    await message.answer(text=LEXICON['/start'], reply_markup=kb)
#-------------------------------------------------------
# Этот хэндлер срабатывает на клавишу "Узнать цену валютной пары"
@router.message(F.text == LEXICON['get price'])
async def process_get_price(message: Message, state: FSMContext):
    await state.set_state(States.ticker_price)
    await message.answer(text='Вы выбрали узнать стоимость валютной пары. Введите интересующую Вас валюту. Пример: BTCUSDT', reply_markup=kb)

@router.message(States.ticker_price)
async def process_get_price_2(message: Message, state: FSMContext):
    symbol_text = message.text
    answer_get_price = f'Текущая стоимость монеты {symbol_text} составляет {get_price(symbol_text)}'
    await message.answer(text=answer_get_price)
#-------------------------------------------------------
# Этот хэндлер срабатывает на клавишу "Узнать баланс кошелька"
@router.message(F.text == LEXICON['get balance'])
async def process_get_balance(message: Message, state: FSMContext):
    #await state.set_state(States.balance)
    answer_get_balance = f'Ваш баланс в USD: {get_wallet_balance()}'
    await message.answer(text=answer_get_balance)
#-------------------------------------------------------
# Этот хэндлер срабатывает на клавишу "Открыть рыночуную заявку"
@router.message(F.text == LEXICON['set market order'])
async def process_set_market_order(message: Message, state: FSMContext):
    await state.set_state(States.setMarketOrder)
    await message.answer(text='Введите ответ в формате: категория(спот - spot, фьючерсы - linear), символ, тип, сумма покупки. Пример: spot,TONUSDT,BUY,1')

@router.message(States.setMarketOrder)
async def process_set_market_order_2(message: Message, state: FSMContext):
    answer = message.text
    answer_lst = answer.split(',')
    market_order = get_market_order_bybit(answer_lst[0], answer_lst[1], answer_lst[2], float(answer_lst[3]))
    answer_text = f'Ваша рыночная заявка: "категория" - {answer_lst[0]}, "валютная пара - {answer_lst[1]}, тип - {answer_lst[2]}, сумма покупки - {answer_lst[3]}" успешно размещена! Ордер заявки - {market_order['result']['orderId']}'
    await message.answer(answer_text)
#---------------------------------------------------------
# Этот хэндлер срабатывает на клавишу "Открыть лимитную заявку"
@router.message(F.text == LEXICON['set limit order'])
async def process_set_limit_order(message: Message, state: FSMContext):
    await state.set_state(States.setLimitOrder)
    await message.answer(text='Введите ответ в формате: категория(спот - spot, фьючерсы - linear), символ, тип, стоимость, сумма покупки. Пример: spot,TONUSDT,BUY,5,1')

@router.message(States.setLimitOrder)
async def process_set_limit_order_2(message: Message, state: FSMContext):
    answer = message.text
    answer_lst = answer.split(',')
    limit_order = get_limit_order_bybit(answer_lst[0], answer_lst[1], answer_lst[2], float(answer_lst[3]), float(answer_lst[4]))
    answer_text_limit = f'Ваша лимитная заявка: "категория" - {answer_lst[0]}, "валютная пара - {answer_lst[1]}, тип - {answer_lst[2]}, стоимость - {answer_lst[3]}, сумма покупки - {answer_lst[4]}" успешно размещена! Ордер заявки - {limit_order['result']['orderId']}'
    await message.answer(answer_text_limit)
# ---------------------------------------------------------