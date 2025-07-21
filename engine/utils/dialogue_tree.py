class DialogueTree:

    def __init__(self, entry_text: str):
        self.entry_text: str = entry_text
        self.dialogue_paths: dict[str, tuple[str, str]] = {}

    def add_node(self, node_name: str, player_line: str, response: str,
                 from_node: str = None):
        if '_' in node_name:
            raise ValueError('Node names cannot have underscores.')
        if node_name.strip() == '':
            raise ValueError('Node name cannot be blank.')
        full_node_name = node_name.strip() if from_node is None else f'{from_node}_{node_name.strip()}'
        if full_node_name in self.dialogue_paths.keys():
            raise ValueError(f'Node path {full_node_name} already taken.')
        self.dialogue_paths[full_node_name] = (player_line, response)


