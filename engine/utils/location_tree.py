class LocationTree:
    """
	Object to store and retrieve information on regions, localities, locations within localities
	:param world_display_name (str): The display name for the world the game is to be set in
	:param first_region_display_name (str): The display name for the first region
	:param first_region_name (str): Name of the region
	:param first_locality_display_name (str): Display name for the first locality in the first region
	:param first_locality_name (str): Name of the first locality
	:param first_locality_entrypoint_display_name (str): Display name of the default entrypoint of the first locality
	:param first_locality_entrypoint_name (str): Name of the default entrypoint location
	"""

    def __init__(self, world_display_name: str,
                 first_region_display_name: str,
                 first_region_name: str,
                 first_locality_display_name: str,
                 first_locality_name: str,
                 first_locality_entrypoint_display_name: str,
                 first_locality_entrypoint_name: str):
        if '_' in first_region_name:
            raise ValueError('Region names cannot have underscores.')
        if '_' in first_locality_name:
            raise ValueError('Locality names cannot have underscores.')
        if '_' in first_locality_entrypoint_name:
            raise ValueError('Location names cannot have underscores.')
        if any([s.strip() == '' for s in (world_display_name, first_region_display_name, first_region_name,
                                          first_locality_display_name, first_locality_name,
                                          first_locality_entrypoint_display_name, first_locality_entrypoint_name)]):
            raise ValueError('Arguments cannot be empty string/whitespace-only.')
        self.world_display_name = world_display_name.strip()
        self.regions: list[list[str]] = [[first_region_name.strip(), first_region_display_name.strip()]]
        self.localities: dict[str, dict[str, str]] = {
            '_'.join([first_region_name.strip(), first_locality_name.strip()]):
                {
                    'display_name': first_locality_display_name.strip(),
                    'entrypoint_global_location': '_'.join([first_region_name.strip(), first_locality_name.strip(),
                                                            first_locality_entrypoint_name.strip()]),
                    'entrypoint_display_name': first_locality_entrypoint_display_name.strip()
                }
        }

        self.locations: list[list[str]] = [['_'.join(
            [first_region_name.strip(), first_locality_name.strip(), first_locality_entrypoint_name.strip()]),
            first_locality_entrypoint_display_name.strip()]]

    def get_world_display_name(self) -> str:
        return self.world_display_name

    def get_region_names(self) -> list[str]:
        return [tup[0] for tup in self.regions]

    def get_region_names_and_display_names(self) -> list[list[str]]:
        return self.regions

    def get_localities(self) -> dict[str, dict[str, str]]:
        return self.localities

    def get_locality_global_locations(self) -> list[str]:
        return list(self.get_localities().keys())

    def get_lowest_level_locations(self) -> list[list[str]]:
        return self.locations

    def add_region(self, region_name: str,
                   region_display_name: str,
                   first_locality_name: str,
                   first_locality_display_name: str,
                   first_locality_entrypoint_name: str,
                   first_locality_entrypoint_display_name: str) -> None:
        if '_' in region_name:
            raise ValueError('Underscore not allowed in region name.')
        if '_' in first_locality_name:
            raise ValueError('Underscore not allowed in locality name.')
        if '_' in first_locality_entrypoint_name:
            raise ValueError('Underscore not allowed in location name.')
        if any([string.strip() == '' for string in (region_name, region_display_name, first_locality_name,
                                                    first_locality_display_name, first_locality_entrypoint_name,
                                                    first_locality_entrypoint_display_name)]):
            raise ValueError('Name or display name cannot be empty/whitespace-only.')
        region_names_and_display_names = self.get_region_names_and_display_names()
        if any([ls[0] == region_name.strip() for ls in region_names_and_display_names]):
            raise ValueError(f'{region_name.strip()} already exists.')
        if any([ls[1] == region_display_name.strip() for ls in region_names_and_display_names]):
            raise ValueError(f'{region_display_name.strip()} already taken as a display name.')
        self.regions.append([region_name.strip(), region_display_name.strip()])
        new_locality_global_location = '_'.join([region_name.strip(), first_locality_name.strip()])
        entrypoint_global_location = '_'.join([new_locality_global_location, first_locality_entrypoint_name.strip()])
        self.localities[new_locality_global_location] = {
            'display_name': first_locality_display_name.strip(),
            'entrypoint_global_location': entrypoint_global_location,
            'entrypoint_display_name': first_locality_entrypoint_display_name.strip()
        }
        self.locations.append([entrypoint_global_location, first_locality_entrypoint_display_name.strip()])

    def add_locality(self, locality_global_location: str,
                     locality_display_name: str,
                     entrypoint_name: str,
                     entrypoint_display_name: str) -> None:
        if len(locality_global_location.split('_')) != 2:
            raise ValueError('locality_global_location argument must conform to region_locality form.')
        region, locality = [s.strip() for s in locality_global_location.split('_')]
        if region == '' or locality == '':
            raise ValueError('Region or locality cannot be empty.')
        if any([s.strip() == '' for s in (locality_display_name, entrypoint_name, entrypoint_display_name)]):
            raise ValueError('Empty/whitespace-only string detected in arguments.')
        if '_' in entrypoint_name:
            raise ValueError('Entrypoint name cannot have underscores.')
        if region not in self.get_region_names():
            raise ValueError(f'Region {region} does not currently exist.')
        localities = self.get_localities()
        if f'{region}_{locality}' in localities:
            raise ValueError(f'Locality of name {locality} in region {region} already exists.')
        locality_display_names_in_region: list[str] = [localities[loc]['display_name'] for loc in localities
                                                       if loc.split('_')[0] == region]
        if locality_display_name.strip() in locality_display_names_in_region:
            raise ValueError(f'Display name {locality_display_name.strip()} in region {region} already taken.')

        entrypoint_global_location = '_'.join([region, locality, entrypoint_name.strip()])
        self.localities[f'{region}_{locality}'] = {
            'display_name': locality_display_name.strip(),
            'entrypoint_global_location': entrypoint_global_location,
            'entrypoint_display_name': entrypoint_display_name.strip()
        }
        self.locations.append([entrypoint_global_location, entrypoint_display_name.strip()])
