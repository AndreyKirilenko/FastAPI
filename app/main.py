import logging
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, Update, WebhookInfo
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from fastapi import FastAPI, BackgroundTasks

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import uvicorn
from contextlib import asynccontextmanager
import asyncio
from db.session import engine 
from db.base import Base


from handlers import questions # Импорт файла хендлеров
from routers import root_router
from pages.routers import pages_router
from api.base import api_router

def create_tables():         
	Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Start 🚀 application FastApi")
    from bot import start_telegram
    await start_telegram()
    create_tables()
    # await bot.set_webhook(url=f"{settings.TUNA_WEPHOOK_URL}/webhook",
    #                       allowed_updates=dp.resolve_used_update_types(),
    #                       drop_pending_updates=True)
    yield
    # Здесь функции выполняемые при остановке сервера 
    logging.info("⛔ Stopping application")

app = FastAPI(lifespan=lifespan)

app.include_router(pages_router)
app.include_router(root_router)
app.include_router(api_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")


# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


async def background_task():
    while True:
        print("Running background task...")
        await asyncio.sleep(1)  # Simulate some async operation



@app.get("/task")
async def start_background_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(background_task)

    return {"message": "Background task started"}



if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    uvicorn.run(app, host="0.0.0.0", port=8000)



# uvicorn main:app --reload


