import typing
from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Option, Range, Choice, ItemDict, DeathLink, PerGameCommonOptions


class GoalOptions:
    DEFEAT_ZAROK = 0
    CHALICE = 1
    BOTH = 2


class ProgressionOptions:
    VANILLA = 0
    OPEN = 1


class CheatMenuOptions:
    OFF = 0
    SIMPLE = 1
    SUPER = 2


class ChaliceWinCountOption(Range):
    """Sets the number of chalices required to complete the game"""

    display_name = "Chalice Win Count"
    default = 20
    range_start = 1
    range_end = 20


class GuaranteedItemsOption(ItemDict):
    """Guarantees that the specified items will be in the item pool"""

    display_name = "Guaranteed Items"


class GoalOption(Choice):
    """Lets the user choose the completion goal
    Defeat Zarok - Beat the boss at the end
    Chalices - Collect all chalices
    Both - Defeat both zarok AND get the chalices
    """

    display_name = "Completion Goal"
    default = GoalOptions.DEFEAT_ZAROK
    option_zarok = GoalOptions.DEFEAT_ZAROK
    option_chalice = GoalOptions.CHALICE
    option_both = GoalOptions.BOTH


class ProgressionOption(Choice):
    """Lets users choose how they wish to progress
    Vanilla - Plays the game like normal
    Open - Unlocks the whole map to go in any order
    """

    display_name = "Game Progression Options"
    default = ProgressionOptions.VANILLA
    option_vanilla = ProgressionOptions.VANILLA
    option_open = ProgressionOptions.OPEN


class IncludeAntHillInChecksToggle(Toggle):
    """Toggle whether to include the ant hill in your location checks and logic"""

    display_name = "Include Ant Hill Logic"
    default = 1
    option_true = 1
    option_false = 0


class IncludeChalicesInChecksToggle(Toggle):
    """Include Chalices in Checks"""

    display_name = "Include Chalices"
    default = 1
    option_true = 1
    option_false = 0


class RuneSanityToggle(Toggle):
    """Sets whether to mix runes into the pool"""

    display_name = "RuneSanity"
    default = 0
    option_true = 1
    option_false = 0


class GargoyleSanityToggle(Toggle):
    """Sets whether to do checks for interacting with gargoyle statues"""

    display_name = "GargoyleSanity"
    default = 0
    option_true = 1
    option_false = 0


class BookSanityToggle(Toggle):
    """Sets whether reading books counts as checks"""

    display_name = "BookSanity"
    default = 0
    option_true = 1
    option_false = 0


class CheatMenuChoice(Choice):
    """Sets the cheat menu to be available in the pause menu. This allows level skip, chalice completion and
    invulnerability. Please note, though. That the chalices are counted via checks as getting the actual number isn't
    viable at the moment. Sorry!"""

    display_name = "Cheat Menu"
    default = CheatMenuOptions.OFF
    option_off = CheatMenuOptions.OFF
    option_simple = CheatMenuOptions.SIMPLE
    option_super = CheatMenuOptions.SUPER


class BreakAmmoLimit(Toggle):
    """Allow weapon ammo to be higher than the default"""

    display_name = "Break Ammo Count Limit"
    default = 1
    option_true = 1
    option_false = 0


class BreakPercentageLimit(Toggle):
    """Allow weapon percentages to be higher than the default"""

    display_name = "Break Weapon Percentage Limit"
    default = 1
    option_true = 1
    option_false = 0


class AmmoAndChargeToggle(Toggle):
    """Allow Ammo and Charge in the pool"""

    display_name = "Ammo and Charge in Item Pool"
    default = 1
    option_true = 1
    option_false = 0


class TrapToggle(Toggle):
    """Allow traps in the pool"""

    display_name = "Traps in Item Pool"
    default = 1
    option_true = 1
    option_false = 0


class DeathLinkToggle(Toggle):
    """Sets if you want deathlink or not"""

    display_name = "Death Link"
    default = 0
    option_true = 1
    option_false = 0


@dataclass
class MedievilOption(PerGameCommonOptions):
    goal: GoalOption
    progression_option: ProgressionOption
    include_ant_hill_in_checks: IncludeAntHillInChecksToggle
    include_chalices_in_checks: IncludeChalicesInChecksToggle
    chalice_win_count: ChaliceWinCountOption
    break_ammo_limit: BreakAmmoLimit
    break_percentage_limit: BreakPercentageLimit
    traps: TrapToggle
    ammo: AmmoAndChargeToggle
    deathlink: DeathLinkToggle
    cheat_menu: CheatMenuChoice
    gargoylesanity: GargoyleSanityToggle
    booksanity: BookSanityToggle
    runesanity: RuneSanityToggle
    guaranteed_items: GuaranteedItemsOption
