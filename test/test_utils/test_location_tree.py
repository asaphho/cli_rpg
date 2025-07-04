from engine.utils.location_tree import LocationTree


def compare_lists(list1: list[list[str]], list2: list[list[str]]) -> None:
    assert sorted(list1, key=lambda x: x[0]) == sorted(list2, key=lambda x:x[0])


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


def test_add_region():
    location_tree = LocationTree(world_display_name='Mundus',
                                 first_region_display_name='Eastmarch',
                                 first_region_name='eastmarch',
                                 first_locality_display_name='Bridgefort',
                                 first_locality_name='bridgefort',
                                 first_locality_entrypoint_display_name='Bridgefort Gates',
                                 first_locality_entrypoint_name='gates')
    location_tree.add_region(region_name='westmarch',
                             region_display_name='Westmarch',
                             first_locality_name='skirge',
                             first_locality_display_name='Skirge',
                             first_locality_entrypoint_name='square',
                             first_locality_entrypoint_display_name='Town Square')
    assert set(location_tree.get_region_names()) == {'eastmarch', 'westmarch'}
    expected_region_and_display_names = [['eastmarch', 'Eastmarch'], ['westmarch', 'Westmarch']]
    compare_lists(location_tree.get_region_names_and_display_names(), expected_region_and_display_names)
    assert location_tree.get_localities() == {
        'eastmarch_bridgefort': {
            'display_name': 'Bridgefort',
            'entrypoint_global_location': 'eastmarch_bridgefort_gates',
            'entrypoint_display_name': 'Bridgefort Gates'
        },
        'westmarch_skirge': {
            'display_name': 'Skirge',
            'entrypoint_global_location': 'westmarch_skirge_square',
            'entrypoint_display_name': 'Town Square'
        }
    }
    expected_lowest_level_locations = [['eastmarch_bridgefort_gates', 'Bridgefort Gates'], ['westmarch_skirge_square', 'Town Square']]
    compare_lists(location_tree.get_lowest_level_locations(), expected_lowest_level_locations)
