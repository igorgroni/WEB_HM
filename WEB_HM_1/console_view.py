from abstract_view import AbstractView


class ConsoleView(AbstractView):
    def show_contacts(self, contacts):
        print("Контакти:")
        for contact in contacts:
            print(contact)

    def show_notes(self, notes):
        print("Нотатки:")
        for note in notes:
            print(note)

    def show_commands(self, commands):
        print("Доступні команди:")
        for command in commands:
            print(command)
