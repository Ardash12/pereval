from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from routes import routes
from core.db import SessionLocal


app = FastAPI()


@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    response = Response('Internet server error', status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

app.include_router(routes)