import logging
from dataclasses import dataclass

from app.clients import BotClient, SMTPClient
from app.core.exceptions import (
    BotHealthcheckError,
    HealthcheckError,
    MailHealthcheckError,
)
from app.core.settings import Settings

logger = logging.getLogger(__name__)


@dataclass
class HealthcheckService:
    s: Settings
    bot_client: BotClient
    smtp_client: SMTPClient

    async def check_bot(self) -> bool:
        try:
            await self.bot_client.ping()
        except HealthcheckError as e:
            logger.error("Bot Healthcheck error", exc_info=e)
            raise BotHealthcheckError(str(e))

    async def check_mail(self) -> bool:
        try:
            await self.smtp_client.ping()
        except HealthcheckError as e:
            logger.error("Mail Healthcheck error", exc_info=e)
            raise MailHealthcheckError(str(e))
