from abc import ABC, abstractmethod
from typing import Callable, Optional


class Interaction(ABC):

    def __init__(self, source, target, interaction_type: str):
        self.source = source
        self.target = target
        self.interaction_type = interaction_type
        self.collectors: list[str] = []
        self.pending_modifiers: list[InteractionModifier] = []

    def get_source(self):
        return self.source

    def get_target(self):
        return self.target

    def get_interaction_type(self) -> str:
        return self.interaction_type

    def get_collectors(self) -> list[str]:
        return self.collectors

    def add_collector(self, collector: str):
        if collector not in self.get_collectors():
            self.collectors.append(collector)

    def sort_pending_modifiers(self):
        self.pending_modifiers.sort(key=lambda x: x.get_priority(), reverse=True)

    def add_modifiers(self, modifiers: list):
        self.pending_modifiers.extend(modifiers)

    def pass_through_screen(self, interaction_screen):
        for collector in self.collectors:
            modifiers: Optional[list[InteractionModifier]] = interaction_screen.get_modifiers_at_port(collector)
            if isinstance(modifiers, list):
                self.add_modifiers(modifiers)

    def apply_modifiers(self):
        self.sort_pending_modifiers()
        while self.pending_modifiers:
            modifier = self.pending_modifiers.pop(0)
            modifier_function = modifier.get_modifier_function()
            modifier_function(self)

    @abstractmethod
    def apply(self):
        pass


class InteractionModifier:

    def __init__(self, name: str, priority: int, modifier_function: Callable[[Interaction], None]):
        self.name = name
        self.priority = priority
        self.modifier_function = modifier_function

    def get_name(self) -> str:
        return self.name

    def get_priority(self) -> int:
        return self.priority

    def get_modifier_function(self) -> Callable[[Interaction], None]:
        return self.modifier_function
