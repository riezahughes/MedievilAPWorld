"""
Regression tests for set_vanilla_runesanity_rules in Rules.py. These use add_rule to
AND extra rune requirements onto the existing vanilla level-progression entrance rules.
Only a representative sample is covered here (not every one of the ~19 entrances this
function touches), since they all follow the same has_required_runes(...) pattern.
"""

from . import MedievilTestBase
from ..Options import ProgressionOptions, RuneSanityToggle


class VanillaRunesanityTest(MedievilTestBase):
    options = {
        "progression_option": ProgressionOptions.VANILLA,
        "runesanity": RuneSanityToggle.option_true,
    }

    def test_the_graveyard_requires_its_two_runes_on_top_of_the_free_level_clear(self) -> None:
        # Dan's Crypt clears for free, so this entrance's requirement reduces to just the
        # two runes added by runesanity.
        self.assertFalse(self.can_reach_entrance("Map -> The Graveyard"))
        self.collect_by_name("Earth Rune: The Graveyard")
        self.assertFalse(self.can_reach_entrance("Map -> The Graveyard"))
        self.collect_by_name("Chaos Rune: The Graveyard")
        self.assertTrue(self.can_reach_entrance("Map -> The Graveyard"))

    def test_hilltop_mausoleum_stacks_runes_on_top_of_the_club_requirement(self) -> None:
        # Cemetery Hill clears for free once The Graveyard's runes are collected, so the
        # combined requirement here is: club AND all three Hilltop Mausoleum runes.
        self.collect_by_name(["Earth Rune: The Graveyard", "Chaos Rune: The Graveyard"])
        self.collect_by_name("Equipment: Club")
        self.assertFalse(self.can_reach_entrance("Map -> The Hilltop Mausoleum"))
        self.collect_by_name(["Moon Rune: The Hilltop Mausoleum", "Earth Rune: The Hilltop Mausoleum"])
        self.assertFalse(self.can_reach_entrance("Map -> The Hilltop Mausoleum"))
        self.collect_by_name("Chaos Rune: The Hilltop Mausoleum")
        self.assertTrue(self.can_reach_entrance("Map -> The Hilltop Mausoleum"))
