import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import httpx

from app.core.settings import Settings
from app.messages import get_tg_error_message, get_tg_success_message

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BotClient:
    s: Settings
    async_client: httpx.AsyncClient

    async def notify_success(self, name: str, phone: str):
        timestamp = datetime.now(timezone(timedelta(hours=3))).strftime(
            "%d.%m.%Y %H:%M:%S"
        )
        message = await get_tg_success_message(
            name=name,
            phone=phone,
            timestamp=timestamp,
        )

        async with self.async_client as client:
            await client.post(
                self.s.bot.notify_url,
                json={
                    "message": message,
                },
            )
        logger.info("Bot successfully sent message")

    async def notify_error(
        self,
        error_type: str,
        error_details: str,
        name: str | None = None,
        phone: str | None = None,
    ) -> None:
        timestamp = datetime.now(timezone(timedelta(hours=3))).strftime(
            "%d.%m.%Y %H:%M:%S"
        )

        html = await get_tg_error_message(
            error_type=error_type,
            error_details=error_details,
            name=name,
            phone=phone,
            timestamp=timestamp,
        )

        async with self.async_client as client:
            await client.post(
                self.s.bot.notify_url,
                json={
                    "message": html,
                },
            )

    async def ping(self) -> None:
        async with self.async_client as client:
            res = await client.get(self.s.bot.ping_url)
            if res.status_code == 200:
                return {"status": "bot is working"}
            else:
                return {"status": "error"}
