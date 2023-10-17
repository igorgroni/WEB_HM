from sqlalchemy.orm import Session
from sqlalchemy import or_
from database.models import Contact
from schemas import ContactModel
from datetime import timedelta, datetime


async def get_contacts(db: Session):
    contacts = db.query(Contact).all()
    return contacts


async def get_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def create_contact(body: ContactModel, db: Session):
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone=body.phone,
        birthday=body.birthday,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        contact.first_name = (body.first_name,)
        contact.last_name = (body.last_name,)
        contact.email = (body.email,)
        contact.phone = (body.phone,)
        contact.birthday = body.birthday
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(query: str, db: Session):
    contacts = (
        db.query(Contact)
        .filter(
            or_(
                Contact.first_name.contains(query),
                Contact.last_name.contains(query),
                Contact.email.contains(query),
            )
        )
        .all()
    )
    return contacts


async def get_upcoming_birthdays(days: int, db: Session):
    request = []
    all_contacts = db.query(Contact).all()
    for contact in all_contacts:
        if (
            timedelta(0)
            <= (
                (contact.birthday.replace(year=int((datetime.now()).year)))
                - datetime.now().date()
            )
            <= timedelta(days)
        ):
            request.append(contact)

    return request
