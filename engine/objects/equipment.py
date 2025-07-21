from engine.objects.item import Item


class Equipment(Item):
	def __init__(self, item_id: str, display_name: str, slot_name: str, stackable: bool = False, weight: float = 0, quest_item: bool = False):
		super().__init__(item_id=item_id, display_name=display_name, equippable=True, stackable=stackable, weight=weight, quest_item=quest_item)
		self.slot = slot_name

	def get_slot(self) -> str:
		return self.slot

