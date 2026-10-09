from abc import ABC, abstractmethod

class Context(ABC):

    def __init__(self, parent_context=None):
        self.parent_context = parent_context
        self.choices: dict[str, str] = {}

    @abstractmethod
    def print_entry_text(self):
        pass

    @abstractmethod
    def print_choices(self):
        pass

    @abstractmethod
    def handle_choice(self, choice: str) -> bool:
        pass

    @abstractmethod
    def generate_choices(self) -> dict[str, str]:
        pass

    def enter(self):
        self.print_entry_text()
        print('\n')
        exit_context = False
        while not exit_context:
            self.choices = self.generate_choices()
            self.print_choices()
            print('\n')
            choice = input('Please enter your choice: ').strip()
            if choice not in self.choices:
                print('Please enter a valid choice.')
                continue
            exit_context = self.handle_choice(choice)
