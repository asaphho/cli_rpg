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
		self.world_display_name = world_display_name.strip()
		self.regions: list[tuple[str, str]] = [(first_region_name.strip(), first_region_display_name.strip())]
		self.localities: dict[str, dict[str, str]] = {
    	  			'_'.join([first_region_name.strip(), first_locality_name.strip()]) :
    	  				{
    	  					'display_name': first_locality_display_name.strip(),
    	  					'entrypoint_global_location': '_'.join([first_region_name.strip(), first_locality_name.strip(), first_locality_entrypoint_name.strip()]),
    	  					'entrypoint_display_name': first_locality_entrypoint_display_name.strip()
    	  				}
    	  		}
    	  	
		self.locations: list[tuple[str, str]] = [('_'.join([first_region_name.strip(), first_locality_name.strip(), first_locality_entrypoint_name.strip()]), first_locality_entrypoint_display_name.strip())]

	def get_world_display_name(self) -> str:
		return self.world_display_name
    	  
	def get_region_names(self) -> list[str]:
		return [tup[0] for tup in self.regions]
    
	def get_region_names_and_display_names(self) -> list[tuple[str, str]]:
		return self.regions 
    
	def get_localities(self) -> dict[str, dict[str, str]]:
		return self.localities 
    
	def get_locality_global_locations(self) -> list[str]:
		return list(self.get_localities().keys())
