import time

from fastapi import Request

from backend.app.core.logger import logger


async def log_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info({'method': request.method, 'url': request.url.path, 'process_time': process_time})
    return response
