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

from handlers import questions # Импорт файла хендлеров
from routers import root_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Start 🚀 application FastApi")
    from bot import start_telegram
    await start_telegram()
    # await bot.set_webhook(url=f"{settings.TUNA_WEPHOOK_URL}/webhook",
    #                       allowed_updates=dp.resolve_used_update_types(),
    #                       drop_pending_updates=True)
    yield
    logging.info("⛔ Stopping application")

app = FastAPI(lifespan=lifespan)
app.include_router(root_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# async def background_task():
#     while True:
#         print("Running background task...")
#         await asyncio.sleep(1)  # Simulate some async operation

# @app.get("/task")
# async def start_background_task(background_tasks: BackgroundTasks):
#     background_tasks.add_task(background_task)

#     return {"message": "Background task started"}



if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    uvicorn.run(app, host="0.0.0.0", port=8080)










# from fastapi import FastAPI
# from app.utils import json_to_dict_list
# import os
# from typing import Optional



# # Получаем путь к файлу с записями (типа БД)
# path_to_json = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'students.json')



# app = FastAPI() # Создание приложения


# @app.get("/students") # Обрабатываются GET запросы на маршрут /students
# def get_all_students():
#     return json_to_dict_list(path_to_json)


# @app.get("/") # Обрабатываются GET запросы на маршрут /
# def home_page():
#     return {"message": "Привет, Засранец!!"}


# @app.get("/students/{course}") #  В этом эндпойнте получаем студентов конкретного курса
# def get_all_students_course(course: int): #  Указываем тип данных
#     students = json_to_dict_list(path_to_json)
#     return_list = []
#     for student in students:
#         if student["course"] == course:
#             return_list.append(student)
#     return return_list


# # Можно обьеденить
# @app.get("/students")
# def get_all_students(course: Optional[int] = None): # Здесь course будет параметром запроса ...?course=1
#     students = json_to_dict_list(path_to_json)
#     if course is None:
#         return students
#     else:
#         return_list = []
#         for student in students:
#             if student["course"] == course:
#                 return_list.append(student)
#         return return_list
    
# # Здесь используем и параметр пути и параметры запроса
# @app.get("/students/{course}") #
# def get_all_students_course(course: int, major: Optional[str] = None, enrollment_year: Optional[int] = 2018):
#     students = json_to_dict_list(path_to_json)
#     filtered_students = []
#     for student in students:
#         if student["course"] == course:
#             filtered_students.append(student)

#     if major:
#         filtered_students = [student for student in filtered_students if student['major'].lower() == major.lower()]

#     if enrollment_year:
#         filtered_students = [student for student in filtered_students if student['enrollment_year'] == enrollment_year]

#     return filtered_students