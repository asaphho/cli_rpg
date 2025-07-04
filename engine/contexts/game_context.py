from engine.contexts.context import Context
from typing import Callable, TypeAlias

ChoiceHandlerD: TypeAlias = dict[str, tuple[str, Callable[[Context, Context], bool]]]
ChoiceHandlerDGenerator: TypeAlias = Callable[[dict], ChoiceHandlerD]
ChoiceHandler: TypeAlias = dict[str, Callable[[Context, Context], bool]]


def get_choice_handler_wo_display(choice_handler_w_display: ChoiceHandlerD) -> ChoiceHandler:
    handler = {}
    for choice in choice_handler_w_display:
        handler[choice] = choice_handler_w_display[choice][1]
    return handler


class GameContext(Context):
    """
    The Context object that serves as the top-level context for the game.
    """
    def __init__(self, game_state: dict,
                 entry_text_directory: dict[str, str],
                 entry_text_overrides: dict[str, str],
                 default_choice_handler_generator: ChoiceHandlerDGenerator,
                 choice_handler_overrides: dict[str, ChoiceHandlerDGenerator]):
        super().__init__(parent_context=None, context_type='game', context_data=game_state)
        self.entry_text_directory = entry_text_directory
        self.entry_text_overrides = entry_text_overrides
        self.default_choice_handler_generator = default_choice_handler_generator
        self.choice_handler_overrides = choice_handler_overrides
        self.choices: dict[str, str]

    def print_entry_text(self) -> None:
        game_state = self.context_data
        encounter_key = game_state['encounter_key']
        if encounter_key in self.entry_text_overrides:
            print(self.entry_text_overrides[encounter_key])
        else:
            print(self.entry_text_directory[encounter_key])

    def _generate_choice_handling(self) -> ChoiceHandler:
        game_state = self.context_data
        encounter_key: str = game_state['encounter_key']
        if encounter_key in self.choice_handler_overrides:
            choice_handler_w_display: ChoiceHandlerD = self.choice_handler_overrides[encounter_key](game_state)
        else:
            choice_handler_w_display: ChoiceHandlerD = self.default_choice_handler_generator(game_state)
        self.choices: dict[str, str] = {}
        for choice in choice_handler_w_display:
            self.choices[choice] = choice_handler_w_display[choice][0]
        return get_choice_handler_wo_display(choice_handler_w_display)

    def print_choices(self) -> None:
        # TODO: Add exit/save game choices
        for choice in sorted((self.choices.keys())):
            print(f'{choice}: {self.choices[choice]}')
