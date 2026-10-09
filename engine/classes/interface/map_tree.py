class WorldMapNode:

    def __init__(self, name: str, display_name: str, level: str, parent):
        self.name = name
        self.display_name = display_name
        self.children: list[WorldMapNode] = []
        self.level = level
        self.parent = parent

    def get_children(self):
        return self.children

    def add_child(self, name: str, display_name: str):
        if self.level == 'world':
            child_level = 'region'
        elif self.level == 'region':
            child_level = 'locality'
        elif self.level == 'locality':
            child_level = 'location'
        else:
            raise Exception('Cannot add node at this level.')
        names = [child.name for child in self.get_children()]
        display_names = [child.display_name for child in self.get_children()]
        if name in names:
            raise ValueError(f'Node with name {name} already exists.')
        if display_name in display_names:
            raise ValueError(f'Node with display name {display_name} already exists.')
        self.children.append(WorldMapNode(name, display_name, child_level, self))

    def get_nodes_at_level(self):
        parent = self.parent
        if isinstance(parent, WorldMapNode):
            return parent.get_children()
        else:
            return [self]
