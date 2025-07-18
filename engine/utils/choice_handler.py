from typing import Callable


class ChoiceHandler:
    """
    Object to handle choices made in a context
    """
    def __init__(self, reserved_choices: list[tuple[str, str]] = None):
        self._choices: dict[str, tuple[str, Callable]] = {}
        self._max_choice_number: int = 0
        self._choice_letters: list[str] = [tup[0].lower().strip() for tup in reserved_choices] \
            if reserved_choices else []
        self._display_texts: list[str] = [tup[1].strip() for tup in reserved_choices] if reserved_choices else []
        if any([(not letter.isalpha()) or (len(letter) != 1) for letter in self._choice_letters]):
            raise ValueError('Invalid reserved choice letter found.')
        if any([text.strip() == '' for text in self._display_texts]):
            raise ValueError('Empty display text detected.')
        if len(set(self._choice_letters)) < len(self._choice_letters):
            raise ValueError('Duplicate choice letter detected.')
        if len(set(self._display_texts)) < len(self._display_texts):
            raise ValueError('Duplicate display text detected.')
        self.reserved_choices = {}
        for tup in reserved_choices:
            self.reserved_choices[tup[0].lower().strip()] = tup[1].strip()

    def add_choice(self, executor: Callable, display_text: str, choice_letter: str = None) -> None:
        if display_text.strip() in self._display_texts:
            raise ValueError(f'Display text "{display_text.strip()}" already taken.')
        if display_text.strip() == '':
            raise ValueError('Display text cannot be blank.')
        if choice_letter is not None:
            if choice_letter.lower().strip() in self._choice_letters:
                raise ValueError(f'Choice letter {choice_letter.lower().strip()} is taken.')
            if (not choice_letter.isalpha()) or (len(choice_letter.strip()) != 1):
                raise ValueError('Choice letter must be exactly one letter. No digits or special characters.')
            self._choice_letters.append(choice_letter.lower().strip())
            self._display_texts.append(display_text.strip())
            self._choices[choice_letter.lower().strip()] = (display_text.strip(), executor)
        else:
            assigned_integer = self._max_choice_number + 1
            self._max_choice_number = assigned_integer
            self._display_texts.append(display_text.strip())
            self._choices[str(assigned_integer)] = (display_text.strip(), executor)

    def get_executor(self, choice: str) -> Callable:
        if choice not in self._choices:
            raise ValueError('Executor does not exist. If it is a reserved choice, this object does not handle it.')
        return self._choices[choice][1]

    def print_choices(self) -> None:
        numbered_choices: list[int] = list(range(1, self._max_choice_number + 1))
        for n in numbered_choices:
            display: str = self._choices[str(n)][0]
            print(f'{n}. {display}')
        non_reserved_letters: list[str] = [letter for letter in self._choice_letters if letter not in
                                           self.reserved_choices.keys()]
        for letter in non_reserved_letters:
            display: str = self._choices[letter][0]
            print(f'{letter}. {display}')
        for reserved in self.reserved_choices:
            print(f'{reserved}. {self.reserved_choices[reserved]}')
