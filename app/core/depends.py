from typing import Annotated

import httpx
from fastapi import Depends

from app.clients import BotClient, SMTPClient
from app.core.settings import settings
from app.services import HealthcheckService, NotifyService


async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()


async def get_bot_client(
    async_client: Annotated[httpx.AsyncClient, Depends(get_async_client)],
) -> BotClient:
    return BotClient(s=settings, async_client=async_client)


async def get_smtp_client() -> SMTPClient:
    return SMTPClient(
        host=settings.mail.smtp_host,
        port=settings.mail.smtp_port,
        timeout=settings.mail.timeout,
        use_tls=settings.mail.smtp_secure,
        password=settings.mail.password,
        admin_mail=settings.mail.admin,
        destination_mail=settings.mail.user,
    )


async def get_notify_service(
    bot_client: Annotated[BotClient, Depends(get_bot_client)],
    smtp_client: Annotated[SMTPClient, Depends(get_smtp_client)],
) -> NotifyService:
    return NotifyService(
        s=settings,
        bot_client=bot_client,
        smtp_client=smtp_client,
    )


async def get_healthcheck_service(
    bot_client: Annotated[BotClient, Depends(get_bot_client)],
    smtp_client: Annotated[SMTPClient, Depends(get_smtp_client)],
) -> HealthcheckService:
    return HealthcheckService(
        s=settings,
        bot_client=bot_client,
        smtp_client=smtp_client,
    )
