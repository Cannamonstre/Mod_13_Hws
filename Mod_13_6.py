from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


API = '7744477667:AAExHvKav97KgTOYfr6TeFosGFsVmVSKjmw'
botik = Bot(token=API)
dp = Dispatcher(botik, storage=MemoryStorage())

inl_kb = InlineKeyboardMarkup()
bt_cal_count = InlineKeyboardButton(text='Calorie count', callback_data='calories')
bt_cal_forms = InlineKeyboardButton(text='Calculation formula', callback_data='formula')
inl_kb.add(bt_cal_count, bt_cal_forms)


@dp.message_handler(commands=['start'])
async def start(msg):
    await msg.answer("Hi! I'll help you with daily calorie limit. "
                     "Just use /options")


@dp.message_handler(commands=['options'])
async def main_menu(msg):
    await msg.answer('Choose the option: ', reply_markup=inl_kb)


@dp.callback_query_handler(text='formula')
async def get_formulas(call):
    await call.message.answer('10 x weight (kg) + 6,25 x height (sm) – 5 x age (yr) – 100')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('How old are you?')
    await UserState.age.set()
    await call.answer()


class UserState(StatesGroup):
    age = State()
    height = State()
    weight = State()


@dp.message_handler(state=UserState.age)
async def set_height(msg, state):
    await state.update_data(age=msg.text)
    await msg.answer('How tall are you?')
    await UserState.height.set()


@dp.message_handler(state=UserState.height)
async def set_weight(msg, state):
    await state.update_data(height=msg.text)
    await msg.answer('How much do you weigh?')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(msg, state):
    await state.update_data(weight=msg.text)
    data = await state.get_data()
    age = int(data.get('age', 0))
    height = int(data.get('height', 0))
    weight = int(data.get('weight', 0))
    await msg.answer(f'Your daily calorie limit to start losing weight is: '
                     f'{10 * weight + 6.25 * height - 5 * age - 100} Cal.')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
