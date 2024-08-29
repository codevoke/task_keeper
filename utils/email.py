import os
import asyncio

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib as smtp

from .email_letter_template import render_template


SMTP_SERVER = "smtp.yandex.ru"
SMTP_PORT = 465
SMTP_LOGIN = "durak2.online@yandex.ru"
SMTP_PASSWORD = "nrddetakhuebpakk"

URL = "https://humble-umbrella-v4p456w4667cjw-5000.app.github.dev"


def send_email_async(email: str, username: str, code: str):
    global SMTP_LOGIN, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT, LOGO_PATH, URL

    message = MIMEMultipart("alternative")
    message["Subject"] = "Подтвердите ваш адрес электронной почты"
    message["From"] = SMTP_LOGIN
    message["To"] = email

    text = "ОТКРОЙ ПИСЬМО, МЫ ЧЕ ЗРЯ ЕГО ВЕРСТАЛИ!? В НЕМ ТВОЙ КОД"
    html = render_template(username, code, URL)

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    asyncio.run(smtp.send(
        message,
        hostname=SMTP_SERVER,
        port=SMTP_PORT,
        username=SMTP_LOGIN,
        password=SMTP_PASSWORD,
        use_tls=True,
    ))
