from abc import ABC, abstractmethod

class Context(ABC):

    def __init__(self, parent_context=None):
        self.parent_context = parent_context

    @abstractmethod
    def print_entry_text(self):
        pass

    @abstractmethod
    def print_choices(self):
        pass

    @abstractmethod
    def handle_choice(self, choice) -> bool:
        pass

    @abstractmethod
    def validate_choice(self) -> bool:
        pass

    def enter(self):
        self.print_entry_text()
        print('\n')
        exit_context = False
        while not exit_context:
            self.print_choices()
            print('\n')
            choice = input('Please enter your choice: ').strip()
            if not self.validate_choice():
                print('Please enter a valid choice.')
                continue
            exit_context = self.handle_choice(choice)
