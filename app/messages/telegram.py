from datetime import datetime


async def get_tg_error_message(
    error_type: str,
    error_details: str,
    timestamp: datetime,
    name: str | None = None,
    phone: str | None = None,
) -> str:

    message = f"""⚠️<b>ОШИБКА СИСТЕМЫ</b>
<b>Тип:</b> <code>{error_type}</code>
<b>Описание:</b> <code>{error_details}</code>
<b>Время:</b> <code>{timestamp}</code>"""

    if name and phone:
        message += f"""<b>Данные заявки:</b>
• Имя: <code>{name}</code>
• Телефон: <a tel:{phone}>{phone}</a>"""

    return message


async def get_tg_success_message(
    name: str,
    phone: str,
    timestamp: datetime,
) -> str:

    message = f"""✅ <b>НОВАЯ ЗАЯВКА</b>
<b>Имя:</b> <code>{name}</code>
<b>Телефон:</b> <a tel:{phone}>{phone}</a>
<b>Время:</b> <code>{timestamp}</code>"""

    return message
