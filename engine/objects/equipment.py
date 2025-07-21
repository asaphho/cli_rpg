from engine.objects.item import Item


class Equipment(Item):
	def __init__(self, item_id: str, display_name: str, slot_name: str):
		super().__init__(item_id=item_id, display_name=display_name)
		self.slot = slot_name
		
