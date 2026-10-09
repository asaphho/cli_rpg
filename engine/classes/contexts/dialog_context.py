from engine.classes.contexts.context import Context
from typing import Callable


class DialogContext(Context):

    def __init__(self, parent_context: Context, data: dict, entry_text_generator: Callable[[dict], str],
                 dialog_choice_generator: Callable[[dict], dict[str, str]], dialog_choice_handler: Callable[[dict, str], bool],
                 dialog_choice_printer: Callable[[dict], None]):
        super().__init__(parent_context)
        self.data = data
        self.context_type = 'dialog'
        self.entry_text_generator = entry_text_generator
        self.dialog_choice_generator = dialog_choice_generator
        self.dialog_choice_handler = dialog_choice_handler
        self.dialog_choice_printer = dialog_choice_printer

    def print_entry_text(self):
        print(self.entry_text_generator(self.data))

    def generate_choices(self):
        return self.dialog_choice_generator(self.data)

    def print_choices(self):
        self.dialog_choice_printer(self.choices)

    def handle_choice(self, choice: str) -> bool:
        return self.dialog_choice_handler(self.data, choice)

