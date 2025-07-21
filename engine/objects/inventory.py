from typing import Union
from engine.objects.equipment import Equipment


class EquipmentLoadout:
	def __init__(self, slot_names: list[str]=None):
		cleaned_slot_names = [name.lower().strip() for name in slot_names] if slot_names is not None else []
		if 'main_hand' in cleaned_slot_names or 'off_hand' in cleaned_slot_names:
			raise ValueError('\'main_hand\' and \'off_hand\' are reserved names.')
		deduplicated_slot_names = list(set(cleaned_slot_names))
		self.slots: list[str] = deduplicated_slot_names
		self.currently_equipped: dict[str, Union[Equipment, None]] = {'main_hand': None, 'off_hand': None}
		for slot in slot_names:
			self.currently_equipped[slot] = None


		
		
