from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.chat.router import router as chat_router
from src.todos.router import router as todos_router
from src.users.router import router as users_router
from src.ws import router as ws_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ws_router)
app.include_router(todos_router)
app.include_router(users_router)
app.include_router(chat_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = {}
    for error in exc.errors():
        field_name = error["loc"][-1]
        error_msg = error["msg"]
        if error_msg.startswith("Value error, "):
            error_msg = error_msg[13:]
        if field_name not in errors:
            errors[field_name] = []
        errors[field_name].append(error_msg)

    return JSONResponse(status_code=400, content={"errors": errors})


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "hello world"}
