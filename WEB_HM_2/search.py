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