"""
Regression tests for set_locked_items_locations in Rules.py, which is called
unconditionally in set_rules() regardless of progression_option.

Uses open progression so the parent level regions are reachable without needing to also
simulate the vanilla level-clear chain.
"""


from . import MedievilTestBase
from ..Options import ProgressionOptions


class LockedItemsRegionsTest(MedievilTestBase):
    options = {
        "progression_option": ProgressionOptions.OPEN,
    }

    def test_locked_items_dc_only_needs_dans_crypt_cleared(self) -> None:
        """
        "Dan's Crypt -> Dan's Crypt Locked Items" requires cleared("Dan's Crypt"), which
        needs no items, so the region is reachable from the start of the game.
        """
        self.assertTrue(self.can_reach_region("Dan's Crypt Locked Items"))

    def test_locked_items_ch_requires_club(self) -> None:
        self.assertFalse(self.can_reach_region("Cemetery Hill Locked Items"))
        self.collect_by_name("Skill: Daring Dash")
        self.assertFalse(self.can_reach_region("Cemetery Hill Locked Items"))
        self.collect_by_name("Equipment: Club")
        self.assertTrue(self.can_reach_region("Cemetery Hill Locked Items"))

    def test_locked_items_ch_hammer_is_not_enough(self) -> None:
        # the Club is needed to light the fire, the Hammer can't do it (see set_locked_items_locations)
        self.assertFalse(self.can_reach_region("Cemetery Hill Locked Items"))
        self.collect_by_name("Equipment: Hammer")
        self.assertFalse(self.can_reach_region("Cemetery Hill Locked Items"))

    def test_locked_items_hm_requires_sheet_music(self) -> None:
        self.assertFalse(self.can_reach_region("The Hilltop Mausoleum Locked Items"))
        self.collect_by_name("Key Item: Sheet Music")
        self.assertTrue(self.can_reach_region("The Hilltop Mausoleum Locked Items"))

    def test_locked_items_rtg_requires_skull_key(self) -> None:
        self.assertFalse(self.can_reach_region("Return to the Graveyard Locked Items"))
        self.collect_by_name("Key Item: Skull Key")
        self.assertTrue(self.can_reach_region("Return to the Graveyard Locked Items"))

    def test_locked_items_sf_requires_harvester_parts(self) -> None:
        self.assertFalse(self.can_reach_region("Scarecrow Fields Locked Items"))
        self.collect_by_name("Key Item: Harvester Parts")
        self.assertTrue(self.can_reach_region("Scarecrow Fields Locked Items"))

    def test_locked_items_sv_requires_crucifix(self) -> None:
        self.assertFalse(self.can_reach_region("The Sleeping Village Locked Items"))
        self.collect_by_name("Key Item: Crucifix")
        self.assertTrue(self.can_reach_region("The Sleeping Village Locked Items"))

    def test_locked_items_ee_requires_shadow_talisman_and_artefact(self) -> None:
        self.assertFalse(self.can_reach_region("Enchanted Earth Locked Items"))
        self.collect_by_name("Key Item: Shadow Talisman")
        self.assertFalse(self.can_reach_region("Enchanted Earth Locked Items"))
        self.collect_by_name("Key Item: Shadow Artefact")
        self.assertTrue(self.can_reach_region("Enchanted Earth Locked Items"))
