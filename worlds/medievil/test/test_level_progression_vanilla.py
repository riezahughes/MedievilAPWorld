"""
Regression tests for the vanilla progression entrance rules currently implemented with
lambdas in Rules.py (set_vanilla_level_progression). These pin down the exact current
behavior so the rule_builder conversion can be verified against them.
"""

from . import MedievilTestBase
from ..Options import ProgressionOptions


class VanillaLevelProgressionTest(MedievilTestBase):
    options = {
        "progression_option": ProgressionOptions.VANILLA,
    }

    def test_full_vanilla_chain_requires_items_in_order(self) -> None:
        # Dan's Crypt is reachable unconditionally, so clearing it (and thus The
        # Graveyard, and thus Cemetery Hill) requires no items at all.
        self.assertTrue(self.can_reach_entrance("Map -> The Graveyard"))
        self.assertTrue(self.can_reach_entrance("Map -> Cemetery Hill"))

        # The Hilltop Mausoleum requires Cemetery Hill cleared (already true) AND a
        # club or hammer.
        self.assertFalse(self.can_reach_entrance("Map -> The Hilltop Mausoleum"))
        self.collect_by_name("Equipment: Club")
        self.assertTrue(self.can_reach_entrance("Map -> The Hilltop Mausoleum"))

        # Return to the Graveyard requires the Hilltop Mausoleum cleared AND the skull key.
        self.assertFalse(self.can_reach_entrance("Map -> Return to the Graveyard"))
        self.collect_by_name("Key Item: Skull Key")
        self.assertTrue(self.can_reach_entrance("Map -> Return to the Graveyard"))

        # Enchanted Earth and Scarecrow Fields both only need Return to the Graveyard cleared.
        self.assertTrue(self.can_reach_entrance("Map -> Enchanted Earth"))
        self.assertTrue(self.can_reach_entrance("Map -> Scarecrow Fields"))
        # The Sleeping Village and Pumpkin Gorge both only need Scarecrow Fields cleared.
        self.assertTrue(self.can_reach_entrance("Map -> The Sleeping Village"))
        self.assertTrue(self.can_reach_entrance("Map -> Pumpkin Gorge"))

        # Asylum Grounds requires the Sleeping Village cleared AND all three key items.
        self.assertFalse(self.can_reach_entrance("Map -> Asylum Grounds"))
        self.collect_by_name(["Key Item: Crucifix Cast", "Key Item: Landlords Bust", "Key Item: Crucifix"])
        self.assertTrue(self.can_reach_entrance("Map -> Asylum Grounds"))
        self.assertTrue(self.can_reach_entrance("Map -> Inside the Asylum"))

        # Pumpkin Serpent requires Pumpkin Gorge cleared (already true) AND the Witches Talisman.
        self.assertFalse(self.can_reach_entrance("Map -> Pumpkin Serpent"))
        self.collect_by_name("Key Item: Witches Talisman")
        self.assertTrue(self.can_reach_entrance("Map -> Pumpkin Serpent"))

        # Pools of the Ancient Dead requires Enchanted Earth cleared (already true) AND the
        # shadow talisman/artefact AND all 8 soul helmets.
        self.assertFalse(self.can_reach_entrance("Map -> Pools of the Ancient Dead"))
        self.collect_by_name(["Key Item: Shadow Talisman", "Key Item: Shadow Artefact"])
        self.assertFalse(self.can_reach_entrance("Map -> Pools of the Ancient Dead"))
        self.collect_by_name([f"Key Item: Soul Helmet {i}" for i in range(1, 9)])
        self.assertTrue(self.can_reach_entrance("Map -> Pools of the Ancient Dead"))
        self.assertTrue(self.can_reach_entrance("Map -> The Lake"))
        self.assertTrue(self.can_reach_entrance("Map -> The Crystal Caves"))

        # The Gallows Gauntlet requires The Crystal Caves cleared (already true) AND dragon
        # armour AND both dragon gems.
        self.assertFalse(self.can_reach_entrance("Map -> The Gallows Gauntlet"))
        self.collect_by_name("Equipment: Dragon Armour")
        self.assertFalse(self.can_reach_entrance("Map -> The Gallows Gauntlet"))
        self.collect_by_name(["Key Item: Dragon Gem - Pumpkin Serpent", "Key Item: Dragon Gem - Inside the Asylum"])
        self.assertTrue(self.can_reach_entrance("Map -> The Gallows Gauntlet"))

        # The Haunted Ruins requires The Gallows Gauntlet cleared AND the crown AND daring dash.
        self.assertFalse(self.can_reach_entrance("Map -> The Haunted Ruins"))
        self.collect_by_name("Key Item: King Peregrine's Crown")
        self.assertFalse(self.can_reach_entrance("Map -> The Haunted Ruins"))
        self.collect_by_name("Skill: Daring Dash")
        self.assertTrue(self.can_reach_entrance("Map -> The Haunted Ruins"))

        # The remainder of the chain only requires the previous level cleared.
        self.assertTrue(self.can_reach_entrance("Map -> The Ghost Ship"))
        self.assertTrue(self.can_reach_entrance("Map -> The Entrance Hall"))
        self.assertTrue(self.can_reach_entrance("Map -> The Time Device"))
        self.assertTrue(self.can_reach_entrance("Map -> Zaroks Lair"))

        # Default goal is "defeat zarok", so the game should now be beatable.
        self.assertBeatable(True)

    def test_hilltop_mausoleum_accepts_hammer_as_alternative_to_club(self) -> None:
        """
        Rules.py checks `has_weapon_required(self, "Club") or has_weapon_required(self, "Hammer")` for this
        entrance. "Equipment: Hammer" is now classified progression in Items.py (category=WEAPON,
        progression=True) so it works as the intended alternative to Club.
        """
        self.assertFalse(self.can_reach_entrance("Map -> The Hilltop Mausoleum"))
        self.collect_by_name("Equipment: Hammer")
        self.assertTrue(self.can_reach_entrance("Map -> The Hilltop Mausoleum"))
