from engine.contexts.context import Context


class PopupContext(Context):
    """
    Context for a text popup, like an item description. No where for the player to go but back. Just
    press enter to exit.
    :param parent_context (Context): The parent context
    :param display_text (str): The text to display in the popup
    :param context_data (dict): Not really needed
    """

    def __init__(self, parent_context: Context, display_text: str, context_data: dict = None):
        super().__init__(parent_context=parent_context,
                         context_type='popup',
                         context_data=context_data if context_data is not None else {})
        self.entry_text = display_text

    def enter(self, exit_choice: str = 'b') -> bool:
        self.print_entry_text()
        print('\n')
        hold = input('Press enter to continue.')
        return False
