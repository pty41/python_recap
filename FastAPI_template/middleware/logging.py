import time
from fastapi import Request
import logging

logger = logging.getLogger("uvicorn.access")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round(time.time() - start, 4)
    logger.info(f"{request.method} {request.url.path} - {response.status_code} ({duration}s)")
    return response