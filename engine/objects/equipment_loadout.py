from typing import Union
from engine.objects.equipment import Equipment, Weapon


class EquipmentLoadout:
	def __init__(self, slot_names: list[str] = None):
		cleaned_slot_names = [name.strip() for name in slot_names] if slot_names is not None else []
		if 'Main hand' in cleaned_slot_names or 'Off-hand' in cleaned_slot_names:
			raise ValueError('\'Main hand\' and \'Off-hand\' are reserved names.')
		deduplicated_slot_names = list(set(cleaned_slot_names))
		self.slots: list[str] = deduplicated_slot_names + ['Main hand', 'Off-hand']
		self.currently_equipped: dict[str, Union[Equipment, None]] = {'Main hand': None, 'Off-hand': None}
		for slot in slot_names:
			self.currently_equipped[slot] = None

	def create_slot(self, slot_name: str) -> None:
		if slot_name.strip() in self.slots:
			raise ValueError('Slot name already exists')
		self.currently_equipped[slot_name.strip()] = None
		self.slots.append(slot_name.strip())

	def equip(self, equipment: Equipment) -> None:
		slot = equipment.get_slot()
		if slot not in self.slots:
			raise ValueError(f'Slot {slot} does not exist')
		self.currently_equipped[slot] = equipment

	def unequip(self, slot: str) -> None:
		if slot.strip() in self.currently_equipped:
			self.currently_equipped[slot.strip()] = None

	def remove_slot(self, slot: str) -> None:
		if slot.strip() in ('Main hand', 'Off-hand'):
			raise ValueError('Slot cannot be removed')
		if slot.strip() in self.currently_equipped:
			self.currently_equipped.pop(slot.strip())
			self.slots.remove(slot.strip())
		else:
			raise ValueError(f'Slot \'{slot.strip()}\' does not exist')

	def get_item(self, slot: str) -> Union[Equipment, None]:
		return self.currently_equipped.get(slot.strip(), None)

	def slot_empty(self, slot: str) -> bool:
		if slot.strip() not in self.slots:
			raise ValueError(f'Slot \'{slot.strip()}\' does not exist.')
		return self.get_item(slot) is None

	def get_loadout_display(self) -> str:
		display_text = ''
		for slot in self.slots:
			name_to_display = self.get_item(slot).get_display_name(include_stack_size=True) if not self.slot_empty(slot)\
				else 'Empty'
			display_text += f'{slot}: {name_to_display}\n'
		return display_text

	def two_handed_equipped(self) -> bool:
		weapon = self.get_item('Main hand')
		if self.get_item('Main hand') is None:
			return False
		assert isinstance(weapon, Weapon)
		return weapon.two_handed

