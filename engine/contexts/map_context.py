from engine.contexts.context import Context
from engine.utils.location_tree import LocationTree
from typing import Callable
from engine.utils.choice_handler import ChoiceHandler


class MapContext(Context):
    """
    Context for when the player opens a map in order to travel
    :param parent_context (Context): Context from which this map context was entered
    :param context_data (dict): The map context data (e.g. below)
    :param known_locations (LocationTree): LocationTree containing all locations in the world known to the player
    >>> context_data = \
    ...{
    ...     'map_domain_name': 'Sillytown',
    ...     'player_global_location': 'oldvale_sillytown_inn',
    ...     'map_level': 'local', # 'world', 'regional', or 'local' only
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
    def __init__(self, parent_context: Context, context_data: dict, known_locations: LocationTree):
        super().__init__(parent_context=parent_context,
                         context_type='map',
                         context_data=context_data)
        self.entry_text = f'Locations in {context_data["map_domain_name"]}' if context_data['map_level'] == 'local' or\
                                                                               context_data['map_level'] == 'regional'\
            else f'Regions in {context_data["map_domain_name"]}'
        self.known_locations = known_locations

    def _generate_choice_handling(self) -> ChoiceHandler:
        context_data = self.get_context_data()
        choice_handler = ChoiceHandler(reserved_choices=[('b', 'Back')])

        def helper_local_travel(i: int) -> Callable[[Context, Context], bool]:
            new_global_location = context_data['map_contained_locations'][i]['global_location']

            def location_changer(curr_context: Context, parent_context: Context):
                parent_context.context_data['player_global_location'] = new_global_location
                curr_context.context_data['player_global_location'] = new_global_location
                return True
            return location_changer

        if context_data['map_level'] in ('local', 'regional'):
            for choice_number in context_data['map_contained_locations']:
                choice_handler.add_choice(executor=helper_local_travel(choice_number),
                                          display_text=context_data['map_contained_locations'][choice_number]['display_name'])
            if context_data['map_level'] == 'local':
                region: str = context_data['map_region']
                choice_handler.add_choice(executor=self.create_nested_map_handler(location=region),
                                          display_text='Region map',
                                          choice_letter='r')
            choice_handler.add_choice(executor=self.create_nested_map_handler(location='world'),
                                      display_text='World map',
                                      choice_letter='w')
        else:
            for choice_number in context_data['map_contained_locations']:
                region: str = context_data['map_contained_locations'][choice_number]['global_location']
                choice_handler.add_choice(executor=self.create_nested_map_handler(location=region),
                                          display_text=context_data['map_contained_locations'][choice_number]['display_name'])

        return choice_handler

    def create_map_context_data(self, location: str) -> dict:
        map_context_data = {'player_global_location': self.get_context_data()['player_global_location'],
                            'map_contained_locations': {}}
        known_locations: LocationTree = self.known_locations
        region_names_and_display_names = known_locations.get_region_names_and_display_names()
        if location == 'world':
            map_context_data['map_domain_name'] = known_locations.get_world_display_name()
            map_context_data['map_level'] = 'world'
            for i in range(1, len(region_names_and_display_names) + 1):
                map_context_data['map_contained_locations'][i] = {'display_name': region_names_and_display_names[i-1][1],
                                                                  'global_location': region_names_and_display_names[i-1][0]}
        else:
            for ls in region_names_and_display_names:
                if ls[0] == location:
                    map_context_data['map_domain_name'] = ls[1]
                    break
            map_context_data['map_level'] = 'regional'
            map_context_data['map_region'] = location
            i = 1
            localities = known_locations.get_localities()
            for locality in localities:
                if locality.startswith(f'{location}_'):
                    map_context_data['map_contained_locations'][i] = {'display_name': localities[locality]['display_name'],
                                                                      'global_location': localities[locality]['entrypoint_global_location']}
                    i += 1
        return map_context_data

    def create_nested_map_handler(self, location: str) -> Callable[[Context, Context], bool]:

        def nested_map_handler(curr_context: Context, parent_context: Context) -> bool:
            curr_context.context_data = self.create_map_context_data(location)
            return False

        return nested_map_handler

