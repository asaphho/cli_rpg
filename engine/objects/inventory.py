from engine.objects.item import Item
from engine.objects.equipment import Equipment, Weapon
from engine.objects.equipment_loadout import EquipmentLoadout
from typing import Union


class Inventory:

    def __init__(self, equipment_loadout: EquipmentLoadout,
                 items_in_storage: list[Item] = None,
                 gold: int = 0):
        self.items_in_storage: list[Item] = items_in_storage if items_in_storage is not None else []
        self.equipment_loadout: EquipmentLoadout = equipment_loadout
        self.gold: int = max(0, int(gold))

    def get_all_stacks(self, item_id: str) -> list[Item]:
        return [item for item in self.items_in_storage if item.get_id() == item_id]

    def get_current_gold(self) -> int:
        return self.gold

    def change_gold(self, amount: int, ignore_insufficient: bool = False):
        if (self.get_current_gold() + int(amount) < 0) and (ignore_insufficient is False):
            raise ValueError('Not enough gold.')
        self.gold = max(0, self.gold + int(amount))

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
                outstanding = stack.add_to_stack_return_excess(outstanding)
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

    def get_all_of_classification(self, classification: str) -> list[Item]:
        return [item for item in self.items_in_storage if item.get_item_classification() == classification]

    def get_all_classifications(self) -> list[str]:
        return list(set([item.get_item_classification() for item in self.items_in_storage]))

    def get_all_equipment(self) -> list[Equipment]:
        return [item for item in self.items_in_storage if isinstance(item, Equipment)]

    def get_all_equipment_classification(self) -> list[str]:
        return list(set([eqp.get_equipment_classification() for eqp in self.get_all_equipment()]))

    def equip_from_storage(self, equipment: Equipment) -> None:
        loadout = self.equipment_loadout
        curr_equipped = loadout.get_item(equipment.get_slot())
        if curr_equipped is not None:
            if (not equipment.is_stackable()) or (curr_equipped.get_id() != equipment.get_id()):
                self.add_to_storage(curr_equipped)
                loadout.equip(equipment)
                self.remove_from_storage(equipment.get_id(), equipment.get_stack_size())
            else:
                curr_equipped_stack = curr_equipped.get_stack_size()
                max_stack_size = curr_equipped.get_max_stack_size()
                capacity = max_stack_size - curr_equipped_stack
                if capacity == 0:
                    self.add_to_storage(curr_equipped)
                    loadout.equip(equipment)
                    self.remove_from_storage(equipment.get_id(), equipment.get_stack_size())
                elif capacity > 0:
                    equipping_stack_size = equipment.get_stack_size()
                    remaining = loadout.get_item(equipment.get_slot()).add_to_stack_return_excess(equipping_stack_size)
                    to_remove = equipping_stack_size - remaining
                    self.remove_from_storage(equipment.get_id(), to_remove)
        else:
            loadout.equip(equipment)
            self.remove_from_storage(equipment.get_id(), equipment.get_stack_size())
        if isinstance(equipment, Weapon):
            if equipment.two_handed:
                in_off_hand = loadout.get_item('Off-hand')
                if in_off_hand is not None:
                    loadout.unequip('Off-hand')
                    self.add_to_storage(in_off_hand)

    def unequip_into_storage(self, equipment: Equipment) -> None:
        self.equipment_loadout.unequip(equipment.get_slot())
        self.add_to_storage(equipment)

    def get_total_storage_weight(self) -> float:
        return sum([item.get_weight() for item in self.items_in_storage])

    def get_total_equipped_weight(self) -> float:
        equipped_weight = 0
        for slot in self.equipment_loadout.currently_equipped:
            if (item := self.equipment_loadout.get_item(slot)) is not None:
                equipped_weight += item.get_weight()
        return equipped_weight

    def get_total_carried_weight(self) -> float:
        return self.get_total_storage_weight() + self.get_total_equipped_weight()

    def export(self) -> dict[str, Union[int, dict, list]]:
        exported = {'gold': self.get_current_gold(),
                    'equipment': self.equipment_loadout.export()}
        stored_items = [(item.get_id(), item.get_stack_size()) for item in self.items_in_storage]
        exported['storage'] = stored_items
        return exported

    def import_from_data(self, data: dict[str, Union[int, dict, list]],
                         item_id_mapping: dict[str, Union[Item, Equipment]]) -> None:
        self.gold = int(data['gold'])
        self.equipment_loadout = EquipmentLoadout()
        self.equipment_loadout.import_from_data(data['equipment'], item_id_mapping)
        self.items_in_storage = []
        for item_id, qty in data['storage']:
            item = item_id_mapping[item_id]
            if item.is_stackable():
                self.add_to_storage(item.copy_stackable(int(qty)))
            else:
                self.add_to_storage(item)

