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
    """
    The read_root function is a function that returns the string &quot;Rest APIContacts v.0&quot;
        This is used to test if the API server is running correctly.

    :return: A dictionary with a message
    :doc-author: Trelent
    """
    return {"message": "Rest APIContacts v.1"}


@app.on_event("startup")
async def startup():
    """
    The startup function is called when the server starts up.
    It's a good place to initialize things that are needed by your application,
    such as databases or other resources.


    :return: The fastapilimiter instance
    :doc-author: Trelent
    """
    r = await redis.Redis(
        host="localhost", port=6379, db=0, encoding="utf-8", decode_responses=True
    )
    await FastAPILimiter.init(r)


@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def index():
    """
    The index function returns a JSON object with the key &quot;msg&quot; and value &quot;Hello World&quot;.


    :return: A dictionary, which will be converted to json
    :doc-author: Trelent
    """
    return {"msg": "Hello World"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    The add_process_time_header function is a middleware function that adds the time it took to process the request
    to the response headers. This can be useful for debugging and performance analysis.

    :param request: Request: Pass the request object to the function
    :param call_next: Call the next function in the pipeline
    :return: A response object with the my-process-time header added
    :doc-author: Trelent
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["My-Process-Time"] = str(process_time)
    return response


@app.post("/send-email")
async def send_in_background(background_tasks: BackgroundTasks, body: EmailSchema):
    """
    The send_in_background function sends an email in the background.

    :param background_tasks: BackgroundTasks: Add a task to the background tasks
    :param body: EmailSchema: Define the schema of the request body
    :return: A dict with a message
    :doc-author: Trelent
    """
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
    """
    The healthchecher function is used to check the health of the server.
    It returns a message if everything is working correctly.

    :param db: Session: Get the database session
    :return: A dictionary with a message
    :doc-author: Trelent
    """
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
