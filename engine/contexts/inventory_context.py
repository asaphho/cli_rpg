from copy import deepcopy
from typing import Callable
from engine.objects.item import Item
from engine.objects.equipment import Equipment
from engine.contexts.context import Context
from engine.contexts.popup_context import PopupContext
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
            self.entry_text = scope.split(': ', maxsplit=1)[1]

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

            def empty_slot_executor(*args):
                print('Slot is empty.')
                return False

            def make_item_executor(equipment: Equipment) -> Callable:
                def item_executor(curr_context: InventoryContext, parent_context: Context) -> bool:
                    item_description_context = ItemDescriptionPage(parent_context=parent_context,
                                                                   context_data=curr_context.get_context_data(),
                                                                   item=equipment,
                                                                   currently_equipped=True,
                                                                   inventory=curr_context.inventory)
                    item_description_context.enter()
                    return False
                return item_executor

            slot_names = self.inventory.equipment_loadout.get_slot_names()
            for i in range(1, len(slot_names) + 1):
                slot_name = slot_names[i - 1]
                item_at_slot = self.inventory.equipment_loadout.get_item(slot_name)
                if item_at_slot is None:
                    choice_handler.add_choice(executor=empty_slot_executor,
                                              display_text=f'{slot_name}: Empty')
                else:
                    choice_handler.add_choice(executor=make_item_executor(item_at_slot),
                                              display_text=f'{slot_name}: {item_at_slot.get_display_name(include_stack_size=True)}')
        elif scope == 'storage-top':
            item_categories: list[str] = self.inventory.get_all_classifications()

            def equipment_executor(curr_context: InventoryContext, parent_context: Context) -> bool:
                new_context_data = deepcopy(curr_context.get_context_data())
                new_context_data['scope'] = 'storage: Equipment'
                new_context = InventoryContext(parent_context=parent_context,
                                               context_data=new_context_data,
                                               inventory=curr_context.inventory)
                new_context.enter()
                return False

            def make_category_executor(classification: str) -> Callable[[InventoryContext, Context], bool]:
                def other_category_executor(curr_context: InventoryContext, parent_context: Context) -> bool:
                    new_context_data = deepcopy(curr_context.get_context_data())
                    new_context_data['scope'] = f'storage: {classification}'
                    new_context = InventoryContext(parent_context=parent_context,
                                                   context_data=new_context_data,
                                                   inventory=curr_context.inventory)
                    new_context.enter()
                    return False
                return other_category_executor
            if 'Equipment' in item_categories:
                choice_handler.add_choice(executor=equipment_executor,
                                          display_text='Equipment')
                item_categories.remove('Equipment')
            for category in item_categories:
                choice_handler.add_choice(executor=make_category_executor(category),
                                          display_text=category)
            choice_handler.add_choice(executor=make_category_executor('All'),
                                      display_text='All items in storage',
                                      choice_letter='a')
        elif scope.startswith('storage: '):
            # TODO: Write this
            def make_item_desc_executor(itm: Item) -> Callable:
                def item_desc_executor(curr_context: InventoryContext, parent_context: Context) -> bool:
                    new_context_data = deepcopy(curr_context.get_context_data())
                    item_desc_context = ItemDescriptionPage(parent_context=parent_context,
                                                            context_data=new_context_data,
                                                            inventory=curr_context.inventory,
                                                            item=itm,
                                                            currently_equipped=False)
                    item_desc_context.enter()
                    return False
                return item_desc_executor
            item_classification = scope.split(': ', maxsplit=1)[1]
            if item_classification != 'All':
                all_items_of_classification = self.inventory.get_all_of_classification(item_classification)
            else:
                all_items_of_classification = self.inventory.items_in_storage
            for item in all_items_of_classification:
                choice_handler.add_choice(executor=make_item_desc_executor(item),
                                          display_text=item.get_display_name(include_stack_size=True))
        return choice_handler


class ItemDescriptionPage(Context):

    def __init__(self, parent_context: Context, context_data: dict,
                 item: Item, currently_equipped: bool, inventory: Inventory):
        super().__init__(parent_context=parent_context, context_type='item_description',
                         context_data=context_data)
        self.item = item
        self.item_currently_equipped = currently_equipped
        self.entry_text = item.get_description_for_display()
        self.inventory = inventory

    def _generate_choice_handling(self) -> ChoiceHandler:
        choice_handler = ChoiceHandler(reserved_choices=[('b', 'Back')])

        def unequip_executor(curr_context: ItemDescriptionPage,
                             parent_context: Context) -> bool:
            assert isinstance(curr_context.item, Equipment)
            curr_context.inventory.unequip_into_storage(curr_context.item)
            print(f'{curr_context.item.get_display_name()} unequipped.')
            return True

        def equip_executor(curr_context: ItemDescriptionPage,
                           parent_context: Context) -> bool:
            assert isinstance(curr_context.item, Equipment)
            required_tags: list[str] = curr_context.get_context_data().get('required_tags', {}).get(curr_context.item.get_equipment_classification(), [])
            forbidden_tags: list[str] = curr_context.get_context_data().get('forbidden_tags', {}).get(curr_context.item.get_equipment_classification(), [])
            if (any([curr_context.item.has_tag(t) for t in forbidden_tags])
                    or not all([curr_context.item.has_tag(t) for t in required_tags])):
                print('THIS ITEM CANNOT BE EQUIPPED BY YOU.')
                return False
            if curr_context.item.get_slot() == 'Off-hand' and curr_context.inventory.equipment_loadout.two_handed_equipped():
                print('Cannot equip off-hand item when two-handed weapon is equipped.')
                return False
            curr_context.inventory.equip_from_storage(curr_context.item)
            print(f'{curr_context.item.get_display_name()} equipped.')
            return True

        def drop_executor(curr_context: ItemDescriptionPage,
                          parent_context: Context) -> bool:
            if curr_context.item.is_quest_item():
                print('YOU CANNOT DROP THIS ITEM.')
                return False
            player_input = ''
            while player_input.strip().lower() not in ('y', 'n'):
                player_input = input('Are you sure you want to drop this item? It may disappear permanently. (y/n)')
            if player_input.strip().lower() == 'y':
                if curr_context.item.is_stackable() and curr_context.item.get_stack_size() > 1:
                    while not player_input.strip().isnumeric():
                        player_input = input('Drop how many?')
                        if not player_input.strip().isnumeric():
                            print('Invalid input')
                        elif int(player_input.strip()) <= 0:
                            print('Invalid quantity')
                            player_input = ''
                    stack_size = curr_context.item.get_stack_size()
                    quantity_to_drop = min(stack_size, int(player_input))
                    curr_context.inventory.remove_from_storage(curr_context.item.get_id(), quantity_to_drop)
                    print(f'{curr_context.item.get_display_name()} ({quantity_to_drop}) dropped.')
                    return True
                else:
                    curr_context.inventory.remove_from_storage(curr_context.item.get_id())
                    print(f'{curr_context.item.get_display_name()} dropped.')
                    return True
            else:
                return False

        def consume_executor(curr_context: ItemDescriptionPage,
                             parent_context: Context) -> bool:
            assert curr_context.item.is_consumable()
            if curr_context.item_currently_equipped:
                assert isinstance(curr_context.item, Equipment)
                all_gone = curr_context.item.remove_from_stack_return_all_gone(1)
                if all_gone:
                    slot = curr_context.item.get_slot()
                    curr_context.inventory.equipment_loadout.unequip(slot)
            else:
                curr_context.inventory.remove_from_storage(curr_context.item.get_id(), 1)
            curr_context.item.consume_function(parent_context)
            print(f'{curr_context.item.get_display_name()} consumed.')
            return True

        def popup_executor(curr_context: ItemDescriptionPage,
                           parent_context: Context) -> bool:
            item_description = curr_context.item.get_description_for_display()
            popup_context = PopupContext(parent_context=parent_context,
                                         display_text=item_description)
            popup_context.enter()
            return False

        if self.item_currently_equipped:
            choice_handler.add_choice(executor=unequip_executor,
                                      display_text='Unequip item',
                                      choice_letter='u')
        if (not self.item_currently_equipped) and isinstance(self.item, Equipment):
            choice_handler.add_choice(executor=equip_executor,
                                      display_text='Equip item',
                                      choice_letter='e')
            if self.inventory.equipment_loadout.get_item(self.item.get_slot()) is not None:
                choice_handler.add_choice(executor=popup_executor,
                                          display_text=f'View currently equipped in {self.item.get_slot()}',
                                          choice_letter='v')
        if self.item.consumable:
            choice_handler.add_choice(executor=consume_executor,
                                      display_text='Consume',
                                      choice_letter='c')
        if (not self.item_currently_equipped) and (not self.item.is_quest_item()):
            choice_handler.add_choice(executor=drop_executor,
                                      display_text='Drop item',
                                      choice_letter='d')
        return choice_handler
