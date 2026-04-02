"""
API 路由模块
"""

import logging

from fastapi import APIRouter

from .accounts import router as accounts_router
from .registration import router as registration_router
from .settings import router as settings_router
from .email import router as email_services_router
from .payment import router as payment_router
from .upload.cpa_services import router as cpa_services_router
from .upload.sub2api_services import router as sub2api_services_router
from .upload.tm_services import router as tm_services_router

logger = logging.getLogger(__name__)


class _NoopAutoPatrolManager:
    async def _delayed_start_if_needed(self):
        return None

    def stop(self):
        return None


cliproxy_available = True
cliproxy_import_error = None
auto_patrol_manager = _NoopAutoPatrolManager()

try:
    from .cliproxy import router as cliproxy_router
    from .cliproxy import auto_patrol_manager as _cliproxy_auto_patrol_manager

    auto_patrol_manager = _cliproxy_auto_patrol_manager
except ModuleNotFoundError as exc:
    if exc.name != "aiohttp":
        raise
    cliproxy_available = False
    cliproxy_import_error = exc
    cliproxy_router = None
    logger.warning("Cliproxy routes disabled because optional dependency 'aiohttp' is not installed")

api_router = APIRouter()

# 注册各模块路由
api_router.include_router(accounts_router, prefix="/accounts", tags=["accounts"])
api_router.include_router(registration_router, prefix="/registration", tags=["registration"])
api_router.include_router(settings_router, prefix="/settings", tags=["settings"])
api_router.include_router(email_services_router, prefix="/email-services", tags=["email-services"])
api_router.include_router(payment_router, prefix="/payment", tags=["payment"])
api_router.include_router(cpa_services_router, prefix="/cpa-services", tags=["cpa-services"])
api_router.include_router(sub2api_services_router, prefix="/sub2api-services", tags=["sub2api-services"])
api_router.include_router(tm_services_router, prefix="/tm-services", tags=["tm-services"])
if cliproxy_router is not None:
    api_router.include_router(cliproxy_router, prefix="/cliproxy", tags=["cliproxy"])
