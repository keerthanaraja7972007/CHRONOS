import logging, time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.api.router import api_router
from backend.core.config import get_settings
from backend.core.errors import http_exception_handler, unhandled_exception_handler
from backend.core.logging import configure_logging
from starlette.exceptions import HTTPException as StarletteHTTPException
configure_logging(); settings=get_settings(); logger=logging.getLogger(__name__)
app=FastAPI(title="CHRONOS API",version="0.1.0",docs_url="/docs" if settings.environment != "production" else None)
app.add_middleware(CORSMiddleware,allow_origins=settings.allowed_origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.add_exception_handler(StarletteHTTPException,http_exception_handler); app.add_exception_handler(Exception,unhandled_exception_handler)
@app.middleware("http")
async def access_log(request: Request, call_next):
    started=time.perf_counter(); response=await call_next(request); logger.info("request_complete",extra={"path":request.url.path,"status":response.status_code,"duration_ms":round((time.perf_counter()-started)*1000,2)}); return response
@app.get("/health",tags=["health"])
def health(): return {"status":"ok","service":"chronos-api"}
app.include_router(api_router)
