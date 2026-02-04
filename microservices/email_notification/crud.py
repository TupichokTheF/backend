from microservices.email_notification import models
from microservices.email_notification.database import database, redis
from microservices.email_notification.schemas import NotificationBase

from sqlalchemy import select

class NotificationRepository:

    def get_user_by_email(self, email: str):
        query = select(models.User).filter_by(email=email)
        with database.session() as session:
            res = session.execute(query)
            return res.scalars().first()

    def add_notification(self, notification: NotificationBase):
        notification = models.EmailNotification(**notification.model_dump())
        with database.session() as session:
            session.add(notification)
            session.commit()
            session.refresh(notification)
            return notification
