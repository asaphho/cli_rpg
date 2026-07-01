from random import randint


class Roll:

    def __init__(self, n: int = 1, d: int = 20, advantage: int = 0, bonus: int = 0, floor_at_zero: bool = True):
        self.n = max(int(n), 1)
        self.d = max(int(d), 2)
        self.advantage = min(max(int(advantage), -1), 1)
        self.bonus = int(bonus)
        self.floor_at_zero = floor_at_zero

    def add_bonus(self, amt: int):
        self.bonus += int(amt)

    def get_bonus(self) -> int:
        return self.bonus

    def add_advantage(self):
        if self.advantage < 1:
            self.advantage += 1

    def add_disadvantage(self):
        if self.advantage > -1:
            self.advantage -= 1

    def get_advantage(self) -> int:
        return self.advantage

    def natural_roll_once(self) -> int:
        return sum([randint(1, self.d) for _ in range(self.n)])

    def natural_roll(self) -> int:
        if self.get_advantage() == 0:
            return self.natural_roll_once()
        else:
            rolls = [self.natural_roll_once(), self.natural_roll_once()]
            return max(rolls) if self.get_advantage() == 1 else min(rolls)

    def resolve(self) -> int:
        natural_roll = self.natural_roll()
        if self.floor_at_zero:
            return max(0, natural_roll + self.get_bonus())
        else:
            return natural_roll + self.get_bonus()

    def resolve_after_natural_roll(self, natural_roll_value: int) -> int:
        if self.floor_at_zero:
            return max(int(natural_roll_value) + self.get_bonus(), 0)
        else:
            return int(natural_roll_value) + self.get_bonus()
