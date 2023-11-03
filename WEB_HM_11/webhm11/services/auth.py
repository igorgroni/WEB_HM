from typing import Optional

from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import timedelta, datetime
from sqlalchemy.orm import Session

from database.db import get_db
from repository import users as repositroy_users
from conf.config import settings


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

    def verify_password(self, plain_password, hashed_password):
        """
        The verify_password function takes a plain-text password and hashed
        password as arguments. It then uses the CryptContext instance to verify that
        the plain-text password matches the hashed one. If it does, it returns True; if not, False.

        :param self: Represent the instance of the class
        :param plain_password: Compare the password entered by the user to a hashed version of it
        :param hashed_password: Compare the password that is being entered with the hashed password in the database
        :return: True if the password is correct and false if it’s not
        :doc-author: Trelent
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        The get_password_hash function takes a password and returns the hashed version of it.
        The hashing algorithm is defined in the settings file, which defaults to Argon2.

        :param self: Represent the instance of the class
        :param password: str: Get the password from the user
        :return: A hash of the password
        :doc-author: Trelent
        """
        return self.pwd_context.hash(password)

    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        """
        The create_access_token function creates a new access token.
            The function takes in the data to be encoded, and an optional expires_delta parameter.
            If no expires_delta is provided, the default value of 15 minutes will be used.
            The function then encodes the data using JWT with our SECRET_KEY and ALGORITHM.

        :param self: Represent the instance of the class
        :param data: dict: Pass the user information that will be encoded in the jwt
        :param expires_delta: Optional[float]: Set the expiration time of the token
        :return: A jwt token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"}
        )
        encoded_access_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        print(encoded_access_token)
        return encoded_access_token

    async def create_refresh_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        """
        The create_refresh_token function creates a refresh token.
            Args:
                data (dict): The payload to be encoded in the JWT.
                expires_delta (Optional[float]): A timedelta object representing the expiration of the token.

        :param self: Represent the instance of the class
        :param data: dict: Pass in the user's id and username
        :param expires_delta: Optional[float]: Set the expiration time of the refresh token
        :return: A jwt encoded with the refresh token data
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"}
        )
        encoded_refresh_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """
        The decode_refresh_token function is used to decode the refresh token.
        The function will raise an HTTPException if the refresh token is invalid or expired.

        :param self: Represent the instance of the class
        :param refresh_token: str: Pass in the refresh token
        :return: The email of the user
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(
                refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            if payload["scope"] == "refresh_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ):
        """
        The get_current_user function is a dependency that will be used in the
            protected endpoints. It takes an OAuth2 token as input and returns the user
            associated with that token. If no user is found, it raises an exception.

        :param self: Access the class attributes
        :param token: str: Get the token from the authorization header
        :param db: Session: Pass the database session to the function
        :return: The user object
        :doc-author: Trelent
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "access_token":
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception

        user = await repositroy_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user

    def create_email_token(self, data: dict):
        """
        The create_email_token function creates a token that is used to verify the user's email address.
        The token contains the following information:
            - iat (issued at): The time when the token was created.
            - exp (expiration): The time when this token will expire and no longer be valid. This is set to 3 days from now, but can be changed in settings.py if desired.

        :param self: Represent the instance of the class
        :param data: dict: Pass in the data that will be encoded into the token
        :return: A token that is encoded using the jwt library
        :doc-author: Trelent
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=3)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    async def get_email_from_token(self, token: str):
        """
        The get_email_from_token function takes a token as an argument and returns the email address associated with that token.
        The function first tries to decode the token using jwt.decode(). If successful, it will return the email address from
        the payload of the decoded JWT. If unsuccessful, it will raise an HTTPException.

        :param self: Represent the instance of the class
        :param token: str: Pass the token to the function
        :return: The email address that is associated with the token
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid token for email verification",
            )


auth_service = Auth()
