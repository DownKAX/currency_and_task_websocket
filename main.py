import uvicorn
from fastapi import FastAPI, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError


from starlette.responses import JSONResponse

from app.api.endpoints.currency import currency
from app.api.auth.register import auth
from app.api.endpoints.tasks import task
from app.api.middleware.middleware import logging_middleware, logger

app = FastAPI()
app.include_router(currency)
app.include_router(auth)
app.include_router(task)
app.middleware('http')(logging_middleware)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    if exc._errors[0].get('loc')[0] == 'session_token':
        return JSONResponse({'error': 'No session token!'}, status_code=422)
    else:
        return await request_validation_exception_handler(request, exc)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Alarm! Global exception!")
    return JSONResponse(
        status_code=500,
        content={"error": "O-o-o-ps! Internal server error"}
    )

if __name__ == '__main__':
    uvicorn.run(app,
                host='127.0.0.1',
                port=80)