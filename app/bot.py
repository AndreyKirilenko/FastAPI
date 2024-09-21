import logging
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, Update, WebhookInfo
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import uvicorn
from contextlib import asynccontextmanager
from handlers import questions # Импорт файла хендлеров
from settings import settings



bot = Bot(token=settings.TELEGRAM_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_routers(questions.router) # подключение роутеров к диспетчеру ПОРЯДОК ВАЖЕН!!


async def set_webhook(my_bot: Bot) -> None:
    # Check and set webhook for Telegram
    async def check_webhook() -> WebhookInfo | None:
        try:
            webhook_info = await my_bot.get_webhook_info()
            return webhook_info
        except Exception as e:
            logging.error(f"Can't get webhook info - {e}")
            return

    current_webhook_info = await check_webhook()
    if settings.debug:
        logging.debug(f"Current bot info: {current_webhook_info}")
    try:
        await my_bot.set_webhook(
            f"{settings.TUNA_WEPHOOK_URL}{settings.WEPHOOK_PATH}",
            drop_pending_updates=current_webhook_info.pending_update_count > 0,
            max_connections=40 if settings.debug else 100,
        )
        if logging.debug:
            logging.debug(f"Updated bot info: {await check_webhook()}")
    except Exception as e:
        logging.error(f"Can't set webhook - {e}")


async def start_telegram():
    # fr = await first_run()
    fr = True
    if settings.debug:
        logging.debug(f"First run: {fr}")
    if fr:
        await set_webhook(bot)
        # await set_bot_commands_menu(bot)

