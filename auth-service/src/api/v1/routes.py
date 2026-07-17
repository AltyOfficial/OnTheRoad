from fastapi import APIRouter

from src.api.v1.users.router import router as user_router
from src.config.settings import settings


routers = APIRouter()
router_list = [
    user_router,
]

for router in router_list:
    routers.include_router(router, prefix=settings.app.PROJECT_V1_URL)