from engine.classes.contexts.context import Context


class TextReaderContext(Context):

    def __init__(self, parent_context: Context, text: str):
        super().__init__(parent_context)
        self.text = text
        self.context_type = 'text_reader'

    def print_entry_text(self):
        print(self.text)

    def generate_choices(self) -> dict[str, str]:
        return {}

    def handle_choice(self, choice: str) -> bool:
        return bool(choice)

    def print_choices(self):
        pass

    def enter(self):
        self.print_entry_text()
        print('\n')
        input('Press enter to continue...')
