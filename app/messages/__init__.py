from .email import get_html_message
from .telegram import get_tg_error_message, get_tg_success_message

__all__ = [
    "get_html_message",
    "get_tg_success_message",
    "get_tg_error_message",
]
