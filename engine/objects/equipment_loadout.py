from typing import Union
from engine.objects.equipment import Equipment


class EquipmentLoadout:
	def __init__(self, slot_names: list[str] = None):
		cleaned_slot_names = [name.lower().strip() for name in slot_names] if slot_names is not None else []
		if 'main_hand' in cleaned_slot_names or 'off_hand' in cleaned_slot_names:
			raise ValueError('\'main_hand\' and \'off_hand\' are reserved names.')
		deduplicated_slot_names = list(set(cleaned_slot_names))
		self.slots: list[str] = deduplicated_slot_names
		self.currently_equipped: dict[str, Union[Equipment, None]] = {'main_hand': None, 'off_hand': None}
		for slot in slot_names:
			self.currently_equipped[slot] = None

	def create_slot(self, slot_name: str) -> None:
		if slot_name.lower().strip() in self.currently_equipped:
			raise ValueError('Slot name already exists')
		self.currently_equipped[slot_name.lower().strip()] = None

	def equip(self, equipment: Equipment) -> None:
		slot = equipment.get_slot()
		if slot not in self.currently_equipped:
			raise ValueError(f'Slot {slot} does not exist')
		self.currently_equipped[slot] = equipment

	def unequip(self, slot: str) -> None:
		if slot.lower().strip() in self.currently_equipped:
			self.currently_equipped[slot.lower().strip()] = None

	def remove_slot(self, slot: str) -> None:
		if slot.lower().strip() in ('main_hand', 'off_hand'):
			raise ValueError('Slot cannot be removed')
		if slot.lower().strip() in self.currently_equipped:
			self.currently_equipped.pop(slot.lower().strip())
		else:
			raise ValueError(f'Slot \'{slot.lower().strip()}\' does not exist')

	def get_item(self, slot: str) -> Union[Equipment, None]:
		return self.currently_equipped.get(slot.lower().strip(), None)

	def slot_empty(self, slot: str) -> bool:
		return self.get_item(slot) is None
