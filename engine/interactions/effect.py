from typing import Callable


class Effect:

    def __init__(self, effect_id: str, display_name: str, effect_type: str, effect_function: Callable):
        self.effect_id = effect_id
        self.display_name = display_name
        self.effect_type = effect_type
        self.effect_function = effect_function

