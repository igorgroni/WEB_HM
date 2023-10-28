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
    contacts = await repository_contacts.get_contacts(db)
    return contacts


@router.get(
    "/{contact_id}",
    response_model=ResponseContact,
)
async def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ResponseContact, tags=["contacts"])
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.create_contact(body, db)
    return contact


@router.put("/{contact_id}", response_model=ResponseContact)
async def update_contact(
    body: ContactModel, contact_id=int, db: Session = Depends(get_db)
):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ResponseContact)
async def del_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.get("/find/{query}", response_model=List[ResponseContact])
async def search_contact(query: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.search_contacts(query, db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contacts


@router.get("/upcoming-birthdays/{days}", response_model=List[ResponseContact])
async def upcoming_birthdays(days: int, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_upcoming_birthdays(days, db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found"
        )
    return contacts
