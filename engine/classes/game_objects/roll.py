from random import randint


class Roll:

    def __init__(self, n: int, d: int, bonus: int = 0, adv: int = 0, minimum=None):
        self.n = int(n)
        self.d = int(d)
        self.bonus = int(bonus)
        self.advantage = int(max(min(adv, 1), -1))
        self.minimum = minimum

    def add_bonus(self, amt: int):
        self.bonus += int(amt)

    def add_advantage(self):
        if self.advantage < 1:
            self.advantage += 1

    def add_disadvantage(self):
        if self.advantage > -1:
            self.advantage -= 1

    def roll(self) -> int:
        if int(self.n) <= 0 or int(self.d) <= 0:
            return 0
        else:
            first_roll = sum([randint(1, int(self.d)) for _ in range(int(self.n))])
            if self.advantage == 0:
                return first_roll
            else:
                second_roll = sum([randint(1, int(self.d)) for _ in range(int(self.n))])
                return max(first_roll, second_roll) if self.advantage > 0 else min(first_roll, second_roll)

    def apply_minimum(self, minimum: int):
        self.minimum = int(minimum)

    def remove_minimum(self):
        self.minimum = None

    def resolve(self) -> dict[str, int]:
        natural_roll = self.roll()
        with_bonus = natural_roll + int(self.bonus)
        if self.minimum is not None and isinstance(self.minimum, int):
            with_bonus = max(with_bonus, self.minimum)
        return {'natural': natural_roll, 'final': with_bonus}

    def copy(self):
        return Roll(self.n, self.d, self.bonus, self.advantage, self.minimum)

    def __str__(self):
        if int(self.n) <= 0 or int(self.d) <= 0:
            if self.minimum is not None and isinstance(self.minimum, int):
                const = max(int(self.bonus), self.minimum)
                return f'{int(const)}'
            else:
                return f'{int(self.bonus)}'
        else:
            strg = f'{int(self.n)}d{int(self.d)}'
            if int(self.bonus) != 0:
                if int(self.bonus) < 0:
                    strg += f' {int(self.bonus)}'
                else:
                    strg += f' +{int(self.bonus)}'
            if self.advantage == 1:
                strg += ' with advantage'
            elif self.advantage == -1:
                strg += ' with disadvantage'
            if self.minimum is not None and isinstance(self.minimum, int):
                roll_minimum = int(self.n) + int(self.bonus)
                roll_maximum = int(self.n) * int(self.d) + int(self.bonus)
                if roll_maximum > self.minimum > roll_minimum:
                    strg += f' (minimum of {self.minimum})'
                elif self.minimum >= roll_maximum:
                    strg = f'{self.minimum}'
            return strg