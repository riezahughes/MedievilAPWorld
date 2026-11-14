"""
Tests for the life_bottles option: one "Life Bottle" item goes into the pool per bottle asked for, and defeating Zarok
needs 5 of them (or all of them when fewer than 5 are in the pool).
"""

from . import MedievilTestBase
from ..Items import LIFE_BOTTLE_ITEM_NAME, item_dictionary
from ..Options import ProgressionOptions

ZAROK_WEAPONS = ["Equipment: Club", "Equipment: Good Lightning"]


def zarok_rule_met(test: MedievilTestBase) -> bool:
    """Only the "Cleared: Zaroks Lair" rule itself, not whether the lair can be reached."""
    return bool(test.world.get_location("Cleared: Zaroks Lair").access_rule(test.multiworld.state))


def life_bottle_count(test: MedievilTestBase) -> int:
    return sum(1 for item in test.multiworld.itempool if item.name == LIFE_BOTTLE_ITEM_NAME and item.player == test.player)


class LifeBottlesDefaultTest(MedievilTestBase):
    options = {"progression_option": ProgressionOptions.OPEN, "knights_to_find": 0}

    def test_default_is_nine(self) -> None:
        self.assertEqual(self.world.options.life_bottles.value, 9)
        self.assertEqual(life_bottle_count(self), 9)

    def test_old_named_life_bottles_are_gone(self) -> None:
        self.assertEqual([name for name in item_dictionary if name.startswith("Life Bottle:")], [])

    def test_life_bottle_is_progression(self) -> None:
        bottle = next(item for item in self.multiworld.itempool if item.name == LIFE_BOTTLE_ITEM_NAME)
        self.assertTrue(bottle.advancement)

    def test_zarok_needs_five(self) -> None:
        self.collect_by_name(ZAROK_WEAPONS)
        bottles = self.get_items_by_name(LIFE_BOTTLE_ITEM_NAME)
        self.collect(bottles[:4])
        self.assertFalse(zarok_rule_met(self))
        self.collect(bottles[4:5])
        self.assertTrue(zarok_rule_met(self))

    def test_slot_data_has_the_count(self) -> None:
        self.assertEqual(self.world.fill_slot_data()["options"]["life_bottles"], 9)


class LifeBottlesTenTest(MedievilTestBase):
    options = {"progression_option": ProgressionOptions.OPEN, "knights_to_find": 0, "life_bottles": 10}

    def test_ten_in_the_pool(self) -> None:
        self.assertEqual(life_bottle_count(self), 10)


class LifeBottlesFewerThanFiveTest(MedievilTestBase):
    options = {"progression_option": ProgressionOptions.OPEN, "knights_to_find": 0, "life_bottles": 2}

    def test_two_in_the_pool(self) -> None:
        self.assertEqual(life_bottle_count(self), 2)

    def test_zarok_needs_every_bottle_in_the_pool(self) -> None:
        self.collect_by_name(ZAROK_WEAPONS)
        bottles = self.get_items_by_name(LIFE_BOTTLE_ITEM_NAME)
        self.collect(bottles[:1])
        self.assertFalse(zarok_rule_met(self))
        self.collect(bottles[1:])
        self.assertTrue(zarok_rule_met(self))


class LifeBottlesZeroTest(MedievilTestBase):
    options = {"progression_option": ProgressionOptions.OPEN, "knights_to_find": 0, "life_bottles": 0}

    def test_none_in_the_pool(self) -> None:
        self.assertEqual(life_bottle_count(self), 0)

    def test_zarok_needs_no_bottles(self) -> None:
        self.collect_by_name(ZAROK_WEAPONS)
        self.assertTrue(zarok_rule_met(self))
