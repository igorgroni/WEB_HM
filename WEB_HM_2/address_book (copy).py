import re
import pickle
import os.path
import time
from datetime import datetime 

class Contact:
    
    def __init__(self, contact_id, name, address, email, birthday, number):
        self.contact_id = contact_id
        self.name = name
        self.address = address
        self.email = email
        self.birthday = birthday
        self.number = number
         
    @staticmethod
    def number_check(number):
        allowed_symbols = ['+', ' ', '(', ')', '-']
        for symbol in number:
            if not symbol.isdigit() and symbol not in allowed_symbols:
                print('Invalid phone number format. Phone number should consist only digit numbers and allowed symbols. Please try again.')
                return False
        number = number.strip().removeprefix('+').replace('(', '').replace(')', '').replace('-', '').replace(' ', '') 
        return number
    
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
    
    def handle_email(self, contact):
        new_email = input('Plese provide new email address: ')
        while not Contact.email_check(new_email):
            new_email = input('Plese provide new email address: ')
        contact.email = new_email

    def handle_number(self, contact):
        new_phone_number = input('Plese provide new phone number: ')
        while not Contact.number_check(new_phone_number):
            new_phone_number = input('Plese provide new phone number: ')
        contact.number = new_phone_number
        
    def handle_birthday(self, contact):
        new_birthday = input('Please provide new date of birthday: ')
        while not Contact.birthday_check(new_birthday):
            new_birthday = input('Please provide new date of birth: ')
        contact.birthday = new_birthday
    
    def handle_name(self, contact):
        new_name = input('Please provide new name: ')
        contact.name = new_name
    
    def handle_address(self, contact):
        new_address = input('Please provide new address: ')
        contact.address = new_address   
    
    def add_contact(self):
        contact_id = len(self.contacts) + 1
        name = input('Please provide name: ')
        address = input('Please provide address: ')
        email = input('Please provide email address: ')
        while Contact.email_check(email) == False:
            email = input('Please provide email address: ')
        birthday = input('Please provide date of birth: ')
        while Contact.birthday_check(birthday) == False:
            birthday = input('Please provide date of birth: ')
        number = input('Please provide phone number: ')
        while Contact.number_check(number) == False:
            number = input('Please provide phone number: ')
        contact = Contact(contact_id, name, address, email, birthday, number)
        self.contacts.append(contact)
        print('Contact successfully added!')  
        
    def delete_contact(self):
        try:
            contact_found = False
            contact_id = int(input('Please provide contact ID: '))
            for index, contact in enumerate(self.contacts):
                if contact_id == index+1:
                    contact_found = True
                    del self.contacts[contact_id-1]
                    print('Contact successfully deleted.')
                    break
            if not contact_found:
                print(f'Contact with ID {contact_id} does not exist. Please try again.')
                self.delete_contact()
        except ValueError:
            print('Contact ID must be digits. Please try again.')
            self.delete_contact()
            
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
            
    def display_contacts(self):
        print('Contact List:')
        if not self.contacts:
            print('No contacts found.')
        else:
            for index, contact in enumerate(self.contacts):
                print(f"ID: {index + 1}, Name: {contact.name}")
    
    def display_contact_information(self): 
        try:
            contact_id = int(input('Please provide contact ID: '))
            contact_found = False
            for index, contact in enumerate(self.contacts):
                if contact_id == index + 1:
                    contact_found = True
                    print(f'Contact information: \nID: {index + 1}, Name: {contact.name}, Address: {contact.address}, Email: {contact.email}, Birthday: {contact.birthday}, Number: {contact.number}')
                    break
            if not contact_found:
                print(f'Contact with ID {contact_id} does not exist. Please try again.')
                self.display_contact_information()
        except ValueError:
            print('Contact ID must be digits. Please try again.')
            self.display_contact_information()
            
    def get_upcoming_birthdays(self):
        while True:
            try:
                days = int(input('Please provide number of days: '))
                break
            except ValueError:
                print('Invalid input. Please enter a digit number of days.')
        upcoming_birthdays = []
        current_date = datetime.now()
        for contact in self.contacts:
            birthday = datetime.strptime(contact.birthday, '%d-%m-%Y')
            next_birthday = datetime(current_date.year, birthday.month, birthday.day)
            if next_birthday < current_date:
                next_birthday = next_birthday.replace(year=current_date.year + 1)
            if (next_birthday - current_date).days <= days:
                upcoming_birthdays.append(contact)
        print(f'Upcoming birthdays within {days} days:')
        for contact in upcoming_birthdays:
            print(f'Name: {contact.name}, Birthday: {contact.birthday}')
            
    def search_contacts(self):
        search_query = input('Please provide search query: ')
        search_results = []
        for index, contact in enumerate(self.contacts):
            if (
                search_query.lower() in contact.name.lower()
                or search_query.lower() in contact.number.lower()
                or search_query.lower() in contact.email.lower()
            ):
                search_results.append((index,contact))
        if search_results:
            print(f'Search results for "{search_query}":')
            for index, contact in search_results:
                print(f'ID: {index+1}, Name: {contact.name}, Number: {contact.number}, Email: {contact.email}')
        else:
            print(f'No contacts found for "{search_query}".')
            
    def save_contacts(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.contacts, file)
        print('Contacts saved successfully.')

    def load_contacts(self, filename):
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                self.contacts = pickle.load(file)
            print('Contacts loaded successfully.')

KEY_WORDS = {
    ('add', 'expanse', 'write'): Contactmanager.add_contact,
    ('delete', 'remove'): Contactmanager.delete_contact,
    ('edit', 'change'): Contactmanager.edit_contact,
    ('display', 'see', 'show'): Contactmanager.display_contacts,
    ('birthday', 'soon'): Contactmanager.get_upcoming_birthdays,
    ('save',): Contactmanager.save_contacts,
    ('search', 'find'): Contactmanager.search_contacts
}


def main():
    contact_manager = Contactmanager()
    filename = 'contacts.pkl'
    contact_manager.load_contacts(filename)
    while True:
        print('1. Add contact')
        print('2. Delete contact')
        print('3. Edit contact')
        print('4. Display contacts')
        print('5. Display contact information')
        print('6. Display upcoming birthdays')
        print('7. Search contacts')
        print('8. Exit')
        choice = input('Please choose a function (1-8) or write what you want: ')
        choice_el = choice.lower().split(' ')
        commands_list = []
        name_command = None
        for key in KEY_WORDS:
            for el in choice_el:
                if el in key:
                    commands_list.append(KEY_WORDS[key].__name__)
        if commands_list != None and len(commands_list) != 1:
            print('Which command should I execute?')
            for index in range(len(commands_list)):
                print(f'{index+1}. {commands_list[index]}')
            name_command = input('Choose command: ').lower()
        elif len(commands_list) == 1:
            name_command = commands_list[0]
        if choice == '1' or name_command == 'add_contact':
            contact_manager.add_contact()
        elif choice == '2' or name_command == 'delete_contact':
            contact_manager.delete_contact()
        elif choice == '3' or name_command == 'edit_contact':
            contact_manager.edit_contact()
        elif choice == '4' or name_command == 'display_contacts':
            contact_manager.display_contacts()
        elif choice == '5':
            contact_manager.display_contact_information()
        elif choice == '6' or name_command == 'get_upcoming_birthdays':
            contact_manager.get_upcoming_birthdays()
        elif choice == '7' or name_command == 'search_contacts':
            contact_manager.search_contacts()
        elif choice == '8' or name_command == 'save_contacts':
            contact_manager.save_contacts(filename)
            print('Exiting the program...')
            break
        else:
            print('Invalid choice. Please try again.')
        time.sleep(2)

if __name__ == '__main__':
    main()