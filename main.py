from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from auth_routes import auth_router
from order_routes import order_router

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    print("❌ ERRO DE VALIDAÇÃO:")
    print(exc.errors())
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

app.include_router(auth_router)
app.include_router(order_router)