from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from crud_functions_2 import *

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

products = get_all_products()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text = 'Рассчитать')
button2 = KeyboardButton(text = 'Информация')
button3 = KeyboardButton(text = 'Купить')
button4 = KeyboardButton(text = 'Регистрация')
kb.add(button1, button2)
kb.add(button3, button4)

kb2 = InlineKeyboardMarkup()
button2_1 = InlineKeyboardButton(text= 'Рассчитать норму калорий', callback_data ='calories')
button2_2 = InlineKeyboardButton(text= 'Формулы расчёта', callback_data ='formulas')
kb2.add(button2_1, button2_2)

kb3 = InlineKeyboardMarkup()
button3_1 = InlineKeyboardButton(text= 'Product1', callback_data="product_buying")
button3_2 = InlineKeyboardButton(text= 'Product2', callback_data="product_buying")
button3_3 = InlineKeyboardButton(text= 'Product3', callback_data="product_buying")
button3_4 = InlineKeyboardButton(text= 'Product4', callback_data="product_buying")
kb3.add(button3_1, button3_2)
kb3.add(button3_3, button3_4)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000

@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler(text = 'Купить')
async def get_buying_list(message):
    i=0
    for product in products:
        i=i+1
        with open(f'file{i}.png', 'rb') as img:
            await message.answer_photo(img, f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
    await message.answer('Выберите продукт для покупки:', reply_markup=kb3)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = kb2)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    result = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 5
    await message.answer(f'Норма калорий в сутки: {str(result)}', reply_markup = kb)
    await state.finish()

@dp.message_handler(text = 'Информация')
async def inform_massage(message):
    await message.answer('Информация о боте.')

@dp.message_handler(text = 'Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state = RegistrationState.username)
async def set_username(message, state):
    if not is_included(message.text):
        await state.update_data(username = message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()

@dp.message_handler(state = RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email = message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()

@dp.message_handler(state = RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age = message.text)
    data_user = await state.get_data()
    add_user(data_user['username'], data_user['email'], int(data_user['age']))
    await message.answer('Регистрация прошла успешно!', reply_markup = kb)
    await state.finish()

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

#connection.close()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)
