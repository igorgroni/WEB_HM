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