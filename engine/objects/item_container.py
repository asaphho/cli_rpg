from engine.objects.item import Item
from typing import Union


class ItemContainer:

    def __init__(self, container_id: str, display_name: str, locked: bool = False, can_lockpick: bool = True,
                 lock_difficulty: int = 1, items: list[Item] = None, gold_contained: int = 0):
        self.container_id: str = container_id
        self.display_name: str = display_name
        self.locked: bool = locked
        self.can_lockpick: bool = can_lockpick
        self.items: list[Item] = [] if items is None else items
        if locked and can_lockpick:
            self.lock_difficulty: int = max(1, int(lock_difficulty))
        if locked and not can_lockpick:
            self.lock_difficulty: int = 999999
        if not locked:
            self.lock_difficulty: int = 0
        self.gold_contained: int = max(0, int(gold_contained))

    def lock(self) -> None:
        self.locked = True

    def unlock(self) -> None:
        self.locked = False

    def set_gold(self, amt: int) -> None:
        self.gold_contained = max(0, int(amt))

    def add_gold(self, amt: int) -> None:
        self.gold_contained = max(0, self.gold_contained + int(amt))

    def set_lock_difficulty(self, new_difficulty: int) -> None:
        self.lock_difficulty = max(1, int(new_difficulty))

    def set_cannot_lockpick(self) -> None:
        self.can_lockpick = False

    def set_can_lockpick(self) -> None:
        self.can_lockpick = True

    def add_item(self, item: Item) -> None:
        if item.is_stackable():
            stacks = [itm for itm in self.items if itm.get_id() == item.get_id()]
            outstanding = item.get_stack_size()
            max_stack_size = item.get_max_stack_size()
            for stack in stacks:
                if (max_stack_size - stack.get_stack_size() > 0) and (outstanding > 0):
                    outstanding = stack.add_to_stack_return_excess(outstanding)
            if outstanding > 0:
                self.items.append(item.copy_stackable(outstanding))
        else:
            self.items.append(item)

    def remove_item(self, item: Item) -> None:
        if not item.is_stackable():
            for i in range(len(self.items)):
                if self.items[i].get_id() == item.get_id():
                    self.items.pop(i)
                    return
        else:
            stack_size = item.get_stack_size()
            initial_amount = sum([stk.get_stack_size() for stk in self.items if stk.get_id() == item.get_id()])
            self.items = list(filter(lambda x: x.get_id() != item.get_id(), self.items))
            if stack_size < initial_amount:
                to_add_back = initial_amount - stack_size
                self.add_item(item.copy_stackable(to_add_back))

    def export(self) -> dict[str, Union[str, int, list]]:
        exported = {'container_id': self.container_id, 'display_name': self.display_name,
                    'gold': self.gold_contained, 'locked': 'true' if self.locked else 'false',
                    'can_lockpick': 'true' if self.can_lockpick else 'false', 'lock_difficulty': self.lock_difficulty}
        stored_items = [(item.get_id(), item.get_stack_size()) for item in self.items]
        exported['items'] = stored_items
        return exported

    def import_from_data(self, data: dict[str, Union[str, int, list]], item_id_mapping: dict[str, Item]) -> None:
        self.container_id = data['container_id']
        self.display_name = data['display_name']
        self.gold_contained = int(data['gold'])
        self.locked = data['locked'] == 'true'
        self.can_lockpick = data['can_lockpick'] == 'true'
        self.lock_difficulty = int(data['lock_difficulty'])
        self.items = []
        for item_id, qty in data['items']:
            item = item_id_mapping[item_id]
            if item.is_stackable():
                self.add_item(item.copy_stackable(int(qty)))
            else:
                self.add_item(item)
