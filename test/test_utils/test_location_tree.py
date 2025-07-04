from engine.utils.location_tree import LocationTree


def test_location_tree_initialization():
    location_tree = LocationTree(world_display_name='Mundus',
                                 first_region_display_name='Eastmarch',
                                 first_region_name='eastmarch',
                                 first_locality_display_name='Bridgefort',
                                 first_locality_name='bridgefort',
                                 first_locality_entrypoint_display_name='Bridgefort Gates',
                                 first_locality_entrypoint_name='gates')
    assert location_tree.world_display_name == 'Mundus'
    assert location_tree.regions == [['eastmarch', 'Eastmarch']]
    assert location_tree.localities == {
        'eastmarch_bridgefort': {
            'display_name': 'Bridgefort',
            'entrypoint_global_location': 'eastmarch_bridgefort_gates',
            'entrypoint_display_name': 'Bridgefort Gates'
        }
    }
    assert location_tree.lowest_level_locations == [['eastmarch_bridgefort_gates', 'Bridgefort Gates']]
