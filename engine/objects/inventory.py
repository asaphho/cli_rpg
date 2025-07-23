from engine.objects.item import Item
from engine.objects.equipment import Equipment
from engine.objects.equipment_loadout import EquipmentLoadout


class Inventory:

    def __init__(self, equipment_loadout: EquipmentLoadout,
                 items_in_storage: list[Item] = None):
        self.items_in_storage: list[Item] = items_in_storage if items_in_storage is not None else []
        self.equipment_loadout: EquipmentLoadout = equipment_loadout

    def get_all_stacks(self, item_id: str) -> list[Item]:
        return [item for item in self.items_in_storage if item.get_id() == item_id]

    def add_to_storage(self, item: Item) -> None:
        if not item.is_stackable():
            self.items_in_storage.append(item)
        else:
            all_stacks = self.get_all_stacks(item_id=item.get_id())
            max_stack_size = item.get_max_stack_size()
            stacks_with_capacity = [stack for stack in all_stacks if stack.get_stack_size() < max_stack_size]
            incoming_stack_size = item.get_stack_size()
            outstanding = incoming_stack_size
            for stack in stacks_with_capacity:
                outstanding = stack.add_to_stack_return_leftover(outstanding)
                if outstanding == 0:
                    break
            if outstanding > 0:
                self.items_in_storage.append(item.copy_stackable(outstanding))

    def remove_from_storage(self, item_id: str, quantity: int = 1) -> None:
        matching_items: list[Item] = [item for item in self.items_in_storage if item.get_id() == item_id]
        if len(matching_items) == 0:
            raise ValueError(f'Item not found.')
        item_to_remove = matching_items[0]
        if not item_to_remove.is_stackable():
            for i in range(len(self.items_in_storage)):
                if self.items_in_storage[i].get_id() == item_id:
                    self.items_in_storage.pop(i)
                    return
        else:
            total_stored_amount = sum([item.get_stack_size() for item in matching_items])
            if quantity > total_stored_amount:
                raise ValueError('Insufficient quantity in storage.')
            leftover = total_stored_amount - quantity
            self.items_in_storage = list(filter(lambda x: x.get_id() != item_id, self.items_in_storage))
            if leftover > 0:
                stack_to_add = item_to_remove.copy_stackable(leftover)
                self.add_to_storage(stack_to_add)

    def count_item_of_id(self, item_id: str) -> int:
        matching_items = [item for item in self.items_in_storage if item.get_id() == item_id]
        if len(matching_items) == 0:
            return 0
        else:
            stackable = matching_items[0].is_stackable()
            if stackable:
                return sum([item.get_stack_size() for item in matching_items])
            else:
                return len(matching_items)



