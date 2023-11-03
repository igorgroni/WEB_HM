from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session

from database.db import get_db
from schemas import ResponseContact, ContactModel
from repository import contacts as repository_contacts
from fastapi_limiter.depends import RateLimiter
from services.auth import Auth as auth_service
from database.models import User
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter


router = APIRouter(prefix="/contacts", tags=["contacts"])

# limiter = FastAPILimiter(key_func=lambda _: "user_id", rate="10/minute")
# limiter = FastAPILimiter(key_func=lambda _: "user_id")


@router.get(
    "/all",
    response_model=List[ResponseContact],
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
# @limiter.limit("10/minute")
async def get_contacts(db: Session = Depends(get_db)):
    """
    The get_contacts function returns a list of contacts.
        ---
        get:
            summary: Get all contacts.
            description: Returns a list of all the contacts in the database.  This is an example of using Swagger to document your API endpoints and their functionality.

    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(db)
    return contacts


@router.get(
    "/{contact_id}",
    response_model=ResponseContact,
)
async def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    The get_contact function returns a contact by its ID.

    :param contact_id: int: Specify the id of the contact to be retrieved
    :param db: Session: Pass a database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ResponseContact, tags=["contacts"])
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    """
    The create_contact function creates a new contact in the database.
        It takes a ContactModel object as input and returns the newly created contact.

    :param body: ContactModel: Validate the request body
    :param db: Session: Pass the database session to the repository layer
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repository_contacts.create_contact(body, db)
    return contact


@router.put("/{contact_id}", response_model=ResponseContact)
async def update_contact(
    body: ContactModel, contact_id=int, db: Session = Depends(get_db)
):
    """
    The update_contact function updates a contact in the database.
        It takes an id and a body as input, and returns the updated contact.
        If no contact is found with that id, it raises an HTTPException.

    :param body: ContactModel: Get the data from the request body
    :param contact_id: Specify the contact to update
    :param db: Session: Get the database session
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ResponseContact)
async def del_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    The del_contact function deletes a contact from the database.
        It takes in an integer, which is the id of the contact to be deleted.
        If no such contact exists, it raises a 404 error.

    :param contact_id: int: Specify the contact to be deleted
    :param db: Session: Get the database session
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.get("/find/{query}", response_model=List[ResponseContact])
async def search_contact(query: str, db: Session = Depends(get_db)):
    """
    The search_contact function searches for a contact in the database.
        It takes a query string as an argument and returns all contacts that match the query.

    :param query: str: Search for a contact
    :param db: Session: Get the database session
    :return: A list of contacts that match the query
    :doc-author: Trelent
    """
    contacts = await repository_contacts.search_contacts(query, db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contacts


@router.get("/upcoming-birthdays/{days}", response_model=List[ResponseContact])
async def upcoming_birthdays(days: int, db: Session = Depends(get_db)):
    """
    The upcoming_birthdays function returns a list of contacts with upcoming birthdays.

    :param days: int: Specify the number of days to look ahead for upcoming birthdays
    :param db: Session: Pass the database session to the function
    :return: A list of contacts with upcoming birthdays
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_upcoming_birthdays(days, db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found"
        )
    return contacts
