class MailError(Exception):
    """Base SMTP error"""


class MailConnectionError(MailError):
    pass


class MailAuthError(MailError):
    pass


class MailSendError(MailError):
    pass


class HealthcheckError(Exception):
    """Bse Healthcheck error"""


class BotHealthcheckError(HealthcheckError):
    pass


class MailHealthcheckError(HealthcheckError):
    pass
