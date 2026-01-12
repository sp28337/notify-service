import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from app.core.exceptions import (
    HealthcheckError,
    MailAuthError,
    MailConnectionError,
    MailSendError,
)
from app.messages import get_html_message

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SMTPClient:
    host: str
    port: int
    use_tls: bool
    password: str
    admin_mail: str
    destination_mail: str
    timeout: int

    async def send_email(self, client_name: str, client_phone: str) -> None:
        try:
            smtp = aiosmtplib.SMTP(
                hostname=self.host,
                port=self.port,
                use_tls=self.use_tls,
                timeout=self.timeout,
            )
            await smtp.connect()
            await smtp.login(self.admin_mail, self.password)

            html = await get_html_message(
                client_name,
                client_phone,
                date=datetime.now(timezone(timedelta(hours=3))).strftime(
                    "%d.%m.%Y %H:%M:%S"
                ),
            )

            message = MIMEMultipart("alternative")
            message["From"] = self.admin_mail
            message["To"] = self.destination_mail
            message["Subject"] = f"Новая заявка от: {client_name}"
            message.attach(MIMEText(html, "html", "utf-8"))

            await smtp.send_message(message)
            await smtp.quit()
            logger.info("SMTP sent successfully")
        except aiosmtplib.SMTPAuthenticationError as e:
            raise MailAuthError("SMTP authentication failed") from e

        except aiosmtplib.SMTPConnectError as e:
            raise MailConnectionError("SMTP connection failed") from e

        except aiosmtplib.SMTPException as e:
            raise MailSendError("SMTP send failed") from e

    async def ping(self) -> None:
        try:
            smtp = aiosmtplib.SMTP(
                hostname=self.host,
                port=self.port,
                use_tls=self.use_tls,
                timeout=self.timeout,
            )
            await smtp.connect()
            await smtp.login(self.admin_mail, self.password)
            await smtp.noop()  # check connection
            await smtp.quit()
        except Exception as e:
            raise HealthcheckError(f"SMTP unavailable: {e}") from e
