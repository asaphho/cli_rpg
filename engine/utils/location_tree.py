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

        self.lowest_level_locations: list[list[str]] = [['_'.join(
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
        return self.lowest_level_locations

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
        self.lowest_level_locations.append([entrypoint_global_location, first_locality_entrypoint_display_name.strip()])

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
        self.lowest_level_locations.append([entrypoint_global_location, entrypoint_display_name.strip()])

    def add_lowest_level_location(self, global_location: str, display_name: str) -> None:
        if len(global_location.split('_')) != 3:
            raise ValueError('global_location must conform to region_locality_lowest-level-location form.')
        region, locality, location_name = [s.strip() for s in global_location.split('_')]
        if '_'.join([region, locality, location_name]) in [ls[0] for ls in self.get_lowest_level_locations()]:
            raise ValueError('Location already exists.')
        if region not in self.get_region_names():
            raise ValueError(f'Region {region} does not exist.')
        if f'{region}_{locality}' not in self.get_locality_global_locations():
            raise ValueError(f'Locality {locality} does not exist in region {region}.')
        if location_name.strip() == '' or display_name.strip() == '':
            raise ValueError('Location name or display name cannot be empty.')
        display_names_in_locality = [ls[1] for ls in self.get_lowest_level_locations() if ls[0].startswith(f'{region}_{locality}_')]
        if display_name.strip() in display_names_in_locality:
            raise ValueError(f'Display name {display_name.strip()} in {region}_{locality} already taken.')
        self.lowest_level_locations.append(['_'.join([region, locality, location_name]), display_name.strip()])

    def remove_region(self, region_name: str) -> None:
        if region_name.strip() not in self.get_region_names():
            raise ValueError(f'Region {region_name.strip()} does not exist.')
        if len(self.get_region_names()) == 1:
            raise ValueError('Cannot remove the only region in the world.')
        self.regions: list[list[str]] = list(filter(lambda x: x[0] != region_name.strip(), self.regions))
        localities: list[str] = self.get_locality_global_locations()
        for locality in localities:
            if locality.startswith(f'{region_name.strip()}_'):
                self.localities.pop(locality)
        self.lowest_level_locations: list[list[str]] = list(filter(lambda x: not x[0].startswith(f'{region_name.strip()}_'),
                                                                   self.lowest_level_locations))

    def remove_locality(self, locality_global_location: str) -> None:
        localities: list[str] = self.get_locality_global_locations()
        if locality_global_location.strip() not in localities:
            raise ValueError(f'No such locality exists')
        region = locality_global_location.split('_')[0]
        localities_in_region: list[str] = list(filter(lambda x: x.startswith(f'{region}_'), localities))
        if len(localities_in_region) == 1:
            raise ValueError('Cannot remove only locality in region.')
        self.localities.pop(locality_global_location.strip())
        self.lowest_level_locations = list(filter(lambda x: not x[0].startswith(f'{locality_global_location.strip()}_'),
                                                  self.lowest_level_locations))

    def remove_lowest_level_location(self, global_location: str) -> None:
        lowest_level_locations = [ls[0] for ls in self.lowest_level_locations]
        if global_location.strip() not in lowest_level_locations:
            raise ValueError(f'Location {global_location.strip()} does not exist.')
        locality_global_location = global_location.strip().rsplit('_', maxsplit=1)[0]
        if global_location.strip() == self.localities[locality_global_location]['entrypoint_global_location']:
            raise ValueError('Cannot remove the locality entrypoint.')
        self.lowest_level_locations = list(filter(lambda x: x[0] != global_location.strip(),
                                                  self.lowest_level_locations))

    def change_display_name(self, global_location: str, new_display_name: str) -> None:
        if new_display_name.strip() == '':
            raise ValueError('Empty display name disallowed.')
        if (location_level := len(global_location.split('_'))) not in (1, 2, 3):
            raise ValueError('Cannot parse global_location: Too many underscores.')
        elif location_level == 1:
            region = global_location.strip()
            if region not in self.get_region_names():
                raise ValueError(f'Region {region} does not exist.')
            existing_display_names = [ls[1] for ls in self.get_region_names_and_display_names() if ls[0] != region]
            if new_display_name.strip() in existing_display_names:
                raise ValueError(f'Display name {new_display_name.strip()} already taken.')
            for i in range(len(self.get_region_names_and_display_names())):
                if self.regions[i][0] == region:
                    self.regions[i][1] = new_display_name.strip()
                    break
        elif location_level == 2:
            locality_global_location = global_location.strip()
            localities = self.get_locality_global_locations()
            if locality_global_location not in localities:
                raise ValueError(f'Locality {locality_global_location} does not exist.')
            region = locality_global_location.split('_')[0]
            display_names_in_region = [self.get_localities()[loc]['display_name'] for loc in localities
                                       if loc.startswith(f'{region}_') and loc != locality_global_location]
            if new_display_name.strip() in display_names_in_region:
                raise ValueError(f'Display name {new_display_name.strip()} in region {region} already taken.')
            self.localities[locality_global_location]['display_name'] = new_display_name.strip()
        else:
            global_location_to_rename = global_location.strip()
            lowest_level_locations = self.get_lowest_level_locations()
            if global_location_to_rename not in [ls[0] for ls in lowest_level_locations]:
                raise ValueError(f'Location {global_location_to_rename} does not exist.')
            locality_global_location = global_location_to_rename.rsplit('_', maxsplit=1)[0]
            locations_in_locality: list[list[str]] = [ls for ls in lowest_level_locations
                                                      if ls[0].startswith(f'{locality_global_location}_')]
            display_names_in_locality: list[str] = [ls[1] for ls in locations_in_locality
                                                    if ls[0] != global_location_to_rename]
            if new_display_name.strip() in display_names_in_locality:
                raise ValueError(f'Display name {new_display_name.strip()} in locality\
{locality_global_location} already taken.')
            for i in range(len(self.lowest_level_locations)):
                if self.lowest_level_locations[i][0] == global_location_to_rename:
                    self.lowest_level_locations[i][1] = new_display_name.strip()
                    break
            if self.localities[locality_global_location]['entrypoint_global_location'] == global_location_to_rename:
                self.localities[locality_global_location]['entrypoint_display_name'] = new_display_name.strip()

    def change_locality_entrypoint(self, locality_global_location: str, new_entrypoint_global_location: str) -> None:
        localities = self.get_localities()
        if locality_global_location.strip() not in localities:
            raise ValueError(f'Locality {locality_global_location.strip()} does not exist.')
        locations_in_locality: list[list[str]] = list(filter(lambda x: x[0].startswith(f'{locality_global_location}_'),
                                                             self.get_lowest_level_locations()))
        if new_entrypoint_global_location.strip() not in [ls[0] for ls in locations_in_locality]:
            raise ValueError(f'Location {new_entrypoint_global_location.strip()} does not exist.')
        new_entrypoint_display_name = locations_in_locality[0][1]
        for ls in locations_in_locality:
            if ls[0] == new_entrypoint_global_location.strip():
                new_entrypoint_display_name = ls[1]
                break
        self.localities[locality_global_location.strip()]['entrypoint_global_location'] = new_entrypoint_global_location.strip()
        self.localities[locality_global_location.strip()]['entrypoint_display_name'] = new_entrypoint_display_name

