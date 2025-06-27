from engine.contexts.context import Context
from typing import Callable


class MapContext(Context):
    """
    Context for when the player opens a map in order to travel
    :param parent_context (Context): Context from which this map context was entered
    :param context_data (dict): The map context data (e.g. below)
    >>> context_data =
    ...{
    ...     'map_domain_name': 'Sillytown',
    ...     'player_global_location': 'oldvale_sillytown_inn',
    ...     'map_level': 'local',
    ...     'map_locality': 'oldvale_sillytown',
    ...     'map_region': 'oldvale',
    ...     'map_contained_locations':
    ...         {
    ...             1: {
    ...                     'display_name': 'Town Hall',
    ...                     'global_location': 'oldvale_sillytown_townhall'
    ...                },
    ...             2: {
    ...                     'display_name': 'Inn',
    ...                     'global_location': 'oldvale_sillytown_inn'
    ...                }
    ...         }
    ...}
    """
    def __init__(self, parent_context: Context, context_data: dict):
        super().__init__(parent_context=parent_context,
                         context_type='map',
                         context_data=context_data)
        self.entry_text = f'Locations in {context_data["map_domain_name"]}'

    def _generate_choice_handling(self) -> dict[str, Callable[[Context, Context], bool]]:
        context_data = self.get_context_data()
        choice_handlers = {}

        def helper_local_travel(i: int) -> Callable[[Context, Context], bool]:
            new_global_location = context_data['map_contained_locations'][i]['global_location']

            def location_changer(curr_context: Context, parent_context: Context):
                parent_context.context_data['player_global_location'] = new_global_location
                curr_context.context_data['player_global_location'] = new_global_location
                return True
            return location_changer

        for choice_number in context_data['map_contained_locations']:
            choice_handlers[str(choice_number)] = helper_local_travel(choice_number)

        choice_handlers['back'] = self.exit_context_with_no_action()

        return choice_handlers
