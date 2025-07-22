from engine.objects.item import Item


class Equipment(Item):
	def __init__(self, item_id: str, display_name: str, slot_name: str, stackable: bool = False, weight: float = 0,
				 stack_size: int = 1, max_stack_size: int = 1, quest_item: bool = False, classification: str = 'equipment',
				 equipment_classification: str = 'general_equipment'):
		super().__init__(item_id=item_id, display_name=display_name, equippable=True, stackable=stackable, weight=weight,
						 quest_item=quest_item, item_classification=classification, stack_size=stack_size,
						 max_stack_size=max_stack_size)
		self.slot = slot_name.lower().strip()
		self.equipment_classification = equipment_classification

	def get_slot(self) -> str:
		return self.slot

	def get_equipment_classification(self) -> str:
		return self.equipment_classification

