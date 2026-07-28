"""
Regression tests for the add_item_rule exclusions set up in MedievilWorld.set_rules()
(worlds/medievil/__init__.py). These control which items the fill algorithm is allowed
to place at a location, independent of access rules.
"""

from . import MedievilTestBase


class ItemPlacementRulesTest(MedievilTestBase):
    def _item_allowed(self, location_name: str, item_name: str) -> bool:
        location = self.multiworld.get_location(location_name, self.player)
        item = self.world.create_item(item_name)
        return location.item_rule(item)

    def test_dans_crypt_excludes_hammer_club_and_daring_dash(self) -> None:
        location_name = "Life Bottle: Dan's Crypt"
        for excluded in ("Equipment: Hammer", "Equipment: Club", "Skill: Daring Dash"):
            with self.subTest(item=excluded):
                self.assertFalse(self._item_allowed(location_name, excluded))
        self.assertTrue(self._item_allowed(location_name, "Gold Coins (50)"))

    def test_locked_items_dc_excludes_hammer_club_and_daring_dash(self) -> None:
        location_name = "Life Bottle: Dan's Crypt - Behind Wall"
        for excluded in ("Equipment: Hammer", "Equipment: Club", "Skill: Daring Dash"):
            with self.subTest(item=excluded):
                self.assertFalse(self._item_allowed(location_name, excluded))
        self.assertTrue(self._item_allowed(location_name, "Gold Coins (50)"))

    def test_locked_items_dc_also_excludes_skull_key(self) -> None:
        self.assertFalse(self._item_allowed("Life Bottle: Dan's Crypt - Behind Wall", "Key Item: Skull Key"))

    def test_locked_items_ch_excludes_skull_key_only(self) -> None:
        location_name = "Equipment: Copper Shield in Arena - CH"
        self.assertFalse(self._item_allowed(location_name, "Key Item: Skull Key"))
        # This location is NOT in Dan's Crypt/Locked Items DC, so the weapon/dash
        # exclusions from that branch don't apply here.
        self.assertTrue(self._item_allowed(location_name, "Equipment: Club"))
        self.assertTrue(self._item_allowed(location_name, "Skill: Daring Dash"))

    def test_locked_items_hm_excludes_skull_key(self) -> None:
        self.assertFalse(self._item_allowed("Gold Coins: Gold Chest at Phantom of the Opera 1 - HM", "Key Item: Skull Key"))

    def test_locked_items_sf_excludes_skull_key(self) -> None:
        self.assertFalse(self._item_allowed("Gold Coins: Chest Next to Chalice - SF", "Key Item: Skull Key"))

    def test_locked_items_sv_does_not_exclude_skull_key(self) -> None:
        """
        Locked Items SV is conspicuously absent from the skull-key exclusion list in
        __init__.py (only DC/CH/HM/SF are listed), so the skull key can be placed there.
        """
        self.assertTrue(self._item_allowed("Energy Vial: Near Chalice - SV", "Key Item: Skull Key"))

    def test_chalice_reward_excludes_all_key_items(self) -> None:
        location_name = "Chalice Reward 1"
        self.assertFalse(self._item_allowed(location_name, "Key Item: Skull Key"))
        self.assertFalse(self._item_allowed(location_name, "Key Item: Witches Talisman"))
        self.assertTrue(self._item_allowed(location_name, "Gold Coins (50)"))
        self.assertTrue(self._item_allowed(location_name, "Equipment: Club"))
