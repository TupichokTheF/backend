from datetime import datetime, timezone

from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, DateTime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_seller: Mapped[bool]

    notifications: Mapped[list["EmailNotification"]] = relationship()

class EmailNotification(Base):
    __tablename__ = "email_notifications"

    notification_id: Mapped[int] = mapped_column(primary_key=True)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    title: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    users: Mapped["User"] = relationship(back_populates="notifications")

