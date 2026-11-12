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

FIVE_LIFE_BOTTLES = [
    "Life Bottle: Dan's Crypt",
    "Life Bottle: The Graveyard",
    "Life Bottle: Scarecrow Fields",
    "Life Bottle: Pools of the Ancient Dead",
    "Life Bottle: The Time Device",
]

ALL_NON_ANT_HILL_CHALICE_UNLOCK_ITEMS = (
    [
        "Key Item: Witches Talisman",
        "Equipment: Club",
        "Equipment: Daggers",
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
    """
    Default goal. Zaroks Lair itself is reachable for free in open mode, but "Cleared: Zaroks
    Lair" needs any weapon, the Good Lightning and 5 life bottles.
    """

    options = {
        "goal": GoalOptions.DEFEAT_ZAROK,
        "progression_option": ProgressionOptions.OPEN,
        "knights_to_find": 0,
    }

    def test_requires_a_weapon_and_five_life_bottles(self) -> None:
        self.assertBeatable(False)
        self.collect_by_name(FIVE_LIFE_BOTTLES)
        self.assertBeatable(False)
        self.collect_by_name("Equipment: Club")
        self.assertBeatable(False)
        self.collect_by_name("Equipment: Good Lightning")
        self.assertBeatable(True)

    def test_four_life_bottles_are_not_enough(self) -> None:
        self.collect_by_name(["Equipment: Club", "Equipment: Good Lightning"])
        self.collect_by_name(FIVE_LIFE_BOTTLES[:4])
        self.assertBeatable(False)


class ChaliceGoalTest(MedievilTestBase):
    options = {
        "goal": GoalOptions.CHALICE,
        "progression_option": ProgressionOptions.OPEN,
        "knights_to_find": 0,
        "chalice_win_count": 11,
    }

    def test_not_beatable_until_required_chalice_count_reached(self) -> None:
        # 7 chalice pickups are reachable with no items in open mode, below the requirement of 11.
        self.assertBeatable(False)
        # A club opens Cemetery Hill, Pumpkin Gorge, Pumpkin Serpent, Inside the Asylum,
        # Ghost Ship and The Entrance Hall's chalices, bringing the reachable count to 12.
        self.collect_by_name("Equipment: Club")
        self.assertBeatable(True)


class BothGoalTest(MedievilTestBase):
    """Isolates each half: the chalice count (needs a club) and Zarok (needs life bottles)."""

    options = {
        "goal": GoalOptions.BOTH,
        "progression_option": ProgressionOptions.OPEN,
        "knights_to_find": 0,
        "chalice_win_count": 11,
    }

    def test_requires_both_zarok_and_chalice_count(self) -> None:
        self.assertBeatable(False)
        self.collect_by_name("Equipment: Club")
        self.assertBeatable(False)  # chalices done, Zarok not
        self.collect_by_name(FIVE_LIFE_BOTTLES)
        self.assertBeatable(False)  # no Good Lightning yet
        self.collect_by_name("Equipment: Good Lightning")
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
        "knights_to_find": 0,
        "chalice_win_count": 20,
        "include_ant_hill_in_checks": 0,
    }

    def test_nineteen_chalices_satisfy_the_capped_requirement(self) -> None:
        self.assertBeatable(False)
        self.collect_by_name(ALL_NON_ANT_HILL_CHALICE_UNLOCK_ITEMS)
        self.assertBeatable(True)
