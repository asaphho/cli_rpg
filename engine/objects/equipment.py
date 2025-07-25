from engine.objects.item import Item
from engine.utils.roll import Roll
from typing import Union, Callable


class Equipment(Item):
    def __init__(self, item_id: str, display_name: str, slot_name: str, stackable: bool = False, weight: float = 0,
                 stack_size: int = 1, max_stack_size: int = 1, quest_item: bool = False,
                 consumable: bool = False, consume_function: Callable = None,
                 equipment_classification: str = 'Apparel', description: str = '', base_value: int = 0,
                 tags: list[str] = None):
        super().__init__(item_id=item_id, display_name=display_name, equippable=True, stackable=stackable,
                         weight=weight, consumable=consumable, consume_function=consume_function,
                         quest_item=quest_item, item_classification='Equipment', stack_size=stack_size,
                         base_value=base_value, max_stack_size=max_stack_size, description=description)
        self.slot = slot_name.strip()
        self.equipment_classification = equipment_classification.lower().strip()
        self.tags: list[str] = [] if tags is None else tags

    def get_slot(self) -> str:
        return self.slot

    def get_equipment_classification(self) -> str:
        return self.equipment_classification

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags


class Weapon(Equipment):

    def __init__(self, item_id: str, display_name: str, damage_roll: Roll, damage_type: str, ranged: bool = False,
                 two_handed: bool = False, required_ammo_type: str = None, self_ammo: bool = False,
                 stackable: bool = False, stack_size: int = 1, max_stack_size: int = 1, weight: float = 0,
                 base_value: int = 0, quest_item: bool = False,
                 description: str = '', tags: list[str] = None):
        super().__init__(item_id=item_id, display_name=display_name, slot_name='Main hand', stackable=stackable,
                         stack_size=stack_size, max_stack_size=max_stack_size, weight=weight, base_value=base_value,
                         quest_item=quest_item, consumable=False,
                         equipment_classification='Weapons', description=description, tags=tags)
        self.damage_roll: Roll = damage_roll
        self.damage_type: str = damage_type
        self.ranged: bool = ranged
        self.two_handed: bool = two_handed
        self.needs_ammo: bool = required_ammo_type is not None
        self.required_ammo_type: Union[str, None] = required_ammo_type
        self.self_ammo: bool = self_ammo

    def get_damage_roll(self) -> Roll:
        return self.damage_roll.copy()

    def get_description_for_display(self) -> str:
        text = f'{self.get_display_name()}\n\n{self.description}\n\n'
        text += f'Damage: {self.damage_roll.get_display_text()}\n'
        text += f'Damage type: {self.damage_type}\n'
        text += 'Two-handed, ' if self.two_handed else 'One-handed, '
        text += 'ranged\n' if self.ranged else 'melee\n'
        if (self.required_ammo_type is not None) and (self.self_ammo is False):
            text += f'Required ammo type: {self.required_ammo_type}\n'
        text += f'Weight: {self.get_unit_weight()}\nBase value: {self.get_base_value()}'
        if len(self.tags) > 0:
            text += f"\nTags: {', '.join(self.tags)}"
        return text

# TODO: Finish this
