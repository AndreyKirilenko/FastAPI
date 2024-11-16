from fastapi import APIRouter

from api.v1 import route_acceptance


api_router = APIRouter()
api_router.include_router(route_acceptance.router,prefix="",tags=["acceptance"])