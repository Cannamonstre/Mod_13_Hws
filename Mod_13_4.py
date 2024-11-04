from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


API = '*your_API_must_be_here*'
botik = Bot(token=API)
dp = Dispatcher(botik, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    height = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(msg):
    await msg.answer("Hi! I'll help you with daily calorie limit. "
                     "Just use /calories")


@dp.message_handler(commands=['calories'])
async def set_age(msg):
    await msg.answer('How old are you?')
    await UserState.age.set()


@dp.message_handler()
async def anything(msg):
    await msg.answer("Enter /start to begin")


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
