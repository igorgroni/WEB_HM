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