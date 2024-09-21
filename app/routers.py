# -*- coding: utf-8 -*-
__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'

from typing import Annotated

from fastapi import APIRouter, Header
import logging
from aiogram import types
from aiogram.types import Message, Update, WebhookInfo
from fastapi.requests import Request

from bot import bot, dp
# from settings import get_settings

from settings import settings

root_router = APIRouter(
    prefix="",
    tags=["root"],
    responses={404: {"description": "Not found"}},
)


@root_router.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@root_router.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)

# @root_router.post("/webhook")
# async def webhook(request: Request) -> None:
#     update = Update.model_validate(await request.json(), context={"bot": bot})
#     await dp.feed_update(bot, update)