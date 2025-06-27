from typing import Callable


class Context:
    """
    Basic Context class for handling contexts like menu, dialog, map, combat encounter, etc.
    :param parent_context (Context): The context instance from which this context is entered
    :param context_type (str): The type of the context ('map', 'inventory', 'dialog', etc.)
    :param context_data (dict): The data specific to this context
    """
    def __init__(self, parent_context, context_type: str, context_data: dict):
        self._parent_context = parent_context
        self.context_type: str = context_type
        self.context_data: dict = context_data
        self.entry_text: str = ''

    def get_context_type(self) -> str:
        return self.context_type

    def get_context_data(self) -> dict:
        return self.context_data

    def get_parent_context_type(self) -> str:
        return self._parent_context.get_context_type()

    def get_parent_context_data(self) -> dict:
        return self._parent_context.get_context_data()

    def print_entry_text(self) -> None:
        print(self.entry_text)

    def _generate_choice_handling(self) -> dict[str, Callable[[dict], bool]]:
        """
        Should be overridden in all subclasses of Context. This should produce a dictionary whose keys are the
        choices that are accepted. The corresponding values are functions that take in the current context data,
        do whatever is supposed to be done by that choice, and then return True if that choice is meant to break the
        context's loop and exit, False otherwise.
        :return:
        """
        return {}

    def _handle_choice(self, choice: str, choice_handler: dict[str, Callable[[dict], bool]]) -> bool:
        func = choice_handler[choice]
        return func(self.get_context_data())

    def print_choices(self) -> None:
        """
        Should be overridden in all subclasses of Context
        :return:
        """
        return

    def enter(self) -> bool:
        """
        Main loop of the context. Always called when a context is entered.
        :return: True
        """
        exit_loop = False
        choice_handler = self._generate_choice_handling()
        reprint_entry = True
        while not exit_loop:
            if reprint_entry:
                self.print_entry_text()
                print('\n')
                self.print_choices()
            choice_input = input().lower().strip()
            if choice_input in choice_handler:
                exit_loop = self._handle_choice(choice=choice_input, choice_handler=choice_handler)
                reprint_entry = True
            else:
                print('Input not recognized.')
                reprint_entry = False
        return True
