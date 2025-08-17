import typing
from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Option, Range, Choice, ItemDict, DeathLink, PerGameCommonOptions

class GoalOptions():
    DEFEAT_ZAROK = 0
    CHALICE = 1

class ProgressionOptions():
    VANILLA = 0
    RANDOM = 1
    

class GuaranteedItemsOption(ItemDict):
    """Guarantees that the specified items will be in the item pool"""
    display_name = "Guaranteed Items"
    

class GoalOption(Choice):
    """Lets the user choose the completion goal
    Defeat Zarok - Beat the boss at the end
    Chalices - Collect all chalices (Collect all chalices doesn't work right now)"""
    display_name = "Completion Goal"
    default = GoalOptions.DEFEAT_ZAROK
    option_zarok = GoalOptions.DEFEAT_ZAROK
    option_chalice = GoalOptions.CHALICE
    
class ProgressionOption(Choice):
    """Lets users choose how they wish to progress
    Vanilla - Plays the game like normal
    (Will only do Vanilla for now)"""
    display_name = "Game Progression Options"
    default = ProgressionOptions.VANILLA
    option_vanilla = ProgressionOptions.VANILLA
    
class ExcludeAntCaves(Toggle):
    """Remove the need to go into the Ant Hill from logic"""
    display_name = "Remove Ant Hill Logic"
    default = 0
    option_true = 1
    option_false = 0    
    
class MonsterSanityToggle(Toggle):
    """Sets whether to do checks for individual monsters (Doesn't work)"""
    display_name = "MonsterSanity"
    default = 0
    option_true = 1
    option_false = 0
    
class RuneSanityToggle(Toggle):
    """Sets whether to mix runes into the pool (Doesn't work yet. Will add the items, but not the logic)"""
    display_name = "RuneSanity"
    default = 0
    option_true = 1
    option_false = 0
    
class BookSanityToggle(Toggle):
    """Sets whether reading books counts as checks (Doesn't work)"""
    display_name = "BookSanity"
    default = 0
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
    exclude_ant_caves: ExcludeAntCaves
    deathlink: DeathLinkToggle
    monstersanity: MonsterSanityToggle
    booksanity: BookSanityToggle
    runesanity: RuneSanityToggle
    guaranteed_items: GuaranteedItemsOption