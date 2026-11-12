"""
Tests for the knights_to_find option: Knights of Gallowmere are needed to defeat Zarok in open progression.
The lair itself stays enterable so its items can be collected.
"""

from . import MedievilTestBase
from ..Items import KNIGHT_ITEM_NAME
from ..Options import ProgressionOptions

FIVE_LIFE_BOTTLES = [
    "Life Bottle: Dan's Crypt",
    "Life Bottle: The Graveyard",
    "Life Bottle: Scarecrow Fields",
    "Life Bottle: Pools of the Ancient Dead",
    "Life Bottle: The Time Device",
]


def knight_count(test: MedievilTestBase) -> int:
    return sum(1 for item in test.multiworld.itempool if item.name == KNIGHT_ITEM_NAME and item.player == test.player)


class KnightsDefaultTest(MedievilTestBase):
    options = {"progression_option": ProgressionOptions.OPEN}

    def test_default_is_eight(self) -> None:
        self.assertEqual(self.world.options.knights_to_find.value, 8)

    def test_knights_are_in_the_pool(self) -> None:
        self.assertEqual(knight_count(self), 8)

    def test_knight_is_progression(self) -> None:
        knight = next(item for item in self.multiworld.itempool if item.name == KNIGHT_ITEM_NAME)
        self.assertTrue(knight.advancement)

    def test_zaroks_lair_can_be_entered_without_knights(self) -> None:
        self.assertTrue(self.can_reach_entrance("Map -> Zaroks Lair"))
        self.assertTrue(self.can_reach_location("Equipment: Good Lightning - ZL"))

    def test_good_lightning_is_in_the_pool_not_locked(self) -> None:
        self.assertFalse(self.world.get_location("Equipment: Good Lightning - ZL").locked)
        self.assertEqual(len(self.get_items_by_name("Equipment: Good Lightning")), 1)

    def test_defeating_zarok_needs_every_knight(self) -> None:
        self.collect_by_name(FIVE_LIFE_BOTTLES)
        self.collect_by_name("Equipment: Good Lightning")
        self.collect_by_name("Equipment: Club")
        knights = self.get_items_by_name(KNIGHT_ITEM_NAME)
        self.collect(knights[:7])
        self.assertFalse(self.can_reach_location("Cleared: Zaroks Lair"))
        self.collect(knights[7:])
        self.assertTrue(self.can_reach_location("Cleared: Zaroks Lair"))

    def test_slot_data_has_the_count(self) -> None:
        self.assertEqual(self.world.fill_slot_data()["options"]["knights_to_find"], 8)


class KnightsZeroTest(MedievilTestBase):
    options = {"progression_option": ProgressionOptions.OPEN, "knights_to_find": 0}

    def test_no_knights_in_the_pool(self) -> None:
        self.assertEqual(knight_count(self), 0)

    def test_zarok_needs_no_knights(self) -> None:
        self.collect_by_name(FIVE_LIFE_BOTTLES)
        self.collect_by_name("Equipment: Good Lightning")
        self.collect_by_name("Equipment: Club")
        self.assertTrue(self.can_reach_location("Cleared: Zaroks Lair"))


class KnightsMaxTest(MedievilTestBase):
    options = {"progression_option": ProgressionOptions.OPEN, "knights_to_find": 100}

    def test_all_knights_in_the_pool(self) -> None:
        self.assertEqual(knight_count(self), 100)


class KnightsVanillaTest(MedievilTestBase):
    options = {"progression_option": ProgressionOptions.VANILLA, "knights_to_find": 8}

    def test_option_is_turned_off(self) -> None:
        self.assertEqual(self.world.options.knights_to_find.value, 0)
        self.assertEqual(knight_count(self), 0)
