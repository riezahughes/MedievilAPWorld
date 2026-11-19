"""
Tests for the gold_bag_1/2/3 options: the three gold bag items keep their ids, and the count in the brackets of their
name comes from the options.
"""

from . import MedievilTestBase
from ..Items import MedievilItem


def gold_bag_names(test: MedievilTestBase) -> set:
    return {item.name for item in test.multiworld.itempool if item.name.startswith("Gold Coins (") and item.player == test.player}


class GoldBagsDefaultTest(MedievilTestBase):
    def test_defaults(self) -> None:
        options = self.world.options
        self.assertEqual((options.gold_bag_1.value, options.gold_bag_2.value, options.gold_bag_3.value), (50, 100, 150))

    def test_default_names_exist(self) -> None:
        ids = MedievilItem.get_name_to_id()
        self.assertEqual([ids["Gold Coins (50)"], ids["Gold Coins (100)"], ids["Gold Coins (150)"]], [9901000, 9901001, 9901002])

    def test_pool_only_has_default_counts(self) -> None:
        self.assertTrue(gold_bag_names(self) <= {"Gold Coins (50)", "Gold Coins (100)", "Gold Coins (150)"})

    def test_slot_data_has_the_counts(self) -> None:
        options = self.world.fill_slot_data()["options"]
        self.assertEqual((options["gold_bag_1"], options["gold_bag_2"], options["gold_bag_3"]), (50, 100, 150))


class GoldBagsCustomTest(MedievilTestBase):
    options = {"gold_bag_1": 25, "gold_bag_2": 777, "gold_bag_3": 9999}

    def test_items_are_renamed_but_keep_their_ids(self) -> None:
        for name, code in (("Gold Coins (50)", 9901000), ("Gold Coins (100)", 9901001), ("Gold Coins (150)", 9901002)):
            item = self.world.create_item(name)
            self.assertEqual(item.code, code)
        self.assertEqual(self.world.create_item("Gold Coins (50)").name, "Gold Coins (25)")
        self.assertEqual(self.world.create_item("Gold Coins (100)").name, "Gold Coins (777)")
        self.assertEqual(self.world.create_item("Gold Coins (150)").name, "Gold Coins (9999)")

    def test_pool_uses_custom_counts(self) -> None:
        names = gold_bag_names(self)
        self.assertTrue(names)
        self.assertTrue(names <= {"Gold Coins (25)", "Gold Coins (777)", "Gold Coins (9999)"})

    def test_slot_data_has_the_counts(self) -> None:
        self.assertEqual(self.world.fill_slot_data()["options"]["gold_bag_2"], 777)


class GoldBagZeroTest(MedievilTestBase):
    options = {"gold_bag_2": 0}

    def test_zero_bag_is_not_in_the_pool(self) -> None:
        names = gold_bag_names(self)
        self.assertIn("Gold Coins (50)", names)
        self.assertIn("Gold Coins (150)", names)
        self.assertNotIn("Gold Coins (0)", names)
        self.assertNotIn("Gold Coins (100)", names)

    def test_filler_is_a_bag_that_is_in_the_pool(self) -> None:
        self.assertEqual(self.world.get_filler_item_name(), "Gold Coins (50)")


class GoldBagAllZeroTest(MedievilTestBase):
    options = {"gold_bag_1": 0, "gold_bag_2": 0, "gold_bag_3": 0}

    def test_no_gold_in_the_pool_and_it_still_fills(self) -> None:
        self.assertEqual(gold_bag_names(self), set())
        self.assertEqual(len(self.multiworld.itempool), len(self.multiworld.get_unfilled_locations(self.player)))
