from fastapi import APIRouter

from . import singin_router, user_router

router_api = APIRouter()
router_api.include_router(user_router.router, prefix="/users", tags=["users"])
router_api.include_router(singin_router.router, prefix="/singin", tags=["singin"])
