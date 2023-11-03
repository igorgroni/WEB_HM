from fastapi_mail import ConnectionConfig
from pydantic import EmailStr
from conf.config import settings
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors

from services.auth import auth_service


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(
        "/Users/igorgroza/Desktop/WEB_HM/WEB_HM/WEB_HM_11/webhm11/templates"
    ),
)


async def send_email(email: EmailStr, username: str, host: str):
    """
    The send_email function sends an email to the user with a link to confirm their email address.
        The function takes in three arguments:
            1) An EmailStr object that contains the user's email address.
            2) A string containing the username of the user who is registering for an account.  This will be used in a template message sent to them via FastMail API.
            3) A string containing hostname of where this application is hosted, which will be used as part of a URL that users can click on to verify their account.

    :param email: EmailStr: Check if the email is valid
    :param username: str: Get the username of the user
    :param host: str: Pass the hostname of the server to be used in the email template
    :return: A coroutine object
    :doc-author: Trelent
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={
                "host": host,
                "username": username,
                "token": token_verification,
            },
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err:
        print(err)
