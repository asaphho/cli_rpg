from engine.contexts.context import Context
from engine.utils.dialogue_tree import DialogueTree
from engine.utils.choice_handler import ChoiceHandler
from typing import Callable


class DialogueContext(Context):
    def __init__(self, parent_context: Context, context_data: dict, dialogue_tree: DialogueTree,
                 curr_node: str = ''):
        super().__init__(parent_context=parent_context,
                         context_type='dialogue',
                         context_data=context_data)
        self.dialogue_tree: DialogueTree = dialogue_tree
        self.dialogue_tree.update_current_node(curr_node)
        self.player_name = context_data['player_name']
        self.npc_name = context_data['npc_name']
        self.entry_text = self.dialogue_tree.get_current_text(player_name=self.player_name,
                                                              npc_name=self.npc_name)

    def _generate_choice_handling(self) -> ChoiceHandler:
        choice_handler = ChoiceHandler()
        if self.dialogue_tree.is_at_terminal_node():
            def terminate_dialogue(c1: Context, c2: Context) -> bool:
                return True

            choice_handler.add_choice(executor=terminate_dialogue,
                                      display_text='End dialogue')
            return choice_handler

        available_nodes = self.dialogue_tree.get_available_nodes()

        def make_choice_executor(node: str) -> Callable[[DialogueContext, Context], bool]:
            def dialogue_choice_executor(current_context: DialogueContext, parent_context: Context) -> bool:
                current_context.dialogue_tree.update_current_node(node)
                current_context.entry_text = current_context.dialogue_tree.get_current_text(player_name=current_context.player_name,
                                                                                            npc_name=current_context.npc_name)
                current_context.dialogue_tree.get_action(node)(parent_context.context_data)
                return False
            return dialogue_choice_executor

        for dialogue_option in available_nodes:
            player_line = self.dialogue_tree.get_player_line(dialogue_option)
            executor = make_choice_executor(dialogue_option)
            choice_handler.add_choice(executor=executor,
                                      display_text=player_line)
        return choice_handler
