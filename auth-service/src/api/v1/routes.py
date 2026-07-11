from fastapi import APIRouter

from src.config.settings import settings


routers = APIRouter()
router_list = [
]

for router in router_list:
    routers.include_router(router, prefix=settings.app.PROJECT_V1_URL)