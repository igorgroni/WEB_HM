from sqlalchemy.orm import Session
from sqlalchemy import or_
from database.models import Contact
from schemas import ContactModel
from datetime import timedelta, datetime


async def get_contacts(db: Session):
    """
    The get_contacts function returns a list of all contacts in the database.


    :param db: Session: Pass the database session to the function
    :return: A list of contact objects
    :doc-author: Trelent
    """
    contacts = db.query(Contact).all()
    return contacts


async def get_contact(contact_id: int, db: Session):
    """
    The get_contact function takes in a contact_id and a database session.
    It then queries the database for the contact with that id, and returns it.

    :param contact_id: int: Specify the contact id of the contact to be retrieved
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def create_contact(body: ContactModel, db: Session):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Get the data from the request body
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
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
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated information for the specified Contact.

    :param contact_id: int: Identify the contact that will be updated
    :param body: ContactModel: Pass in the contact information that will be updated
    :param db: Session: Access the database
    :return: The contact object
    :doc-author: Trelent
    """
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
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            db (Session): A session object for interacting with the database.

    :param contact_id: int: Specify the id of the contact to be removed
    :param db: Session: Pass in the database session object
    :return: The contact that was deleted
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(query: str, db: Session):
    """
    The search_contacts function takes a query string and returns all contacts that match the query.
    The search is case insensitive, so if you search for &quot;john&quot; it will return both &quot;John&quot; and &quot;john&quot;.
    It also searches across first_name, last_name, email.

    :param query: str: Search for a contact by first name, last name or email
    :param db: Session: Pass the database session to the function
    :return: A list of contact objects
    :doc-author: Trelent
    """
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
    """
    The get_upcoming_birthdays function takes in a number of days and a database session.
    It then queries the database for all contacts, and checks if their birthday is within the next x days.
    If it is, it adds them to an array which will be returned at the end of this function.

    :param days: int: Specify the number of days in advance you want to see birthdays for
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
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
