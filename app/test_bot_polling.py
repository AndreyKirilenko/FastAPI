#----------------------------------------------#
#                                              #
#   Тестовый бот на AIOGRAM 3 работает         #
#                                              #
#----------------------------------------------#

from aiogram import Bot, types, Dispatcher
from aiogram.filters import Command
from settings import settings
from aiogram import Router, F
import asyncio
import logging

bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher()
start_router = Router()

@start_router.message(Command("start"))
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@start_router.message(Command("help"))
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@start_router.message()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    asyncio.run(main())
