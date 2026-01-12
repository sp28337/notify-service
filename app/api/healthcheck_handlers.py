import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.depends import get_healthcheck_service
from app.services import HealthcheckService

router = APIRouter(tags=["healthcheck-handlers"])
logger = logging.getLogger(__name__)


@router.get("/")
async def root():
    return {"status": "OK"}


@router.get("/check-mail-health")
async def check_mail_health(
    healthcheck_service: Annotated[
        HealthcheckService, Depends(get_healthcheck_service)
    ],
):
    try:
        await healthcheck_service.check_mail()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Notify Service unavailable",
        )
    return {"status": "OK"}


@router.get("/check-bot-health")
async def check_bot_health(
    healthcheck_service: Annotated[
        HealthcheckService, Depends(get_healthcheck_service)
    ],
):
    try:
        await healthcheck_service.check_bot()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Notify Bot unavailable",
        )
    return {"status": "OK"}
