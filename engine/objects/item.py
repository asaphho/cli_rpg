class Item:
    """
    Object for general item.
    :param item_id (str): This id is used internally.
    :param display_name (str): The name to be displayed in-game
    :param equippable (bool): Whether this item can be equipped in an EquipmentLoadout
    :param stackable (bool): Whether this item can be in a stack
    :param weight (float): A number can be assigned to give the item weight
    :param quest_item (bool): Setting this to true prevents this item from being removed from inventory by normal means
    :param base_worth (int): A number can be assigned to give the item a gold value
    :param item_classification (str): A flag to be used in any way you want
    """

    def __init__(self, item_id: str, display_name: str, equippable: bool = False, stackable: bool = False, stack_size: int = 1,
                 max_stack_size: int = 1, weight: float = 0, quest_item: bool = False, base_worth: int = 0,
                 item_classification: str = 'general', description: str = ''):
        self.item_id = item_id
        self.display_name = display_name
        self.equippable = equippable
        self.stackable = stackable
        self.weight = weight
        self.quest_item = quest_item
        self.base_worth = base_worth
        self.classification = item_classification.lower().strip()
        self.stack_size = min(stack_size, max_stack_size)
        self.max_stack_size = max_stack_size
        self.description = description

    def get_id(self) -> str:
        return self.item_id

    def get_display_name(self, include_stack_size: bool = False) -> str:
        return self.display_name + f' ({self.get_stack_size()})' if self.is_stackable() and include_stack_size else ''

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

    def get_item_classification(self) -> str:
        return self.classification

    def get_stack_size(self) -> int:
        return self.stack_size

    def get_max_stack_size(self) -> int:
        return self.max_stack_size

    def add_to_stack_return_leftover(self, incoming_stack_size: int) -> int:
        if not self.is_stackable():
            raise ValueError('Cannot be stacked')
        original_stack_size = self.get_stack_size()
        self.stack_size = min(original_stack_size + incoming_stack_size, self.get_max_stack_size())
        return max(0, original_stack_size + incoming_stack_size - self.get_max_stack_size())

    def remove_from_stack_return_all_gone(self, count: int, ignore_insufficient: bool = False) -> bool:
        if (count > self.get_stack_size()) and (ignore_insufficient is False):
            raise ValueError('Insufficient amount in stack.')
        self.stack_size = max(0, self.get_stack_size() - count)
        return self.get_stack_size() == 0

    def get_description_for_display(self) -> str:
        return f'{self.get_display_name()}\n\n{self.description}'
