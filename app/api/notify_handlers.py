import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.depends import get_notify_service
from app.core.exceptions import MailError
from app.schemas import ShortFormSchema
from app.services import NotifyService

router = APIRouter(tags=["notify-handlers"])
logger = logging.getLogger(__name__)


@router.post("/notify-mail/send-notifications")
async def send_notifications(
    body: ShortFormSchema,
    notify_service: Annotated[NotifyService, Depends(get_notify_service)],
):
    try:
        await notify_service.send_notifications(body.name, body.phone)
    except MailError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The messaging service is temporarily unavailable.",
        )

    return {"success": True}
