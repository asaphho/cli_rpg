from random import randint
from typing import Callable


class Roll:

    def __init__(self, n: int = 1, d: int = 20, bonus: int = 0, adv: int = 0, minimum: int = 0):
        self.n = max(1, int(n))
        self.d = max(2, int(d))
        self.bonus = int(bonus)
        if adv != 0:
            self.adv = int(adv//abs(adv))
        else:
            self.adv = 0
        self.min = int(minimum)

    def minimum_forces_constant(self) -> bool:
        if self.bonus >= 0:
            return False
        return self.n * self.d + self.bonus <= self.min

    def get_display_text(self) -> str:
        if self.minimum_forces_constant():
            return str(self.min)
        text = f'{self.n}d{self.d}'
        if self.bonus > 0:
            text += f'+{self.bonus}'
        elif self.bonus < 0:
            text += str(self.bonus)
        if self.adv == 1:
            text += ' with advantage'
        elif self.adv == -1:
            text += ' with disadvantage'
        if (self.bonus < 0) and (self.n + self.bonus < self.min):
            text += f' (min. {self.min})'
        return text

    def add_bonus(self, amt: int) -> None:
        self.bonus += int(amt)

    def add_dice(self, n: int) -> None:
        self.n = max(self.n + int(n), 1)

    def grant_advantage(self) -> None:
        self.adv = min(1, self.adv + 1)

    def grant_disadvantage(self) -> None:
        self.adv = max(self.adv - 1, -1)

    def raw_roll_once(self) -> int:
        return sum([randint(1, self.d) for _ in range(self.n)])

    def roll(self) -> int:
        if self.minimum_forces_constant():
            return self.min

        raw_rolls = [self.raw_roll_once() for _ in range(abs(self.adv) + 1)]

        def take_first(x):
            return x[0]

        funcs: list[Callable[[list[int]], int]] = [take_first, max, min]
        func: Callable[[list[int]], int] = funcs[self.adv]
        result = func(raw_rolls)
        if self.bonus >= 0:
            return result + self.bonus
        else:
            return max(result + self.bonus, self.min)

    def set_minimum(self, new_min: int) -> None:
        self.min = int(new_min)

    def set_die_size(self, new_size: int) -> None:
        self.d = max(2, int(new_size))

    def set_n(self, new_n: int) -> None:
        self.n = max(1, int(new_n))

    def set_bonus(self, new_bonus) -> None:
        self.bonus = int(new_bonus)

    def set_advantage(self, adv: int) -> None:
        if adv != 0:
            self.adv = int(adv//abs(adv))
        else:
            self.adv = 0

    def copy(self):
        return Roll(n=self.n, d=self.d, adv=self.adv, bonus=self.bonus, minimum=self.min)

