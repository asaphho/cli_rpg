class Item:

    def __init__(self, item_id: str, display_name: str, equippable: bool = False, stackable: bool = False,
                 weight: float = 0, quest_item: bool = False, base_worth: int = 0):
        self.item_id = item_id
        self.display_name = display_name
        self.equippable = equippable
        self.stackable = stackable
        self.weight = weight
        self.quest_item = quest_item
        self.base_worth = base_worth

    def get_id(self) -> str:
        return self.item_id

    def get_display_name(self) -> str:
        return self.display_name

    def is_equippable(self) -> bool:
        return self.equippable

    def is_stackable(self) -> bool:
        return self.stackable

    def get_weight(self) -> float:
        return self.weight

    def is_quest_item(self) -> bool:
        return self.quest_item

    def get_base_worth(self) -> int:
        return self.base_worth
