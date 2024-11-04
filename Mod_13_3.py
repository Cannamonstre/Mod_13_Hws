from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API = '*your_API_must_be_here*'
botik = Bot(token=API)
dp = Dispatcher(botik, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(msg):
    await msg.answer("Hi! I'm a health helper bot")


@dp.message_handler()
async def all_msgs(msg):
    await msg.answer('Use /start command to talk')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
