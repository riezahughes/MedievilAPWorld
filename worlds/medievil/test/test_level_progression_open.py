"""
Regression tests for the open progression entrance rules currently implemented with
lambdas in Rules.py (set_open_level_progression). These pin down the exact current
behavior so the rule_builder conversion can be verified against them.
"""

from . import MedievilTestBase
from ..Options import ProgressionOptions


class OpenLevelProgressionTest(MedievilTestBase):
    options = {
        "progression_option": ProgressionOptions.OPEN,
    }

    def test_entrances_with_no_rule_are_open_from_the_start(self) -> None:
        """
        set_open_level_progression only sets rules for 7 of the ~20 "Map -> X" entrances.
        Everything else is left at the default `lambda state: True` set at the top of
        set_rules(), so it is reachable with zero items. This includes Zaroks Lair itself,
        meaning the "defeat zarok" goal is trivially satisfied in open mode today.
        """
        for entrance in (
            "Map -> Dan's Crypt",
            "Map -> The Graveyard",
            "Map -> The Hilltop Mausoleum",
            "Map -> Enchanted Earth",
            "Map -> Scarecrow Fields",
            "Map -> The Sleeping Village",
            "Map -> Pumpkin Gorge",
            "Map -> Inside the Asylum",
            "Map -> The Crystal Caves",
            "Map -> The Lake",
            "Map -> The Ghost Ship",
            "Map -> The Entrance Hall",
            "Map -> The Time Device",
            "Map -> Zaroks Lair",
        ):
            with self.subTest(entrance=entrance):
                self.assertTrue(self.can_reach_entrance(entrance))
        self.assertBeatable(True)

    def test_cemetery_hill_accepts_club_or_hammer(self) -> None:
        self.assertFalse(self.can_reach_entrance("Map -> Cemetery Hill"))
        self.collect_by_name("Equipment: Hammer")
        self.assertTrue(self.can_reach_entrance("Map -> Cemetery Hill"))

    def test_return_to_the_graveyard_requires_skull_key(self) -> None:
        self.assertFalse(self.can_reach_entrance("Map -> Return to the Graveyard"))
        self.collect_by_name("Key Item: Skull Key")
        self.assertTrue(self.can_reach_entrance("Map -> Return to the Graveyard"))

    def test_asylum_grounds_requires_all_three_key_items(self) -> None:
        self.assertFalse(self.can_reach_entrance("Map -> Asylum Grounds"))
        self.collect_by_name("Key Item: Crucifix Cast")
        self.assertFalse(self.can_reach_entrance("Map -> Asylum Grounds"))
        self.collect_by_name("Key Item: Landlords Bust")
        self.assertFalse(self.can_reach_entrance("Map -> Asylum Grounds"))
        self.collect_by_name("Key Item: Crucifix")
        self.assertTrue(self.can_reach_entrance("Map -> Asylum Grounds"))

    def test_pumpkin_serpent_requires_witches_talisman(self) -> None:
        self.assertFalse(self.can_reach_entrance("Map -> Pumpkin Serpent"))
        self.collect_by_name("Key Item: Witches Talisman")
        self.assertTrue(self.can_reach_entrance("Map -> Pumpkin Serpent"))

    def test_pools_of_the_ancient_dead_requires_shadow_items_and_all_souls(self) -> None:
        self.assertFalse(self.can_reach_entrance("Map -> Pools of the Ancient Dead"))
        self.collect_by_name(["Key Item: Shadow Talisman", "Key Item: Shadow Artefact"])
        self.assertFalse(self.can_reach_entrance("Map -> Pools of the Ancient Dead"))
        self.collect_by_name([f"Key Item: Soul Helmet {i}" for i in range(1, 9)])
        self.assertTrue(self.can_reach_entrance("Map -> Pools of the Ancient Dead"))

    def test_gallows_gauntlet_requires_only_dragon_armour_not_gems(self) -> None:
        """
        Unlike the vanilla chain, open mode's rule for this entrance is just
        `has_weapon_required(self, "Dragon Armour")` -- no dragon gems required.
        """
        self.assertFalse(self.can_reach_entrance("Map -> The Gallows Gauntlet"))
        self.collect_by_name("Equipment: Dragon Armour")
        self.assertTrue(self.can_reach_entrance("Map -> The Gallows Gauntlet"))

    def test_haunted_ruins_requires_crown_and_daring_dash(self) -> None:
        self.assertFalse(self.can_reach_entrance("Map -> The Haunted Ruins"))
        self.collect_by_name("Key Item: King Peregrine's Crown")
        self.assertFalse(self.can_reach_entrance("Map -> The Haunted Ruins"))
        self.collect_by_name("Skill: Daring Dash")
        self.assertTrue(self.can_reach_entrance("Map -> The Haunted Ruins"))
