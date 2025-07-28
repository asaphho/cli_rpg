from typing import Callable
from engine.contexts.context import Context
from engine.utils.choice_handler import ChoiceHandler
from engine.objects.item import Item
from engine.objects.item_container import ItemContainer
from engine.objects.inventory import Inventory


class OpenContainerContext(Context):

    def __init__(self, parent_context: Context, context_data: dict,
                 container: ItemContainer, player_inventory: Inventory):
        super().__init__(parent_context=parent_context,
                         context_type='open_container',
                         context_data=context_data)
        self.container: ItemContainer = container
        self.player_inventory: Inventory = player_inventory
        if container.gold_contained == 0 and container.items == []:
            self.entry_text = f'The {container.display_name} is empty.'
        else:
            self.entry_text = f'These are the items in the {container.display_name}. Select an item to store it in your inventory.'

    def _generate_choice_handling(self) -> ChoiceHandler:
        choice_handler = ChoiceHandler(reserved_choices=[('b', 'Back')])

        def make_take_gold_executor(amt: int) -> Callable:
            def take_gold_executor(curr_context: OpenContainerContext, parent_context: Context) -> bool:
                curr_context.player_inventory.change_gold(amt)
                curr_context.container.add_gold(-1 * amt)
                return False
            return take_gold_executor

        def make_take_item_executor(item: Item) -> Callable:
            def take_item_executor(curr_context: OpenContainerContext, parent_context: Context) -> bool:
                curr_context.player_inventory.add_to_storage(item)
                curr_context.container.remove_item(item)
                return False
            return take_item_executor

        if self.container.gold_contained == 0 and self.container.items == []:
            self.entry_text = f'The {self.container.display_name} is empty.'
        else:
            self.entry_text = f'These are the items in the {self.container.display_name}. Select an item to store it in your inventory.'
        if self.container.gold_contained > 0:
            choice_handler.add_choice(executor=make_take_gold_executor(self.container.gold_contained),
                                      display_text=f'Gold: ({self.container.gold_contained})')
        for itm in self.container.items:
            choice_handler.add_choice(executor=make_take_item_executor(itm),
                                      display_text=f'{itm.get_display_name(include_stack_size=True)}')
        return choice_handler
