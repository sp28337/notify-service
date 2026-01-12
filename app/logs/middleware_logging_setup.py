import logging
import time

from fastapi import Request

logger = logging.getLogger("app.http")


async def logging_middleware(request: Request, call_next):
    start_time = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        logger.exception(
            "HTTP request failed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client": request.client[0] if request.client else "unknown",
            },
        )
        raise

    duration = round((time.perf_counter() - start_time) * 1000, 2)

    logger.info(
        "HTTP request",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration,
            "client": request.client[0] if request.client else "unknown",
        },
    )

    return response
