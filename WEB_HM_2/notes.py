import os



def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


class Notes:
    
    def __init__(self, note_id, title, content):
        self.note_id = note_id
        self.title = title
        self.content = content
        
        
class NoteManager:
    
    def __init__(self):
        self.notes_list = []
    
    def handle_title(self, note):
        new_title = input('Plese provide new title: ')
        note.title = new_title
    
    def handle_content(self, note):
        new_content = input('Plese provide new content: ')
        note.content = new_content #изменялся заголовок место содержания заметки
                    
    def add_note(self):
        note_id = len(self.notes_list)+1
        title = input('Please provide title: ')
        content = input('Please provide content: ')
        note = Notes(note_id, title, content)
        self.notes_list.append(note)
        print('Note added successfully.')
        
    def delete_note(self): #при неправильном вводе вызывалась рекурсия и при отсутствии заметок не выходило из функции
        if len(self.notes_list):
            try:
                note_id = int(input('Please provide note ID: '))
                note_found = False
                for note in self.notes_list:
                    if note_id == note.note_id:
                        note_found = True
                        self.notes_list.remove(note)
                        print('Note deleted successfully.')
                        break
                if not note_found:
                    print(f'Note with ID {note_id} does not exist. Please try again.')
                    self.delete_note()
            except ValueError:
                print('Note ID must be digits. Please try again.')
                self.delete_note()
        else:
            print('No notes.')
            

    def edit_note(self):
        while True:
            try:
                note_id = int(input('Please provide note ID: '))
                note_found = False
                for note in self.notes_list:
                    if note_id == note.note_id:
                        while True:
                            field_handlers = {'title': self.handle_title,
                                              'content': self.handle_content}
                            field = input('Please provide field to be changed: ').lower()
                            if field in field_handlers:
                                field_handlers[field](note)
                                print(f'{field.capitalize()} succesfully changed.')
                                break
                            else:
                                print(f'Field {field} does not exist. Please try again')
                        break
                    if not note_found:
                        print(f'Note with ID number {note_id} not found. Please try again.')
            except ValueError:
                    print('ID number must be digits. Please try again.')
            break        
        
    def search_note(self):
        search_query = input('Please provide search query: ')
        search_results = []
        for index, note in enumerate(self.notes_list):
            if (
                search_query.lower() in note.title.lower() # для поиска по заметке нужно note а не contact
                or search_query.lower() in note.content.lower()
            ):
                search_results.append((index, note))
        if search_results:
            print(f'Search results for "{search_query}":')
            for index, note in search_results:
                print(f'ID: {index+1}, Title: {note.title}, Content: {note.content}')
        else:
            print(f'No contacts found for "{search_query}".')    


def main():
    notemanager = NoteManager()

    while True:
        clear_console()  # Очистка консоли перед каждым выводом меню

        print("\n _____       _           _____                               \n|   | | ___ | |_  ___   |     | ___  ___  ___  ___  ___  ___ \n| | | || . ||  _|| -_|  | | | || .'||   || .'|| . || -_||  _|\n|_|___||___||_|  |___|  |_|_|_||__,||_|_||__,||_  ||___||_|  \n                                              |___|          ")
        print("1. Add a Note")
        print("2. Delete a Note")
        print("3. Edit a Note")
        print("4. Search for Notes")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            clear_console()
            notemanager.add_note()
            input("Press Enter to continue...")
        elif choice == "2":
            clear_console()
            notemanager.delete_note()
            input("Press Enter to continue...")
        elif choice == "3":
            clear_console()
            notemanager.edit_note()
            input("Press Enter to continue...")
        elif choice == "4":
            clear_console()
            notemanager.search_note()
            input("Press Enter to continue...")
        elif choice == "5":
            clear_console()
            print("Exiting Note Manager...")
            break
        else:
            clear_console()
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()