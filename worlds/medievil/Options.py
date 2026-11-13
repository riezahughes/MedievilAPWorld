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


class KeysanityOptions:
    LEVEL_NAME = 0
    UNIQUE_NAME = 1


class ChaliceWinCountOption(Range):
    """Sets the number of chalices required to complete the game"""

    display_name = "Chalice Win Count"
    default = 20
    range_start = 1
    range_end = 20


class KnightsToFind(Range):
    """How many Knights of Gallowmere you need to find to unlock Zarok's Lair. They're spread across the multiworld.
    Only works with open progression, it's turned off for vanilla. 0 leaves the boss open to fight at any time."""

    display_name = "Knights to Find"
    default = 8
    range_start = 0
    range_end = 250


class GuaranteedItemsOption(ItemDict):
    """Guarantees that the specified items will be in the item pool"""

    display_name = "Guaranteed Items"


class GoalOption(Choice):
    """Lets the user choose the completion goal
    Defeat Zarok - Beat the boss at the end
    Chalice - Collect chalices
    Both - Defeat both zarok AND get the chalices
    Must have include_chalices_in_checks set to true for Chalice or Both goal.
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
    default = ProgressionOptions.OPEN
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
    """Sets whether to mix runes into the pool (Note: Doing this AND Keysanity is cursed)"""

    display_name = "RuneSanity"
    default = 0
    option_true = 1
    option_false = 0


class KeySanityToggle(Toggle):
    """Sets whether to mix keys for each level into the pool. Only works with open progression, it's turned off
    for vanilla."""

    display_name = "KeySanity"
    default = 1
    option_true = 1
    option_false = 0


class KeySanityNamingOption(Choice):
    """Sets whether to give your keys fun names:
    LEVEL_NAME = The Graveyard Unlock
    UNIQUE_NAME = Angelic Call
    """

    display_name = "Keysanity Item Naming"
    default = KeysanityOptions.UNIQUE_NAME
    option_level_name = KeysanityOptions.LEVEL_NAME
    option_unique_name = KeysanityOptions.UNIQUE_NAME


class KeySanityStartingKeys(Range):
    """How Many keys you'd like to start the game with"""

    display_name = "Keysanity starting Keys"
    default = 2
    range_start = 1
    range_end = 19


class GargoyleSanityToggle(Toggle):
    """Sets whether to do checks for interacting with gargoyle statues"""

    display_name = "GargoyleSanity"
    default = 1
    option_true = 1
    option_false = 0


class BookSanityToggle(Toggle):
    """Sets whether reading books counts as checks"""

    display_name = "BookSanity"
    default = 1
    option_true = 1
    option_false = 0


class ShopSanityToggle(Toggle):
    """Sets whether Merchant Gargoyles sell Archipelago items for gold"""

    display_name = "ShopSanity"
    default = 1
    option_true = 1
    option_false = 0


class ShopSanityItemsPerShop(Range):
    """How many Archipelago items each Merchant Gargoyle sells when ShopSanity is on. The shop has room for 11;
    weapons stolen by imps are listed first, so in a full shop some items show once a row is free."""

    display_name = "ShopSanity Items Per Shop"
    default = 3
    range_start = 1
    range_end = 11  # Locations.SHOP_MENU_ROWS


class ShopSanityProgressionToggle(Toggle):
    """Allow progression items (such as weapons needed to progress) to be sold in Merchant Gargoyle shops.
    Gold isn't tracked by logic, so you may need to collect gold before you can buy something you need."""

    display_name = "ShopSanity Allow Progression"
    default = 1
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


class DeathSoundToggle(Toggle):
    """There is a sound that will play moments before your death with this on."""

    display_name = "Death Sound"
    default = 0
    option_true = 1
    option_false = 0


class ProgressiveSwordToggle(Toggle):
    """Replaces the Small Sword, Broadsword and Magic Sword with 3 copies of Equipment: Progressive Sword.
    Each copy gives the next sword up, in that order."""

    display_name = "Progressive Sword"
    default = 1
    option_true = 1
    option_false = 0


class ProgressiveBowToggle(Toggle):
    """Replaces the Crossbow, Longbow, Fire Longbow and Magic Longbow with 4 copies of Equipment: Progressive Bow.
    Each copy gives the next bow up, in that order."""

    display_name = "Progressive Bow"
    default = 1
    option_true = 1
    option_false = 0


class ProgressiveShieldToggle(Toggle):
    """Replaces the Copper Shield, Silver Shield and Gold Shield with 3 copies of Equipment: Progressive Shield.
    Each copy gives the next shield up, in that order."""

    display_name = "Progressive Shield"
    default = 1
    option_true = 1
    option_false = 0


@dataclass
class MedievilOption(PerGameCommonOptions):
    goal: GoalOption
    progression_option: ProgressionOption
    include_ant_hill_in_checks: IncludeAntHillInChecksToggle
    include_chalices_in_checks: IncludeChalicesInChecksToggle
    chalice_win_count: ChaliceWinCountOption
    knights_to_find: KnightsToFind
    break_ammo_limit: BreakAmmoLimit
    break_percentage_limit: BreakPercentageLimit
    traps: TrapToggle
    ammo: AmmoAndChargeToggle
    deathlink: DeathLinkToggle
    deathsound: DeathSoundToggle
    cheat_menu: CheatMenuChoice
    keysanity: KeySanityToggle
    keysanity_naming: KeySanityNamingOption
    keysanity_starting_keys: KeySanityStartingKeys
    gargoylesanity: GargoyleSanityToggle
    booksanity: BookSanityToggle
    runesanity: RuneSanityToggle
    shopsanity: ShopSanityToggle
    shopsanity_items_per_shop: ShopSanityItemsPerShop
    shopsanity_allow_progression: ShopSanityProgressionToggle
    progressive_sword: ProgressiveSwordToggle
    progressive_bow: ProgressiveBowToggle
    progressive_shield: ProgressiveShieldToggle
    guaranteed_items: GuaranteedItemsOption
