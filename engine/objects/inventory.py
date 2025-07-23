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


