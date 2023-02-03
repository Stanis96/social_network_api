from fastapi import APIRouter

from . import user_router

router = APIRouter()
router.include_router(user_router.router, prefix="/users", tags=["users"])
