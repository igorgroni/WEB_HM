from typing import List

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    Security,
    BackgroundTasks,
    Request,
    File,
    UploadFile,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from database.db import get_db
from schemas import UserModel, ResponseUser, TokenModel
from repository import users as repository_users
from services.auth import auth_service
from services.email import send_email
from schemas import UserModel, TokenModel, RequestEmail, ResponseModel
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url


router = APIRouter(prefix="/auth")
security = HTTPBearer()


@router.post(
    "/signup", response_model=ResponseUser, status_code=status.HTTP_201_CREATED
)
async def signup(body: UserModel, db: Session = Depends(get_db)):
    """
    The signup function creates a new user in the database.
    It takes a UserModel object as input and returns an HTTP response with the newly created user's information.
    If there is already an account associated with that email address, it will return a 409 Conflict error.

    :param body: UserModel: Validate the data that is passed in
    :param db: Session: Get the database session
    :return: A dictionary with the user and a detail message
    :doc-author: Trelent
    """
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    BackgroundTasks.add_task(
        send_email, new_user.email, new_user.username, Request.base_url
    )
    return {
        "user": new_user,
        "detail": "User successfully created. Check your email for confirmation.",
    }


@router.post("/login", response_model=TokenModel)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    The login function is used to authenticate a user.
        It takes in the username and password of the user, and returns an access token if successful.
        The access token can be used to make authenticated requests for data from our API.

    :param body: OAuth2PasswordRequestForm: Get the username and password from the request body
    :param db: Session: Pass the database session to the function
    :return: A dictionary with the access token, refresh token and a bearer type
    :doc-author: Trelent
    """
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )
    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed"
        )
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    access_token = await auth_service.create_access_token(
        data={"sub": user.email}, expires_delta=3600
    )
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/refresh_token", response_model=TokenModel)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    """
    The refresh_token function is used to refresh the access token.
        The function will check if the user has a valid refresh token and then return a new access_token.
        If there is no valid refresh_token, it will raise an HTTPException with status code 401 (Unauthorized).

    :param credentials: HTTPAuthorizationCredentials: Get the token from the request header
    :param db: Session: Get a database session
    :param : Get the current user
    :return: A dictionary with the access_token, refresh_token and token type
    :doc-author: Trelent
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/confirmed_email/{token}")
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
    The confirmed_email function is used to confirm a user's email address.
        It takes the token from the URL and uses it to get the user's email address.
        Then, it gets that user from our database and checks if their account has already been confirmed.
        If so, we return a message saying as much; otherwise, we update their account in our database with confirmed=True.

    :param token: str: Get the token from the url
    :param db: Session: Pass the database session to the function
    :return: A message that the email is confirmed
    :doc-author: Trelent
    """
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error"
        )
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post("/request_email")
async def request_email(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    The request_email function is used to send an email to the user with a link
    to confirm their account. The function takes in a RequestEmail object, which
    contains the user's email address. It then checks if that email address exists
    in our database and if it does, sends an email containing a confirmation link.

    :param body: RequestEmail: Get the email from the request body
    :param background_tasks: BackgroundTasks: Add a task to the background tasks queue
    :param request: Request: Get the base_url of the application
    :param db: Session: Get access to the database
    :param : Get the user's email, username and base url
    :return: A dictionary with a message
    :doc-author: Trelent
    """
    user = await repository_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(
            send_email, user.email, user.username, request.base_url
        )
    return {"message": "Check your email for confirmation."}


@router.post("/update-avatar/{user_id}", response_model=ResponseModel, tags=["user"])
async def update_user_avatar(
    user_id: int,
    avatar: UploadFile = File(...),
):
    """
    The update_user_avatar function updates the user's avatar.

    :param user_id: int: Specify the user id of the user whose avatar is being updated
    :param avatar: UploadFile: Upload the avatar image to cloudinary
    :param : Get the user id from the request
    :return: A dictionary with the message and avatar_url keys
    :doc-author: Trelent
    """
    # Отримайте зображення з запиту та завантажте його в Cloudinary
    upload_result = upload(avatar.file)

    # Отримайте URL завантаженого аватара з Cloudinary
    avatar_url, options = cloudinary_url(
        upload_result["public_id"],
        format=upload_result["format"],
        width=150,  # розмір вашого аватара
        height=150,
    )
    return {"message": "Аватар користувача успішно оновлено", "avatar_url": avatar_url}
