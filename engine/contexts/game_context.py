from engine.contexts.context import Context
from typing import Callable


class GameContext(Context):
    """
    The Context object that serves as the top-level context for the game.
    """
    def __init__(self, game_state: dict,
                 entry_text_directory: dict[str, str],
                 entry_text_overrides: dict[str, str],
                 default_choice_handler_generator: Callable[[dict], dict[str, Callable[[Context, Context], bool]]],
                 choice_handler_overrides: dict[str, dict[str, Callable[[Context, Context], bool]]]):
        super().__init__(parent_context=None, context_type='game', context_data=game_state)
        self.entry_text_directory = entry_text_directory
        self.entry_text_overrides = entry_text_overrides
        self.default_choice_handler_generator = default_choice_handler_generator
        self.choice_handler_overrides = choice_handler_overrides

    def print_entry_text(self) -> None:
        game_state = self.context_data
        encounter_key = game_state['encounter_key']
        if encounter_key in self.entry_text_overrides:
            print(self.entry_text_overrides[encounter_key])
        else:
            print(self.entry_text_directory[encounter_key])

    def _generate_choice_handling(self) -> dict[str, Callable[[Context, Context], bool]]:
        game_state = self.context_data
        encounter_key = game_state['encounter_key']
        if encounter_key in self.choice_handler_overrides:
            return self.choice_handler_overrides[encounter_key]
        else:
            return self.default_choice_handler_generator(game_state)

