class DialogueTree:

    def __init__(self, entry_text: str):
        self.entry_text: str = entry_text
        self.dialogue_paths: dict[str, tuple[str, str]] = {}
        self.curr_node: str = ''

    def get_current_node(self) -> str:
        return self.curr_node

    def add_node(self, node_name: str, player_line: str, response: str,
                 from_node: str = None) -> None:
        if '_' in node_name:
            raise ValueError('Node names cannot have underscores.')
        if node_name.strip() == '':
            raise ValueError('Node name cannot be blank.')
        full_node_name = node_name.strip() if from_node is None else f'{from_node}_{node_name.strip()}'
        if full_node_name in self.dialogue_paths.keys():
            raise ValueError(f'Node path {full_node_name} already taken.')
        self.dialogue_paths[full_node_name] = (player_line, response)

    def replace_node(self, node_name: str, player_line: str, response: str,
                     from_node: str = None) -> None:
        full_node_name = f'{from_node}_{node_name.strip()}' if from_node is not None else node_name.strip()
        if full_node_name not in self.dialogue_paths.keys():
            raise ValueError(f'Node {full_node_name} does not exist.')
        self.dialogue_paths[full_node_name] = (player_line, response)

    def get_player_line(self, full_node_name: str) -> str:
        return self.dialogue_paths[full_node_name][0]

    def get_response(self, full_node_name: str) -> str:
        return self.dialogue_paths[full_node_name][1]

    def get_available_nodes(self) -> list[str]:
        all_nodes = list(self.dialogue_paths.keys())
        current_node = self.get_current_node()
        if current_node == '':
            return list(filter(lambda x: '_' not in x, all_nodes))
        return list(filter(lambda x: x.rsplit('_', maxsplit=1)[0] == current_node, all_nodes))

    def update_current_node(self, new_node_full_name: str):
        if new_node_full_name == '':
            self.curr_node = ''
            return
        if new_node_full_name not in self.dialogue_paths.keys():
            raise ValueError('Node does not exist.')
        self.curr_node = new_node_full_name

    def cut_branch(self, head_full_name: str):
        all_nodes: list[str] = list(self.dialogue_paths.keys())
        if head_full_name.strip() not in all_nodes:
            raise ValueError(f'Node does not exist.')
        nodes_to_remove = list(filter(lambda x: x.startswith(head_full_name.strip()), all_nodes))
        for node in nodes_to_remove:
            self.dialogue_paths.pop(node)

    def is_at_terminal_node(self) -> bool:
        return len(self.get_available_nodes()) == 0

    def export(self) -> dict[str, tuple[str, str]]:
        return self.dialogue_paths
