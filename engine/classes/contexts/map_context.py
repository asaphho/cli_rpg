from engine.classes.contexts.context import Context
from engine.classes.interface.map_tree import WorldMapNode


class MapContext(Context):

    def __init__(self, parent_context: Context, current_location: WorldMapNode):
        super().__init__(parent_context)
        self.current_node = current_location
        self.current_location = current_location
        self.context_type = 'map'

    def print_entry_text(self):
        current_level = self.current_node.level
        if current_level == 'location':
            print('Select a location to travel to.')
        elif current_level == 'locality':
            region_name = self.current_node.parent.display_name
            print(f'Places in {region_name}:')
        else:
            print('Regions:')

    def generate_choices(self) -> dict[str, str]:
        nodes_at_level = self.current_node.get_nodes_at_level()
        current_level = self.current_node.level
        choices = {}
        for i in range(len(nodes_at_level)):
            choices[str(i+1)] = nodes_at_level[i].display_name
        if current_level != 'region':
            choices['u'] = 'Go up one level'
        return choices

    def print_choices(self):
        for i in sorted(list(self.choices.keys())):
            print(f'{i}: {self.choices[i]}')
        self.choices['b'] = 'Back to game'
        print('b: Back to game')

    def handle_choice(self, choice: str) -> bool:
        chosen_choice = self.choices[choice]
        if chosen_choice == 'Go up one level':
            self.current_node = self.current_node.parent
            return False
        elif chosen_choice == 'Back to game':
            return True
        else:
            chosen_node = [node for node in self.current_node.get_nodes_at_level() if node.display_name == chosen_choice][0]
            current_level = self.current_node.level
            if current_level != 'location':
                self.current_node = chosen_node.get_children()[0]
                return False
            else:
                self.parent_context.data['location'] = chosen_node.name
                return True
