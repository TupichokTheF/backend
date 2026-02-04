from pydantic import BaseModel, ConfigDict

from datetime import datetime

class TokenBase(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class RefreshTokenData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    refresh_token: str
    username: str
    expired_at: datetime