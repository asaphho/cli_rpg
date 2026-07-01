from abc import ABC, abstractmethod
from typing import Optional, Union


class Context(ABC):

    def __init__(self, name: str, context_type: str):
        self.name = name
        self.context_type = context_type
        self.data: Optional[dict] = None
        self.parent_context: Optional[Context] = None

    def get_name(self) -> str:
        return self.name

    def get_context_type(self) -> str:
        return self.context_type

    def get_data(self) -> Optional[dict]:
        return self.data

    def get_parent_context(self):
        return self.parent_context

    @abstractmethod
    def print_entry_text(self):
        pass

    @abstractmethod
    def handle_inputs(self):
        pass

    def enter(self):
        self.print_entry_text()
        exit_context = False
        while not exit_context:
            output: Union[Context, bool] = self.handle_inputs()
            if isinstance(output, Context):
                output.parent_context = self
                output.enter()
                self.print_entry_text()
            elif isinstance(output, bool):
                exit_context = output

