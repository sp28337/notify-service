import logging
from dataclasses import dataclass

from app.clients import BotClient, SMTPClient
from app.core.exceptions import MailError
from app.core.settings import Settings

logger = logging.getLogger(__name__)


@dataclass
class NotifyService:
    s: Settings
    bot_client: BotClient
    smtp_client: SMTPClient

    async def send_notifications(self, name: str, phone: str) -> bool:
        try:
            await self.smtp_client.send_email(name, phone)
            await self.bot_client.notify_success(name, phone)
        except MailError as e:
            logger.error("Mail error", exc_info=e)

            await self.bot_client.notify_error(
                error_type=type(e).__name__,
                error_details=str(e),
                name=name,
                phone=phone,
            )
            raise MailError(str(e))
