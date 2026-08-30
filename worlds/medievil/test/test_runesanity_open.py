"""
Regression tests for set_open_runesanity_rules and its helpers set_rune_blocks,
set_breakable_locations, and set_dashable_locations in Rules.py. These only touch
individual LOCATION access rules (not entrances), gating them behind rune items,
club/hammer, and/or daring dash. Only representative examples are covered here, not
every one of the hundreds of individual location assignments made by this function.
"""

from . import MedievilTestBase
from ..Options import BookSanityToggle, GargoyleSanityToggle, IncludeChalicesInChecksToggle, ProgressionOptions, RuneSanityToggle


class OpenRunesanityLocationRulesTest(MedievilTestBase):
    options = {
        "progression_option": ProgressionOptions.OPEN,
        "runesanity": RuneSanityToggle.option_true,
    }

    def test_rune_block_gates_a_location_behind_its_named_rune(self) -> None:
        # set_rune_blocks(self, ["Chaos Rune: The Graveyard", ...], "Earth Rune: The Graveyard")
        self.assertFalse(self.can_reach_location("Chaos Rune: The Graveyard"))
        self.collect_by_name("Earth Rune: The Graveyard")
        self.assertTrue(self.can_reach_location("Chaos Rune: The Graveyard"))

    def test_rune_blocks_can_chain(self) -> None:
        # "Cleared: The Graveyard" is gated behind "Chaos Rune: The Graveyard", which is
        # itself gated behind "Earth Rune: The Graveyard".
        self.assertFalse(self.can_reach_location("Cleared: The Graveyard"))
        self.collect_by_name("Earth Rune: The Graveyard")
        self.assertFalse(self.can_reach_location("Cleared: The Graveyard"))
        self.collect_by_name("Chaos Rune: The Graveyard")
        self.assertTrue(self.can_reach_location("Cleared: The Graveyard"))

    def test_breakable_and_dashable_stack_on_a_shared_location(self) -> None:
        """
        "Earth Rune: The Hilltop Mausoleum" is in both the set_breakable_locations and
        set_dashable_locations lists (and is not itself gated by any rune block), so it
        needs (club or dead-hammer) AND daring dash.
        """
        self.assertFalse(self.can_reach_location("Earth Rune: The Hilltop Mausoleum"))
        self.collect_by_name("Equipment: Club")
        self.assertFalse(self.can_reach_location("Earth Rune: The Hilltop Mausoleum"))
        self.collect_by_name("Skill: Daring Dash")
        self.assertTrue(self.can_reach_location("Earth Rune: The Hilltop Mausoleum"))

    def test_chalice_hilltop_requires_earth_rune(self) -> None:
        self.assertFalse(self.can_reach_location("Chalice: The Hilltop Mausoleum"))
        self.collect_by_name("Key Item: Sheet Music")
        self.assertFalse(self.can_reach_location("Chalice: The Hilltop Mausoleum"))
        self.collect_by_name("Earth Rune: The Hilltop Mausoleum")
        self.assertTrue(self.can_reach_location("Chalice: The Hilltop Mausoleum"))


class OpenRunesanityAllSanityTogglesOffSmokeTest(MedievilTestBase):
    """
    set_rune_blocks/set_breakable_locations/set_dashable_locations each guard against
    calling self.get_location(...) on locations that don't exist when booksanity,
    gargoylesanity, or chalices are turned off (those locations are skipped entirely in
    create_region). This is a smoke test that generation doesn't crash with every one of
    those toggles off at once, since it exercises every skip branch in those helpers.
    """

    options = {
        "progression_option": ProgressionOptions.OPEN,
        "runesanity": RuneSanityToggle.option_true,
        "booksanity": BookSanityToggle.option_false,
        "gargoylesanity": GargoyleSanityToggle.option_false,
        "include_chalices_in_checks": IncludeChalicesInChecksToggle.option_false,
    }

    def test_generation_does_not_crash(self) -> None:
        self.assertTrue(self.constructed)
