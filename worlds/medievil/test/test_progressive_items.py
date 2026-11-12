"""
Tests for the progressive_sword, progressive_bow and progressive_shield options. Each one swaps the weapons it covers
for one copy of its progressive item per weapon.
"""

from . import MedievilTestBase
from ..Items import progressive_groups, MedievilItem

ALL_OPTIONS = {"progressive_sword": 1, "progressive_bow": 1, "progressive_shield": 1}
PROGRESSIVE_NAMES = [name for _, name, _ in progressive_groups]
EXPECTED_COUNTS = {"Equipment: Progressive Sword": 3, "Equipment: Progressive Bow": 4, "Equipment: Progressive Shield": 3}


def pool_names(test: MedievilTestBase) -> list[str]:
    return [item.name for item in test.multiworld.itempool if item.player == test.player]


class ProgressiveOffTest(MedievilTestBase):
    def test_defaults_are_off(self) -> None:
        for option, _, _ in progressive_groups:
            self.assertEqual(getattr(self.world.options, option).value, 0)

    def test_base_weapons_stay_and_progressive_items_stay_out(self) -> None:
        names = pool_names(self)
        for _, progressive_name, members in progressive_groups:
            self.assertNotIn(progressive_name, names)
            for member in members:
                self.assertIn(member, names)


class ProgressiveAllTest(MedievilTestBase):
    options = ALL_OPTIONS

    def test_progressive_copies_match_the_weapons_they_replace(self) -> None:
        names = pool_names(self)
        for progressive_name, count in EXPECTED_COUNTS.items():
            self.assertEqual(names.count(progressive_name), count, progressive_name)

    def test_base_weapons_are_removed_from_the_pool(self) -> None:
        names = pool_names(self)
        for _, _, members in progressive_groups:
            for member in members:
                self.assertNotIn(member, names)

    def test_other_weapons_are_untouched(self) -> None:
        names = pool_names(self)
        for weapon in ("Equipment: Club", "Equipment: Hammer", "Equipment: Daggers", "Equipment: Axe", "Equipment: Spear"):
            self.assertIn(weapon, names)

    def test_progressive_items_have_unique_ids(self) -> None:
        ids = MedievilItem.get_name_to_id()
        self.assertEqual(len({ids[name] for name in PROGRESSIVE_NAMES}), len(PROGRESSIVE_NAMES))
        self.assertEqual(len(set(ids.values())), len(ids))

    def test_slot_data_has_the_options(self) -> None:
        options = self.world.fill_slot_data()["options"]
        for option, _, _ in progressive_groups:
            self.assertEqual(options[option], 1)

    def test_ranged_location_needs_a_bow(self) -> None:
        everything_but_ranged = PROGRESSIVE_NAMES + ["Equipment: Daggers", "Equipment: Axe", "Equipment: Spear", "Equipment: Lightning"]
        self.collect_all_but(everything_but_ranged)
        self.assertFalse(self.can_reach_location("Cleared: The Hilltop Mausoleum"))
        self.collect_by_name(["Equipment: Progressive Bow"])
        self.assertTrue(self.can_reach_location("Cleared: The Hilltop Mausoleum"))


class ProgressiveSwordOnlyTest(MedievilTestBase):
    options = {"progressive_sword": 1}

    def test_only_the_sword_is_swapped(self) -> None:
        names = pool_names(self)
        self.assertEqual(names.count("Equipment: Progressive Sword"), 3)
        self.assertNotIn("Equipment: Small Sword", names)
        self.assertIn("Equipment: Crossbow", names)
        self.assertIn("Equipment: Copper Shield", names)
        self.assertNotIn("Equipment: Progressive Bow", names)
