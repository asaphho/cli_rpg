class Creature:

    def __init__(self, creature_id: str, display_name: str, creature_type: str, max_hp: int, starting_hp: int = None):
        self.creature_id = creature_id
        self.display_name = display_name
        self.creature_type = creature_type
        self.max_hp = max(1, int(max_hp))
        if starting_hp is None:
            self.hp = self.max_hp
        else:
            self.hp = max(min(self.max_hp, int(starting_hp)), 0)
        self.alive = self.hp > 0

    def get_id(self) -> str:
        return self.creature_id

    def get_display_name(self) -> str:
        return self.display_name

    def get_creature_type(self) -> str:
        return self.creature_type

    def is_alive(self) -> bool:
        return self.hp > 0

    def damage(self, amt: int) -> None:
        self.hp -= max(0, int(amt))
        if self.hp <= 0:
            self.alive = False

    def heal(self, amt: int) -> None:
        self.hp += max(0, int(amt))
        self.hp = min(self.max_hp, self.hp)

    def kill(self) -> None:
        self.hp = 0
        self.alive = False
