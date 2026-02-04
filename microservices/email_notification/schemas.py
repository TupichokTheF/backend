from pydantic import BaseModel

class NotificationBase(BaseModel):
    receiver_id: int
    title: str
    message: str