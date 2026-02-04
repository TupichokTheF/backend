from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.schemas.logger import LoggerScheme
from app.database import database
from app.models import Logger


class CustomLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        client_host = request.client.host
        method = request.method
        url = request.url.path
        response = await call_next(request)
        status_code = response.status_code
        log_data = LoggerScheme(
                                client_host=client_host,
                                request_method=method,
                                request_url=url,
                                status_code=status_code,
                            )
        await self._add_to_database(log_data)
        return response

    @staticmethod
    async def _add_to_database(log_data: LoggerScheme):
        async with database.session as session:
            log_model = Logger(**log_data.model_dump())
            session.add(log_model)
            await session.commit()