from datetime import datetime


async def get_html_message(
    client_name: str,
    client_phone: str,
    date: datetime,
) -> str:

    message = f"""<html>
                 <body style="font-family: Arial;">
                   <h2 style="color: #164e3b;">Новая заявка от клиента</h2>
                   <p>
                     <strong>Имя:</strong> {client_name}
                   </p>
                   <p>
                     <strong>Телефон:</strong> 
                     <a href="tel:{client_phone}">{client_phone}</a>
                   </p>
                   <p>
                     <strong>
                       Время:
                     </strong> {date}
                   </p>
                 </body>
               </html>
            """
    return message
