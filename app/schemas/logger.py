from pydantic import BaseModel, ConfigDict


class LoggerScheme(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    client_host: str
    request_method: str
    request_url: str
    status_code: int
    #response_body: dict