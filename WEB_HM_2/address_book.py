import re
import pickle
import os.path
from datetime import datetime


class Contact:

    def __init__(self, contact_id, name, phone, birthday, email, address):
        self.contact_id = contact_id
        self.name = name
        self.phone = phone
        self.email = email
        self.birthday = birthday
        self.address = address

    @staticmethod
    def phone_check(phone):
        allowed_symbols = ['+', ' ', '(', ')', '-']
        for symbol in phone:
            if not symbol.isdigit() and symbol not in allowed_symbols:
                print('Invalid phone number format. Phone number should consist only digit numbers and allowed symbols. Please try again.')
                return False
        phone = phone.strip().removeprefix('+').replace('(', '').replace(')',
                                                                         '').replace('-', '').replace(' ', '')
        return phone

    @staticmethod
    def email_check(email):
        pattern = r'^([A-z0-9_-]+\.)*[A-z0-9_-]+@[A-z0-9_-]+(\.[A-z0-9_-]+)*\.[A-z]{2,6}$'
        if re.match(pattern, email):
            return True
        print('Invalid email address format. Please try again.')
        return False

    @staticmethod
    def birthday_check(birthday):
        pattern = r'^\d{2}-\d{2}-\d{4}$'
        if re.match(pattern, birthday):
            try:
                datetime.strptime(birthday, '%d-%m-%Y')
                return True
            except ValueError:
                print('Invalid date of birth format. Please provide dd-mm-yyyy.')
                return False
        print('Invalid date of birth format. Please provide dd-mm-yyyy.')
        return False


class Contactmanager:

    def __init__(self):
        self.contacts = []

    def add_contact(self):
        contact_id = len(self.contacts) + 1
        name = input('Please provide name: ')
        address = input('Please provide address: ')
        email = input('Please provide email: ')
        while Contact.email_check(email) == False:
            email = input('Please provide email address: ')
        birthday = input('Please provide date of birth: ')
        while Contact.birthday_check(birthday) == False:
            birthday = input('Please provide date of birth: ')
        phone = input('Please provide phone number: ')
        while Contact.phone_check(phone) == False:
            number = input('Please provide phone number: ')
        contact = Contact(contact_id, name, phone, address, email, birthday)
        self.contacts.append(contact)
        print('Contact successfully added!')

    def save_contacts(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.contacts, file)
        print('Contacts saved successfully.')

    def load_contacts(self, filename):
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                self.contacts = pickle.load(file)
            print('Contacts loaded successfully.')

    def search_contacts(self):
        search_query = input('Please provide search query: ')
        search_results = []
        for index, contact in enumerate(self.contacts):
            if (
                    search_query.lower() in contact.name.lower()
                    or search_query.lower() in contact.number.lower()
                    or search_query.lower() in contact.email.lower()
            ):
                search_results.append((index, contact))
        if search_results:
            print(f'Search results for "{search_query}":')
            for index, contact in search_results:
                print(f'ID: {index + 1}, Name: {contact.name}, Number: {contact.number}, Email: {contact.email}')
        else:
            print(f'No contacts found for "{search_query}".')

        def edit_contact(self):
            while True:
                try:
                    contact_id = int(input('Please provide contact ID: '))
                    contact_found = False
                    for index, contact in enumerate(self.contacts):
                        if contact_id == index + 1:
                            contact_found = True
                            while True:
                                field = input('Please provide field to be changed: ').lower()
                                field_handlers = {
                                    'name': self.handle_name,
                                    'address': self.handle_address,
                                    'email': self.handle_email,
                                    'birthday': self.handle_birthday,
                                    'number': self.handle_number,
                                }
                                if field in field_handlers:
                                    field_handlers[field](contact)
                                    print(f'{field.capitalize()} succesfully changed.')
                                    break
                                else:
                                    print(f'Field {field} does not exist. Please try again')
                            break
                    if not contact_found:
                        print(f'Contact with ID number {contact_id} not found. Please try again.')
                except ValueError:
                    print('ID number must be digits. Please try again.')
                break

    def delete_contact(self):
        try:
            contact_found = False
            contact_id = int(input('Please provide contact ID: '))
            for index, contact in enumerate(self.contacts):
                if contact_id == index + 1:
                    contact_found = True
                    del self.contacts[contact_id - 1]
                    print('Contact successfully deleted.')
                    break
            if not contact_found:
                print(f'Contact with ID {contact_id} does not exist. Please try again.')
                self.delete_contact()
        except ValueError:
            print('Contact ID must be digits. Please try again.')
            self.delete_contact()


def address_book():
    contact_manager = Contactmanager()
    filename = 'contacts.pkl'
    contact_manager.load_contacts(filename)
    while True:
        print('1. Add contact')
        print('8. Exit')
        choice = input('Please choose a function (1-8): ')
        if choice == '1':
            contact_manager.add_contact()
        elif choice == '8':
            contact_manager.save_contacts(filename)
            print('Exiting the program...')
            break



