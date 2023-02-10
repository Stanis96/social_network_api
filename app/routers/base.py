from fastapi import APIRouter

from . import post_router
from . import singin_router
from . import user_router


router_api = APIRouter()
router_api.include_router(user_router.router, prefix="/users", tags=["users"])
router_api.include_router(singin_router.router, prefix="/singin", tags=["singin"])
router_api.include_router(post_router.router, prefix="/posts", tags=["posts"])
