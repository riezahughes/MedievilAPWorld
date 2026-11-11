"""
Tests for ShopSanity: Merchant Gargoyle shop locations, their prices, rules and slot data.
"""

from . import MedievilTestBase
from ..Locations import shop_tables, shop_location_names, MedievilLocation, SHOP_PRICE_MIN, SHOP_PRICE_MAX, SHOP_MENU_ROWS
from ..Options import ProgressionOptions, ShopSanityItemsPerShop


def shop_names(count: int = ShopSanityItemsPerShop.default) -> list:
    return [name for shop in shop_tables for name in shop_location_names(shop, count)]


SHOP_NAMES = shop_names()


class ShopSanityOffTest(MedievilTestBase):
    options = {"shopsanity": 0}

    def test_no_shop_locations_created(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertFalse(names & set(SHOP_NAMES))

    def test_slot_data_has_empty_stock(self) -> None:
        self.assertEqual(self.world.fill_slot_data()["shop_stock"], {})


class ShopSanityOnTest(MedievilTestBase):
    options = {
        "shopsanity": 1,
        "progression_option": ProgressionOptions.OPEN,
    }

    def test_every_shop_gets_its_items(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        for name in SHOP_NAMES:
            self.assertIn(name, names)

    def test_shop_ids_dont_clash_with_other_locations(self) -> None:
        ids = MedievilLocation.get_name_to_id()
        self.assertEqual(len(ids), len(set(ids.values())))

    def test_option_limit_matches_the_shop_menu(self) -> None:
        # the SECOND HAND GOODS section of the shop menu has 11 rows
        self.assertEqual(ShopSanityItemsPerShop.range_end, SHOP_MENU_ROWS)

    def test_only_the_chosen_number_of_items(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertFalse(names & (set(shop_names(SHOP_MENU_ROWS)) - set(SHOP_NAMES)))

    def test_prices_in_range(self) -> None:
        for name in SHOP_NAMES:
            price = self.world.shop_prices[name]
            self.assertTrue(SHOP_PRICE_MIN <= price <= SHOP_PRICE_MAX, f"{name} costs {price}")
            self.assertEqual(price % 10, 0)

    def test_slot_data_stock(self) -> None:
        stock = self.world.fill_slot_data()["shop_stock"]
        self.assertEqual(set(stock), {str(shop.level_id) for shop in shop_tables})
        for shop in shop_tables:
            entries = stock[str(shop.level_id)]
            names = shop_location_names(shop, ShopSanityItemsPerShop.default)
            self.assertEqual(len(entries), len(names))
            for entry, name in zip(entries, names):
                self.assertEqual(entry["id"], self.world.location_name_to_id[name])
                self.assertEqual(entry["price"], self.world.shop_prices[name])

    def test_no_progression_in_shops(self) -> None:
        key_item = self.world.create_item("Key Item: Skull Key")
        filler = self.world.create_item("Gold (50)")
        for name in SHOP_NAMES:
            location = self.multiworld.get_location(name, self.player)
            self.assertFalse(location.item_rule(key_item), name)
            self.assertTrue(location.item_rule(filler), name)

    def test_progression_toggle_defaults_off(self) -> None:
        self.assertEqual(self.world.options.shopsanity_allow_progression.value, 0)

    def test_enchanted_earth_shop_needs_shadow_items(self) -> None:
        shop = next(s for s in shop_tables if s.level_name == "Enchanted Earth")
        name = shop_location_names(shop, 1)[0]
        self.assertFalse(self.can_reach_location(name))
        self.collect_by_name(["Key Item: Shadow Artefact", "Key Item: Shadow Talisman"])
        self.assertTrue(self.can_reach_location(name))


class ShopSanityProgressionAllowedTest(MedievilTestBase):
    options = {"shopsanity": 1, "shopsanity_allow_progression": 1}

    def test_shops_accept_progression(self) -> None:
        key_item = self.world.create_item("Key Item: Skull Key")
        for name in SHOP_NAMES:
            self.assertTrue(self.multiworld.get_location(name, self.player).item_rule(key_item), name)

    def test_slot_data_has_toggle(self) -> None:
        self.assertEqual(self.world.fill_slot_data()["options"]["shopsanity_allow_progression"], 1)


class ShopSanityOneItemTest(MedievilTestBase):
    options = {"shopsanity": 1, "shopsanity_items_per_shop": 1}

    def test_one_item_per_shop(self) -> None:
        stock = self.world.fill_slot_data()["shop_stock"]
        self.assertTrue(all(len(entries) == 1 for entries in stock.values()))


class ShopSanityFullShopTest(MedievilTestBase):
    options = {"shopsanity": 1, "shopsanity_items_per_shop": SHOP_MENU_ROWS}

    def test_full_shops(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        for name in shop_names(SHOP_MENU_ROWS):
            self.assertIn(name, names)
        stock = self.world.fill_slot_data()["shop_stock"]
        self.assertTrue(all(len(entries) == SHOP_MENU_ROWS for entries in stock.values()))
        self.assertEqual(self.world.fill_slot_data()["options"]["shopsanity_items_per_shop"], SHOP_MENU_ROWS)

