"""
Regression tests for VictoryConditions.py and how set_rules() wires up
multiworld.completion_condition based on the `goal` option.
"""

from . import MedievilTestBase
from ..Options import GoalOptions, ProgressionOptions


ASYLUM_AND_POOLS_ITEMS = [
    "Key Item: Crucifix Cast",
    "Key Item: Landlords Bust",
    "Key Item: Crucifix",
    "Key Item: Shadow Talisman",
    "Key Item: Shadow Artefact",
] + [f"Key Item: Soul Helmet {i}" for i in range(1, 9)]

ALL_NON_ANT_HILL_CHALICE_UNLOCK_ITEMS = (
    [
        "Key Item: Witches Talisman",
        "Equipment: Club",
        "Key Item: Sheet Music",
        "Key Item: Skull Key",
        "Key Item: Harvester Parts",
        "Equipment: Dragon Armour",
        "Key Item: King Peregrine's Crown",
        "Skill: Daring Dash",
    ]
    + ASYLUM_AND_POOLS_ITEMS
)


class DefeatZarokGoalTest(MedievilTestBase):
    """Default goal. In open mode "Map -> Zaroks Lair" has no rule, so it's free."""

    options = {
        "goal": GoalOptions.DEFEAT_ZAROK,
        "progression_option": ProgressionOptions.OPEN,
    }

    def test_beatable_as_soon_as_zaroks_lair_is_reachable(self) -> None:
        self.assertBeatable(True)


class ChaliceGoalTest(MedievilTestBase):
    options = {
        "goal": GoalOptions.CHALICE,
        "progression_option": ProgressionOptions.OPEN,
        "chalice_win_count": 11,
    }

    def test_not_beatable_until_required_chalice_count_reached(self) -> None:
        # 9 chalices are freely reachable in open mode (see test_hall_of_heroes.py),
        # which is below the configured requirement of 11.
        self.assertBeatable(False)
        # Witches Talisman simultaneously unlocks Pumpkin Serpent's and Ant Hill's
        # chalices, bringing the reachable count to 11.
        self.collect_by_name("Key Item: Witches Talisman")
        self.assertBeatable(True)


class BothGoalTest(MedievilTestBase):
    """Zaroks Lair is free in open mode, so this isolates the chalice-count half."""

    options = {
        "goal": GoalOptions.BOTH,
        "progression_option": ProgressionOptions.OPEN,
        "chalice_win_count": 11,
    }

    def test_requires_both_zarok_and_chalice_count(self) -> None:
        self.assertBeatable(False)
        self.collect_by_name("Key Item: Witches Talisman")
        self.assertBeatable(True)


class ChaliceGoalAntHillDisabledCapTest(MedievilTestBase):
    """
    When include_ant_hill_in_checks is off, set_rules() caps max_chalice_count at 19
    even if chalice_win_count is set to 20, and "Chalice: Ant Hill" is never part of
    has_number_of_chalices' tracked list. This test checks the cap is honored: all 19
    non-ant-hill chalices being reachable is enough to win, even though the option
    asked for 20.
    """

    options = {
        "goal": GoalOptions.CHALICE,
        "progression_option": ProgressionOptions.OPEN,
        "chalice_win_count": 20,
        "include_ant_hill_in_checks": 0,
    }

    def test_nineteen_chalices_satisfy_the_capped_requirement(self) -> None:
        self.assertBeatable(False)
        self.collect_by_name(ALL_NON_ANT_HILL_CHALICE_UNLOCK_ITEMS)
        self.assertBeatable(True)
