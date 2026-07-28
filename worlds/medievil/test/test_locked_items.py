"""
Regression tests for set_locked_items_locations in Rules.py, which is called
unconditionally in set_rules() regardless of progression_option.

Uses open progression so the "Locked Items X" parent regions (Hilltop Mausoleum,
Scarecrow Fields, Sleeping Village) are reachable without needing to also simulate
the vanilla level-clear chain; Cemetery Hill is gated by a club/hammer in both modes.
"""


from . import MedievilTestBase
from ..Options import ProgressionOptions


class LockedItemsRegionsTest(MedievilTestBase):
    options = {
        "progression_option": ProgressionOptions.OPEN,
    }

    def test_locked_items_dc_has_no_rule_and_is_always_open(self) -> None:
        """
        Unlike the other four "Locked Items" regions, nothing in Rules.py ever calls
        set_rule/add_rule on "Dan's Crypt -> Locked Items DC". It keeps the default
        `lambda state: True` assigned at the top of set_rules(), so it's reachable
        unconditionally as soon as Dan's Crypt is (i.e. from the start of the game).
        """
        self.assertTrue(self.can_reach_region("Locked Items DC"))

    def test_locked_items_ch_requires_reaching_cemetery_hill_which_needs_club_or_hammer(self) -> None:
        """
        "Cemetery Hill -> Locked Items CH" itself accepts Daring Dash OR Club OR Hammer,
        but Cemetery Hill (the parent region) can only be entered with Club or Hammer.
        Since either of those already satisfies the Locked Items CH check too, Daring
        Dash never actually functions as an independent path to this region: by the
        time you can reach the entrance at all, you already hold an item that trivially
        satisfies its own rule.
        """
        self.assertFalse(self.can_reach_region("Locked Items CH"))
        self.collect_by_name("Skill: Daring Dash")
        self.assertFalse(self.can_reach_region("Locked Items CH"))
        self.collect_by_name("Equipment: Hammer")
        self.assertTrue(self.can_reach_region("Locked Items CH"))

    def test_locked_items_hm_requires_sheet_music(self) -> None:
        self.assertFalse(self.can_reach_region("Locked Items HM"))
        self.collect_by_name("Key Item: Sheet Music")
        self.assertTrue(self.can_reach_region("Locked Items HM"))

    def test_locked_items_sf_requires_harvester_parts(self) -> None:
        self.assertFalse(self.can_reach_region("Locked Items SF"))
        self.collect_by_name("Key Item: Harvester Parts")
        self.assertTrue(self.can_reach_region("Locked Items SF"))

    def test_locked_items_sv_requires_crucifix(self) -> None:
        self.assertFalse(self.can_reach_region("Locked Items SV"))
        self.collect_by_name("Key Item: Crucifix")
        self.assertTrue(self.can_reach_region("Locked Items SV"))
