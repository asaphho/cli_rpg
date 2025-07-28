from engine.objects.item import Item


class ItemContainer:

    def __init__(self, container_id: str, display_name: str, locked: bool = False, can_lockpick: bool = True, lock_difficulty: int = 0, items: list[Item] = None):
        self.container_id = container_id
        self.display_name = display_name
        self.locked = locked
        self.can_lockpick = can_lockpick
        self.items = [] if items is None else items
        self.lock_difficulty = lock_difficulty

    def lock(self) -> None:
        self.locked = True

    def unlock(self) -> None:
        self.locked = False

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







