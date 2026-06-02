import time
import uuid

import structlog
from starlette.types import ASGIApp, Message, Receive, Scope, Send

REQUEST_ID_HEADER = "X-Request-ID"
_REQUEST_ID_HEADER_BYTES = REQUEST_ID_HEADER.lower().encode("latin-1")

logger = structlog.get_logger("app.request")


class RequestIdMiddleware:
    """Plain ASGI middleware: extracts/generates X-Request-ID, binds it to the
    structlog contextvar, echoes it on the response, and emits a structured
    per-request access log. Avoids BaseHTTPMiddleware's response buffering
    and background-task pitfalls.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = self._read_or_generate(scope)
        request_id_bytes = request_id.encode("latin-1")

        structlog.contextvars.bind_contextvars(request_id=request_id)
        start = time.perf_counter()
        status: int | None = None

        async def send_with_request_id(message: Message) -> None:
            nonlocal status
            if message["type"] == "http.response.start":
                status = message["status"]
                headers = [
                    (n, v) for n, v in message.get("headers", []) if n != _REQUEST_ID_HEADER_BYTES
                ]
                headers.append((_REQUEST_ID_HEADER_BYTES, request_id_bytes))
                message["headers"] = headers
            await send(message)

        try:
            await self.app(scope, receive, send_with_request_id)
        finally:
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            logger.info(
                "request",
                method=scope.get("method"),
                path=scope.get("path"),
                status=status,
                duration_ms=duration_ms,
            )
            structlog.contextvars.clear_contextvars()

    @staticmethod
    def _read_or_generate(scope: Scope) -> str:
        headers: list[tuple[bytes, bytes]] = scope.get("headers", [])
        for name, value in headers:
            if name == _REQUEST_ID_HEADER_BYTES:
                return value.decode("latin-1")
        return str(uuid.uuid4())
