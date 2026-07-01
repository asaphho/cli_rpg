from engine.interactions.interaction import InteractionModifier
from typing import Optional


class InteractionScreen:

    def __init__(self):
        self.modifiers_by_port: dict[str, list[InteractionModifier]] = {}

    def get_modifiers_at_port(self, port: str) -> Optional[list[InteractionModifier]]:
        return self.modifiers_by_port.get(port, None)

    def add_modifier(self, port: str, modifier: InteractionModifier):
        if port not in self.modifiers_by_port:
            self.modifiers_by_port[port] = [modifier]
        else:
            self.modifiers_by_port[port].append(modifier)

    def remove_modifier(self, port: str, modifier: InteractionModifier):
        if modifier in self.get_modifiers_at_port(port):
            self.modifiers_by_port[port].remove(modifier)
