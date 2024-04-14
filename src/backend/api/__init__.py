from fastapi import APIRouter
from .auth import router as auth_router
from .orders import router as orders_router
from .role import router as role_router
from .projects import router as projects_router
from .order_status import router as order_status_router
from .comments import router as comment_router
from .user import router as user_router
from .letter import router as letter_router
from .admin import router as admin_router

router = APIRouter(prefix="/api/v1",)

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(orders_router)
router.include_router(role_router)
router.include_router(projects_router)
router.include_router(order_status_router)
router.include_router(comment_router)
router.include_router(letter_router)
router.include_router(admin_router)

