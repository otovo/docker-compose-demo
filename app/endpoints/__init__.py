from fastapi import APIRouter

from app.endpoints.health_check import health_router
from app.endpoints.index import index_router

base_router = APIRouter()
base_router.include_router(health_router)
base_router.include_router(index_router)

__all__ = ('base_router',)
