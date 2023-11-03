from libgravatar import Gravatar
from sqlalchemy.orm import Session

from database.models import User
from schemas import UserModel


async def get_user_by_email(
    email: str,
    db: Session,
) -> User:
    """
    The get_user_by_email function takes an email and a database session,
    and returns the user with that email. If no such user exists, it returns None.

    :param email: str: Specify the email of the user that we want to get
    :param db: Session: Pass the database session to the function
    :param : Get the user by email
    :return: The first user found with the email provided
    :doc-author: Trelent
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.

    :param body: UserModel: Specify the type of data that will be passed into the function
    :param db: Session: Pass a database session to the function
    :return: The newly created user
    :doc-author: Trelent
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Find the user in the database
    :param token: str | None: Store the token in the database
    :param db: Session: Commit the changes to the database
    :return: None
    :doc-author: Trelent
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes an email and a database session as arguments.
    It then gets the user from the database using that email, sets their confirmed field to True,
    and commits those changes to the database.

    :param email: str: Pass in the email address of the user who is trying to confirm their account
    :param db: Session: Access the database
    :return: None
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()
