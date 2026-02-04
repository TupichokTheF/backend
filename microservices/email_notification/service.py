from microservices.email_notification.settings import  settings
from microservices.email_notification.crud import NotificationRepository
from microservices.email_notification.schemas import NotificationBase

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



class NotificationService:

    def __init__(self):
        self._notification_repo = NotificationRepository()

    def send_email(self, body: dict):
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        msg = MIMEMultipart()
        msg["From"] = settings.SMTP_EMAIL
        msg["To"] = body["receiver"]
        msg["Subject"] = body["title"]
        msg.attach(MIMEText(body["message"], "html"))
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.ehlo()
            server.login(settings.SMTP_EMAIL, settings.SMTP_PASS)
            print("lol")
            server.send_message(msg)
        if body["type"] == "notification":
            receiver = self._notification_repo.get_user_by_email(body["receiver"])
            notification = NotificationBase(receiver_id=receiver.user_id, title=body["title"], message=body["message"])
            self._notification_repo.add_notification(notification)