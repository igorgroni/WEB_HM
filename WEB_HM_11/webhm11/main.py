import time
import uvicorn

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Request,
    BackgroundTasks,
    File,
    UploadFile,
)
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from sqlalchemy import text
from sqlalchemy.orm import Session

from database.db import get_db
from routes import contacts
from routes import auth
from schemas import EmailSchema
from services.email import conf
import redis.asyncio as redis

from fastapi.middleware.cors import CORSMiddleware

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter


app = FastAPI()


origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Rest APIContacts v.1"}


@app.on_event("startup")
async def startup():
    r = await redis.Redis(
        host="localhost", port=6379, db=0, encoding="utf-8", decode_responses=True
    )
    await FastAPILimiter.init(r)


@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def index():
    return {"msg": "Hello World"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["My-Process-Time"] = str(process_time)
    return response


@app.post("/send-email")
async def send_in_background(background_tasks: BackgroundTasks, body: EmailSchema):
    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=[body.email],
        template_body={"fullname": "Billy Jones"},
        subtype=MessageType.html,
    )

    fm = FastMail(conf)

    background_tasks.add_task(
        fm.send_message, message, template_name="example_email.html"
    )

    return {"message": "email has been sent"}


@app.get("/api/healthchecker")
def healthchecher(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "Welcom to FastApi"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
