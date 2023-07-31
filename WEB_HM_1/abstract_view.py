from abc import ABC, abstractmethod


class AbstractView(ABC):
    @abstractmethod
    def show_contacts(self, contacts):
        pass

    @abstractmethod
    def show_notes(self, notes):
        pass

    @abstractmethod
    def show_commands(self, commands):
        pass
