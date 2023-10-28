from dotenv import load_dotenv
import os

load_dotenv()

ENGINE = os.getenv("ENGINE")
NAME = os.getenv("NAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")


print(
    {
        ENGINE,
        NAME,
        USER,
        PASSWORD,
        HOST,
        PORT,
    }
)
