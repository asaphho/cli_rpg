from copy import deepcopy
from typing import Callable
from engine.objects.item import Item
from engine.contexts.context import Context
from engine.objects.inventory import Inventory
from engine.utils.choice_handler import ChoiceHandler


class InventoryContext(Context):
    """
    context_data['scope'] possibilities: 'top', 'equipment', 'storage-top', 'storage: <classification>
    context_data['required_tags'] = {<tag categories>: [tags]}
    context_data['forbidden_tags'] = {<tag categories>: [tags]}
    tag categories must match equipment_classification property exactly
    """

    def __init__(self,
                 parent_context: Context,
                 context_data: dict,
                 inventory: Inventory):
        super().__init__(parent_context=parent_context,
                         context_type='inventory',
                         context_data=context_data)
        self.inventory: Inventory = inventory

    def print_entry_text(self) -> None:
        # TODO: Make sure every scope is included
        scope = self.get_context_data()['scope']
        if scope == 'top':
            self.entry_text = 'You are looking at your inventory. Choose an action below.'
        elif scope == 'equipment':
            self.entry_text = 'These are your currently-equipped items. Select an item to view its description or replace it.'
        elif scope == 'storage-top':
            self.entry_text = 'These are your items in storage. Select a category.'
        elif scope.startswith('storage: '):
            self.entry_text = ''

        print(self.entry_text)

    def _generate_choice_handling(self) -> ChoiceHandler:
        scope = self.get_context_data()['scope']
        choice_handler = ChoiceHandler(reserved_choices=[('b', 'Back')])
        # TODO: Make sure every scope is included
        if scope == 'top':
            def make_executor(choice: str) -> Callable:
                def executor(curr_context: InventoryContext, parent_context: Context) -> bool:
                    new_scope = 'equipment' if choice == 'e' else 'storage'
                    new_context_data = deepcopy(curr_context.get_context_data())
                    new_context_data['scope'] = new_scope
                    new_context = InventoryContext(parent_context=parent_context,
                                                   context_data=new_context_data,
                                                   inventory=curr_context.inventory)
                    new_context.enter()
                    return False

                return executor

            choice_handler.add_choice(executor=make_executor('e'),
                                      display_text='View equipment',
                                      choice_letter='e')
            choice_handler.add_choice(executor=make_executor('s'),
                                      display_text='Stored items',
                                      choice_letter='s')
        elif scope == 'equipment':
            # TODO: Complete
            pass
        return choice_handler


class ItemDescriptionPage(Context):

    def __init__(self, parent_context: Context, context_data: dict,
                 item: Item, currently_equipped: bool):
        super().__init__(parent_context=parent_context, context_type='item_description',
                         context_data=context_data)
        self.item = item
        self.item_currently_equipped = currently_equipped
        self.entry_text = item.get_description_for_display()


