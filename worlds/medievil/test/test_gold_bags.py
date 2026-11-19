"""
Tests for the gold_bag_1/2/3 options: every gold count is a real item in the datapackage, so the name the server and
client look up by id says the right amount.
"""

from . import MedievilTestBase
from ..Items import GOLD_MAX, GOLD_M_CODE_OFFSET, MedievilItem
from .. import MedievilWorld


def gold_bag_names(test: MedievilTestBase) -> set:
    return {item.name for item in test.multiworld.itempool if item.name.startswith("Gold Coins (") and item.player == test.player}


class GoldDatapackageTest(MedievilTestBase):
    def test_every_count_is_a_unique_item(self) -> None:
        ids = MedievilItem.get_name_to_id()
        gold = {name: code for name, code in ids.items() if name.startswith("Gold Coins (")}
        self.assertEqual(len(gold), GOLD_MAX)
        self.assertEqual(len(set(ids.values())), len(ids))
        self.assertEqual(MedievilWorld.item_name_to_id["Gold Coins (777)"], 9901000 + GOLD_M_CODE_OFFSET + 777)

    def test_id_resolves_back_to_the_same_name(self) -> None:
        id_to_name = {code: name for name, code in MedievilWorld.item_name_to_id.items()}
        self.assertEqual(id_to_name[MedievilWorld.item_name_to_id["Gold Coins (777)"]], "Gold Coins (777)")


class GoldBagsDefaultTest(MedievilTestBase):
    def test_defaults(self) -> None:
        options = self.world.options
        self.assertEqual((options.gold_bag_1.value, options.gold_bag_2.value, options.gold_bag_3.value), (50, 100, 150))

    def test_pool_only_has_default_counts(self) -> None:
        self.assertTrue(gold_bag_names(self) <= {"Gold Coins (50)", "Gold Coins (100)", "Gold Coins (150)"})


class GoldBagsCustomTest(MedievilTestBase):
    options = {"gold_bag_1": 25, "gold_bag_2": 777, "gold_bag_3": 1000}

    def test_pool_uses_custom_counts(self) -> None:
        names = gold_bag_names(self)
        self.assertTrue(names)
        self.assertTrue(names <= {"Gold Coins (25)", "Gold Coins (777)", "Gold Coins (1000)"})

    def test_item_code_matches_datapackage_name(self) -> None:
        id_to_name = {code: name for name, code in MedievilWorld.item_name_to_id.items()}
        for item in self.multiworld.itempool:
            if item.player == self.player:
                self.assertEqual(id_to_name[item.code], item.name)

    def test_slot_data_has_the_counts(self) -> None:
        self.assertEqual(self.world.fill_slot_data()["options"]["gold_bag_2"], 777)


class GoldBagZeroTest(MedievilTestBase):
    options = {"gold_bag_2": 0}

    def test_zero_bag_is_not_in_the_pool(self) -> None:
        names = gold_bag_names(self)
        self.assertIn("Gold Coins (50)", names)
        self.assertIn("Gold Coins (150)", names)
        self.assertNotIn("Gold Coins (100)", names)

    def test_filler_is_a_bag_that_is_in_the_pool(self) -> None:
        self.assertEqual(self.world.get_filler_item_name(), "Gold Coins (50)")


class GoldBagAllZeroTest(MedievilTestBase):
    options = {"gold_bag_1": 0, "gold_bag_2": 0, "gold_bag_3": 0}

    def test_no_gold_in_the_pool_and_it_still_fills(self) -> None:
        self.assertEqual(gold_bag_names(self), set())
        self.assertEqual(len(self.multiworld.itempool), len(self.multiworld.get_unfilled_locations(self.player)))
