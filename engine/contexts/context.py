from engine.utils.choice_handler import ChoiceHandler


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
        return self._parent_context.get_context_type() if self._parent_context is not None else None

    def get_parent_context_data(self) -> dict:
        return self._parent_context.get_context_data() if self._parent_context is not None else {}

    def print_entry_text(self) -> None:
        print(self.entry_text)

    def _generate_choice_handling(self) -> ChoiceHandler:
        """
        Should be overridden in all subclasses of Context. This should produce a ChoiceHandler object, which maps the choices
        to functions that take in the current context instance and the parent context instance, do whatever is supposed
        to be done by that choice, and then return True if that choice is meant to break the context's loop and exit,
        False otherwise.
        :return: bool - True if it exits the context, False if it does not.
        """
        return ChoiceHandler()

    def _handle_choice(self, choice: str, choice_handler: ChoiceHandler) -> bool:
        func = choice_handler.get_executor(choice)
        return func(self, self._parent_context)

    def print_choices(self, choice_handler: ChoiceHandler) -> None:
        """
        Prints the choices
        :return:
        """
        choice_handler.print_choices()

    def enter(self, exit_choice: str = 'b') -> bool:
        """
        Main loop of the context. Always called when a context is entered.
        :return: True
        """
        exit_loop = False
        choice_handler = self._generate_choice_handling()
        rerun_entry = True
        while not exit_loop:
            if rerun_entry:
                choice_handler = self._generate_choice_handling()
                self.print_entry_text()
                print('\n')
                self.print_choices(choice_handler)
            choice_input = input().lower().strip()
            if choice_input == exit_choice:
                return False
            if choice_input in choice_handler:
                exit_loop = self._handle_choice(choice=choice_input, choice_handler=choice_handler)
                rerun_entry = True
            else:
                print('Input not recognized.')
                rerun_entry = False
        return True
