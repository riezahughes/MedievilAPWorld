from enum import IntEnum
from typing import NamedTuple, List, Optional
import random
from BaseClasses import (
    Item,
    ItemClassification,
)  # ItemClassification is used for internal logic, but not directly in MedievilItemData itself.
from .Options import (
    RuneSanityToggle,
    IncludeAntHillInChecksToggle,
    TrapToggle,
    AmmoAndChargeToggle,
    IncludeChalicesInChecksToggle,
    KeysanityOptions,
)


class MedievilItemCategory(IntEnum):
    AMMO_FILLER = 0
    GOLD_FILLER = 1
    PROGRESSION = 2
    WEAPON = 3
    CHALICE = 4
    RUNE = 5
    TRAP = 6
    FUN = 7
    LEVEL_END = 8
    SKIP = 9
    LEVEL_KEYS = 10
    KNIGHT = 11


class MedievilItemData(NamedTuple):
    name: str
    m_code: Optional[int]  # Changed to Optional[int] for flexibility with None
    category: MedievilItemCategory
    progression: bool  # Added 'progression' field to the raw data


class MedievilItem(Item):
    game: str = "Medievil"
    category: MedievilItemCategory
    m_code: Optional[int]  # Make m_code an instance attribute for MedievilItem

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        super().__init__(name, classification, code, player)
        # The 'advancement' attribute is automatically handled by the parent Item class
        # if ItemClassification.progression is passed to its constructor.
        # You can explicitly set it here for clarity if you prefer, but BaseClasses.Item does this.
        # self.advancement = classification == ItemClassification.progression

        # Store game-specific data directly on the item instance
        item_data = item_dictionary.get(name)
        if item_data:
            self.m_code = item_data.m_code
            self.category = item_data.category
        else:
            self.m_code = None
            self.category = MedievilItemCategory.GOLD_FILLER  # Fallback for unknown items

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 9901000
        # Create a dictionary mapping item names to their unique Archipelago IDs.
        output = {item_data.name: (base_id + item_data.m_code) for item_data in _all_items if item_data.m_code is not None}
        output.update({item_data.name: base_id + item_data.m_code for item_data in _keysanity_regular})
        output.update({item_data.name: base_id + item_data.m_code + KEYSANITY_UNIQUE_ID_OFFSET for item_data in _keysanity_unique})
        output.update({item_data.name: base_id + item_data.m_code for item_data in _knights})
        return output


key_item_names = {
    # life bottles
    "Life Bottle: Dan's Crypt",
    "Life Bottle: The Graveyard",
    "Life Bottle: Hall of Heroes (Canny Tim)",
    "Life Bottle: Dan's Crypt - Behind Wall",
    "Life Bottle: Scarecrow Fields",
    "Life Bottle: Pools of the Ancient Dead",
    "Life Bottle: Hall of Heroes (Ravenhooves The Archer)",
    "Life Bottle: Hall of Heroes (Dirk Steadfast)",
    "Life Bottle: The Time Device",
    # skills
    "Skill: Daring Dash"
    # Inventory Key Items
    "Key Item: Dragon Gem - Pumpkin Serpent",
    "Key Item: Dragon Gem - Inside the Asylum",
    "Key Item: King Peregrine's Crown",
    "Key Item: Soul Helmet 1",
    "Key Item: Soul Helmet 2",
    "Key Item: Soul Helmet 3",
    "Key Item: Soul Helmet 4",
    "Key Item: Soul Helmet 5",
    "Key Item: Soul Helmet 6",
    "Key Item: Soul Helmet 7",
    "Key Item: Soul Helmet 8",
    "Key Item: Witches Talisman",
    "Key Item: Safe Key",
    "Key Item: Shadow Artefact",
    "Key Item: Shadow Talisman",
    "Key Item: Crucifix",
    "Key Item: Landlords Bust",
    "Key Item: Crucifix Cast",
    "Key Item: Amber Piece 1",
    "Key Item: Amber Piece 2",
    "Key Item: Amber Piece 3",
    "Key Item: Amber Piece 4",
    "Key Item: Amber Piece 5",
    "Key Item: Amber Piece 6",
    "Key Item: Amber Piece 7",
    "Key Item: Harvester Parts",
    "Key Item: Skull Key",
    "Key Item: Sheet Music",
    # Required Equipment
    "Equipment: Club",
    # Runes
    "Chaos Rune: The Graveyard",
    "Chaos Rune: The Hilltop Mausoleum",
    "Chaos Rune: Scarecrow Fields",
    "Chaos Rune: The Lake",
    "Chaos Rune: Pumpkin Gorge",
    "Chaos Rune: The Sleeping Village",
    "Chaos Rune: Pools of the Ancient Dead",
    "Chaos Rune: The Asylum Grounds",
    "Chaos Rune: The Haunted Ruins",
    "Chaos Rune: The Ghost Ship",
    "Chaos Rune: The Time Device",
    "Earth Rune: The Graveyard",
    "Earth Rune: The Hilltop Mausoleum",
    "Earth Rune: Scarecrow Fields",
    "Earth Rune: The Crystal Caves",
    "Earth Rune: The Lake",
    "Earth Rune: Pumpkin Gorge",
    "Earth Rune: The Sleeping Village",
    "Earth Rune: Inside the Asylum",
    "Earth Rune: Enchanted Earth",
    "Earth Rune: The Haunted Ruins",
    "Earth Rune: The Time Device",
    "Moon Rune: The Hilltop Mausoleum",
    "Moon Rune: The Sleeping Village",
    "Moon Rune: Scarecrow Fields",
    "Moon Rune: Pumpkin Gorge",
    "Moon Rune: The Ghost Ship",
    "Moon Rune: The Time Device",
    "Star Rune: Return to the Graveyard",
    "Star Rune: Dan's Crypt",
    "Star Rune: The Crystal Caves",
    "Star Rune: The Lake",
    "Star Rune: Enchanted Earth",
    "Star Rune: The Gallows Gauntlet",
    "Star Rune: The Ghost Ship",
    "Time Rune: The Lake",
    "Time Rune: Pumpkin Gorge",
    "Time Rune: The Time Device",
}

_weapons = [
    "Equipment: Small Sword",
    "Equipment: Broadsword",
    "Equipment: Magic Sword",
    "Equipment: Club",
    "Equipment: Hammer",
    "Equipment: Daggers",
    "Equipment: Axe",
    "Equipment: Crossbow",
    "Equipment: Longbow",
    "Equipment: Fire Longbow",
    "Equipment: Magic Longbow",
    "Equipment: Spear",
    "Equipment: Lightning",
]
_ranged_weapons = [
    "Equipment: Daggers",
    "Equipment: Axe",
    "Equipment: Crossbow",
    "Equipment: Longbow",
    "Equipment: Fire Longbow",
    "Equipment: Magic Longbow",
    "Equipment: Spear",
    "Equipment: Lightning",
]

_life_bottles = {
    # life bottles
    "Life Bottle: Dan's Crypt",
    "Life Bottle: The Graveyard",
    "Life Bottle: Hall of Heroes (Canny Tim)",
    "Life Bottle: Dan's Crypt - Behind Wall",
    "Life Bottle: Scarecrow Fields",
    "Life Bottle: Pools of the Ancient Dead",
    "Life Bottle: Hall of Heroes (Ravenhooves The Archer)",
    "Life Bottle: Hall of Heroes (Dirk Steadfast)",
    "Life Bottle: The Time Device",
}


_all_items: List[MedievilItemData] = [
    # Filler Items
    ("Gold Coins (150)", 0, MedievilItemCategory.GOLD_FILLER, False),
    ("Gold Coins (200)", 1, MedievilItemCategory.GOLD_FILLER, False),
    ("Gold Coins (350)", 2, MedievilItemCategory.GOLD_FILLER, False),
    ("Dagger Ammo (10)", 3, MedievilItemCategory.AMMO_FILLER, False),
    ("Dagger Ammo (20)", 4, MedievilItemCategory.AMMO_FILLER, False),
    ("Broadsword Charge (20)", 5, MedievilItemCategory.AMMO_FILLER, False),
    ("Broadsword Charge (50)", 6, MedievilItemCategory.AMMO_FILLER, False),
    ("Club Charge (20)", 7, MedievilItemCategory.AMMO_FILLER, False),
    ("Club Charge (50)", 8, MedievilItemCategory.AMMO_FILLER, False),
    ("Chicken Drumsticks Ammo (10)", 9, MedievilItemCategory.AMMO_FILLER, False),
    ("Crossbow Ammo (20)", 10, MedievilItemCategory.AMMO_FILLER, False),
    ("Crossbow Ammo (50)", 11, MedievilItemCategory.AMMO_FILLER, False),
    ("Longbow Ammo (20)", 12, MedievilItemCategory.AMMO_FILLER, False),
    ("Longbow Ammo (50)", 13, MedievilItemCategory.AMMO_FILLER, False),
    ("Fire Longbow Ammo (20)", 14, MedievilItemCategory.AMMO_FILLER, False),
    ("Fire Longbow Ammo (50)", 15, MedievilItemCategory.AMMO_FILLER, False),
    ("Magic Longbow Ammo (20)", 16, MedievilItemCategory.AMMO_FILLER, False),
    ("Magic Longbow Ammo (50)", 17, MedievilItemCategory.AMMO_FILLER, False),
    ("Spear Ammo (20)", 18, MedievilItemCategory.AMMO_FILLER, False),
    ("Spear Ammo (50)", 19, MedievilItemCategory.AMMO_FILLER, False),
    ("Lightning Charge (30)", 20, MedievilItemCategory.AMMO_FILLER, False),
    ("Lightning Charge (50)", 21, MedievilItemCategory.AMMO_FILLER, False),
    ("Copper Shield Ammo (50)", 22, MedievilItemCategory.AMMO_FILLER, False),
    ("Copper Shield Ammo (100)", 23, MedievilItemCategory.AMMO_FILLER, False),
    ("Silver Shield Ammo (50)", 24, MedievilItemCategory.AMMO_FILLER, False),
    ("Silver Shield Ammo (100)", 25, MedievilItemCategory.AMMO_FILLER, False),
    ("Gold Shield Ammo (50)", 26, MedievilItemCategory.AMMO_FILLER, False),
    ("Gold Shield Ammo (100)", 27, MedievilItemCategory.AMMO_FILLER, False),
    ("Health Vial (50)", 28, MedievilItemCategory.AMMO_FILLER, False),
    ("Health Vial (150)", 29, MedievilItemCategory.AMMO_FILLER, False),
    ("Health Vial (300)", 30, MedievilItemCategory.AMMO_FILLER, False),
    # list of weapons
    # Maybe make some useful or proguseful rather than progression?
    ("Equipment: Small Sword", 31, MedievilItemCategory.WEAPON, True),
    ("Equipment: Broadsword", 32, MedievilItemCategory.WEAPON, True),
    ("Equipment: Magic Sword", 33, MedievilItemCategory.WEAPON, True),
    ("Equipment: Club", 34, MedievilItemCategory.PROGRESSION, True),
    ("Equipment: Hammer", 35, MedievilItemCategory.WEAPON, True),
    ("Equipment: Daggers", 36, MedievilItemCategory.WEAPON, True),
    ("Equipment: Axe", 37, MedievilItemCategory.WEAPON, True),
    ("Equipment: Chicken Drumsticks", 38, MedievilItemCategory.WEAPON, False),
    ("Equipment: Crossbow", 39, MedievilItemCategory.WEAPON, True),
    ("Equipment: Longbow", 40, MedievilItemCategory.WEAPON, True),
    ("Equipment: Fire Longbow", 41, MedievilItemCategory.WEAPON, True),
    ("Equipment: Magic Longbow", 42, MedievilItemCategory.WEAPON, True),
    ("Equipment: Spear", 43, MedievilItemCategory.WEAPON, True),
    ("Equipment: Lightning", 44, MedievilItemCategory.WEAPON, True),
    ("Equipment: Good Lightning", 45, MedievilItemCategory.WEAPON, True),
    ("Equipment: Copper Shield", 46, MedievilItemCategory.WEAPON, False),
    ("Equipment: Silver Shield", 47, MedievilItemCategory.WEAPON, False),
    ("Equipment: Gold Shield", 48, MedievilItemCategory.WEAPON, False),
    ("Equipment: Dragon Armour", 49, MedievilItemCategory.WEAPON, True),
    # Progression items
    ("Life Bottle: Dan's Crypt", 50, MedievilItemCategory.PROGRESSION, True),
    ("Life Bottle: The Graveyard", 51, MedievilItemCategory.PROGRESSION, True),
    ("Life Bottle: Hall of Heroes (Canny Tim)", 52, MedievilItemCategory.PROGRESSION, True),
    ("Life Bottle: Dan's Crypt - Behind Wall", 53, MedievilItemCategory.PROGRESSION, True),
    ("Life Bottle: Scarecrow Fields", 54, MedievilItemCategory.PROGRESSION, True),
    ("Life Bottle: Pools of the Ancient Dead", 55, MedievilItemCategory.PROGRESSION, True),
    ("Life Bottle: Hall of Heroes (Ravenhooves The Archer)", 56, MedievilItemCategory.PROGRESSION, True),
    ("Life Bottle: Hall of Heroes (Dirk Steadfast)", 57, MedievilItemCategory.PROGRESSION, True),
    ("Life Bottle: The Time Device", 58, MedievilItemCategory.PROGRESSION, True),
    ("Skill: Daring Dash", 60, MedievilItemCategory.PROGRESSION, True),
    # Key Inventory Items
    ("Key Item: Dragon Gem - Pumpkin Serpent", 89, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Dragon Gem - Inside the Asylum", 90, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: King Peregrine's Crown", 91, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Soul Helmet 1", 92, MedievilItemCategory.PROGRESSION, True),  # progressive soul helmet?
    ("Key Item: Soul Helmet 2", 93, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Soul Helmet 3", 94, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Soul Helmet 4", 95, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Soul Helmet 5", 96, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Soul Helmet 6", 97, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Soul Helmet 7", 98, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Soul Helmet 8", 99, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Witches Talisman", 100, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Safe Key", 101, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Shadow Artefact", 102, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Shadow Talisman", 103, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Crucifix", 104, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Landlords Bust", 105, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Crucifix Cast", 106, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Amber Piece 1", 107, MedievilItemCategory.PROGRESSION, True),  # progressive amber piece later?
    ("Key Item: Amber Piece 2", 108, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Amber Piece 3", 109, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Amber Piece 4", 110, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Amber Piece 5", 111, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Amber Piece 6", 112, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Amber Piece 7", 113, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Harvester Parts", 114, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Skull Key", 115, MedievilItemCategory.PROGRESSION, True),
    ("Key Item: Sheet Music", 116, MedievilItemCategory.PROGRESSION, True),
    # Runes
    ("Chaos Rune: The Graveyard", 117, MedievilItemCategory.RUNE, True),
    ("Chaos Rune: The Hilltop Mausoleum", 118, MedievilItemCategory.RUNE, True),
    ("Chaos Rune: Scarecrow Fields", 119, MedievilItemCategory.RUNE, True),
    ("Chaos Rune: The Lake", 120, MedievilItemCategory.RUNE, True),
    ("Chaos Rune: Pumpkin Gorge", 121, MedievilItemCategory.RUNE, True),
    ("Chaos Rune: The Sleeping Village", 122, MedievilItemCategory.RUNE, True),
    ("Chaos Rune: Pools of the Ancient Dead", 123, MedievilItemCategory.RUNE, True),
    ("Chaos Rune: The Asylum Grounds", 124, MedievilItemCategory.RUNE, True),
    ("Chaos Rune: The Haunted Ruins", 125, MedievilItemCategory.RUNE, True),
    ("Chaos Rune: Ghost Ship", 126, MedievilItemCategory.RUNE, True),
    ("Chaos Rune: The Time Device", 127, MedievilItemCategory.RUNE, True),
    ("Earth Rune: The Graveyard", 128, MedievilItemCategory.RUNE, True),
    ("Earth Rune: The Hilltop Mausoleum", 129, MedievilItemCategory.RUNE, True),
    ("Earth Rune: Scarecrow Fields", 130, MedievilItemCategory.RUNE, True),
    ("Earth Rune: The Crystal Caves", 131, MedievilItemCategory.RUNE, True),
    ("Earth Rune: The Lake", 132, MedievilItemCategory.RUNE, True),
    ("Earth Rune: Pumpkin Gorge", 133, MedievilItemCategory.RUNE, True),
    ("Earth Rune: The Sleeping Village", 134, MedievilItemCategory.RUNE, True),
    ("Earth Rune: Inside the Asylum", 135, MedievilItemCategory.RUNE, True),
    ("Earth Rune: Enchanted Earth", 136, MedievilItemCategory.RUNE, True),
    ("Earth Rune: The Haunted Ruins", 137, MedievilItemCategory.RUNE, True),
    ("Earth Rune: The Time Device", 138, MedievilItemCategory.RUNE, True),
    ("Moon Rune: The Hilltop Mausoleum", 139, MedievilItemCategory.RUNE, True),
    ("Moon Rune: Scarecrow Fields", 140, MedievilItemCategory.RUNE, True),
    ("Moon Rune: The Sleeping Village", 141, MedievilItemCategory.RUNE, True),
    ("Moon Rune: Pumpkin Gorge", 142, MedievilItemCategory.RUNE, True),
    ("Moon Rune: Ghost Ship", 143, MedievilItemCategory.RUNE, True),
    ("Moon Rune: The Time Device", 144, MedievilItemCategory.RUNE, True),
    ("Star Rune: Return to the Graveyard", 145, MedievilItemCategory.RUNE, True),
    ("Star Rune: Dan's Crypt", 146, MedievilItemCategory.RUNE, True),
    ("Star Rune: The Crystal Caves", 147, MedievilItemCategory.RUNE, True),
    ("Star Rune: The Lake", 148, MedievilItemCategory.RUNE, True),
    ("Star Rune: Enchanted Earth", 149, MedievilItemCategory.RUNE, True),
    ("Star Rune: Pumpkin Gorge", 150, MedievilItemCategory.RUNE, True),
    ("Star Rune: The Gallows Gauntlet", 151, MedievilItemCategory.RUNE, True),
    ("Star Rune: Ghost Ship", 152, MedievilItemCategory.RUNE, True),
    ("Time Rune: The Lake", 153, MedievilItemCategory.RUNE, True),
    ("Time Rune: Pumpkin Gorge", 154, MedievilItemCategory.RUNE, True),
    ("Time Rune: The Time Device", 155, MedievilItemCategory.RUNE, True),
    # List of Traps
    ("Trap: Heavy Dan", 156, MedievilItemCategory.TRAP, False),
    ("Trap: Light Dan", 157, MedievilItemCategory.TRAP, False),
    ("Trap: Darkness", 158, MedievilItemCategory.TRAP, False),
    ("Trap: Hudless", 159, MedievilItemCategory.TRAP, False),
]


_keysanity_regular: List[MedievilItemData] = [
    ("The Graveyard Unlock", 160, MedievilItemCategory.LEVEL_KEYS, True),  # The Graveyard
    ("Cemetery Hill Unlock", 161, MedievilItemCategory.LEVEL_KEYS, True),  # Cemetery Hill
    ("The Hilltop Mausoleum Unlock", 162, MedievilItemCategory.LEVEL_KEYS, True),  # Hilltop Mausoleum
    ("Return to the Graveyard Unlock", 163, MedievilItemCategory.LEVEL_KEYS, True),  # Return to Graveyard
    ("Scarecrow Fields Unlock", 164, MedievilItemCategory.LEVEL_KEYS, True),  # Scarecrow Fields
    ("Pumpkin Gorge Unlock", 165, MedievilItemCategory.LEVEL_KEYS, True),  # Pumpkin Gorge
    ("Pumpkin Serpent Unlock", 166, MedievilItemCategory.LEVEL_KEYS, True),  # Pumpkin Serpent
    ("The Sleeping Village Unlock", 167, MedievilItemCategory.LEVEL_KEYS, True),  # The Sleeping Village
    ("Asylum Grounds Unlock", 168, MedievilItemCategory.LEVEL_KEYS, True),  # Asylum grounds
    ("Inside the Asylum Unlock", 169, MedievilItemCategory.LEVEL_KEYS, True),  # Inside the Asylum
    ("Enchanted Earth Unlock", 170, MedievilItemCategory.LEVEL_KEYS, True),  # Enchanted Earth
    ("Zaroks Lair Unlock", 171, MedievilItemCategory.LEVEL_KEYS, True),  # Zaroks Lair
    ("Pools of the Ancient Dead Unlock", 172, MedievilItemCategory.LEVEL_KEYS, True),  # Pools of the Ancient Dead
    ("The Lake Unlock", 173, MedievilItemCategory.LEVEL_KEYS, True),  # The Lake
    ("The Crystal Caves Unlock", 174, MedievilItemCategory.LEVEL_KEYS, True),  # Crystal Caves
    ("The Gallows Gauntlet Unlock", 175, MedievilItemCategory.LEVEL_KEYS, True),  # Gallows Gauntlet
    ("The Haunted Ruins Unlock", 176, MedievilItemCategory.LEVEL_KEYS, True),  # Haunted Ruins
    ("The Ghost Ship Unlock", 177, MedievilItemCategory.LEVEL_KEYS, True),  # The Ghost Ship
    ("The Entrance Hall Unlock", 178, MedievilItemCategory.LEVEL_KEYS, True),  # Entrance Hall
    ("The Time Device Unlock", 179, MedievilItemCategory.LEVEL_KEYS, True),  # The Time Device
]

_keysanity_unique: List[MedievilItemData] = [
    ("Angelic Call", 160, MedievilItemCategory.LEVEL_KEYS, True),  # The Graveyard
    ("Hillwalking Boots", 161, MedievilItemCategory.LEVEL_KEYS, True),  # Cemetery Hill
    ("Musical Staff", 162, MedievilItemCategory.LEVEL_KEYS, True),  # Hilltop Mausoleum
    ("Moldy Dog Food", 163, MedievilItemCategory.LEVEL_KEYS, True),  # Return to Graveyard
    ("Farm Deed", 164, MedievilItemCategory.LEVEL_KEYS, True),  # Scarecrow Fields
    ("Smashed Pumpkin", 165, MedievilItemCategory.LEVEL_KEYS, True),  # Pumpkin Gorge
    ("Witches Request", 166, MedievilItemCategory.LEVEL_KEYS, True),  # Pumpkin Serpent
    ("Key to the City", 167, MedievilItemCategory.LEVEL_KEYS, True),  # The Sleeping Village
    ("Jack's Invitation", 168, MedievilItemCategory.LEVEL_KEYS, True),  # Asylum grounds
    ("Fight Club", 169, MedievilItemCategory.LEVEL_KEYS, True),  # Inside the Asylum
    ("Demonic Amulet", 170, MedievilItemCategory.LEVEL_KEYS, True),  # Enchanted Earth
    ("False Heroes Hope", 171, MedievilItemCategory.LEVEL_KEYS, True),  # Zaroks Lair
    ("Boating Licence", 172, MedievilItemCategory.LEVEL_KEYS, True),  # Pools of the Ancient Dead
    ("Lake Key", 173, MedievilItemCategory.LEVEL_KEYS, True),  # The Lake
    ("Ancient Horn", 174, MedievilItemCategory.LEVEL_KEYS, True),  # Crystal Caves
    ("Serpent Effigy", 175, MedievilItemCategory.LEVEL_KEYS, True),  # Gallows Gauntlet
    ("Royal Decree", 176, MedievilItemCategory.LEVEL_KEYS, True),  # Haunted Ruins
    ("Stowaway’s Spirit", 177, MedievilItemCategory.LEVEL_KEYS, True),  # The Ghost Ship
    ("Ancient Knocker", 178, MedievilItemCategory.LEVEL_KEYS, True),  # Entrance Hall
    ("Alarm Clock", 179, MedievilItemCategory.LEVEL_KEYS, True),  # The Time Device
]

KNIGHT_ITEM_NAME = "Knight of Gallowmere"

# Kept out of _all_items so BuildItemPool only adds as many as the knights_to_find option asks for.
_knights: List[MedievilItemData] = [
    (KNIGHT_ITEM_NAME, 180, MedievilItemCategory.KNIGHT, True),
]

# The level each key opens, by m_code. Both naming lists share these m_codes, so the client unlocks the same level
# whichever name the key has. Dan's Crypt and the Ant Hill (entered from Enchanted Earth) have no key.
level_key_regions: dict[int, str] = {
    160: "The Graveyard",
    161: "Cemetery Hill",
    162: "The Hilltop Mausoleum",
    163: "Return to the Graveyard",
    164: "Scarecrow Fields",
    165: "Pumpkin Gorge",
    166: "Pumpkin Serpent",
    167: "The Sleeping Village",
    168: "Asylum Grounds",
    169: "Inside the Asylum",
    170: "Enchanted Earth",
    171: "Zaroks Lair",
    172: "Pools of the Ancient Dead",
    173: "The Lake",
    174: "The Crystal Caves",
    175: "The Gallows Gauntlet",
    176: "The Haunted Ruins",
    177: "The Ghost Ship",
    178: "The Entrance Hall",
    179: "The Time Device",
}

# Archipelago IDs must be unique per item name, so the unique-name keys get their own IDs (m_code + this offset)
# while keeping the shared m_code that the client receives.
KEYSANITY_UNIQUE_ID_OFFSET = 40

# Convert raw lists of tuples into MedievilItemData NamedTuple instances
_all_items = [MedievilItemData(row[0], row[1], row[2], row[3]) for row in _all_items]
_keysanity_regular = [MedievilItemData(*row) for row in _keysanity_regular]
_keysanity_unique = [MedievilItemData(*row) for row in _keysanity_unique]
_knights = [MedievilItemData(*row) for row in _knights]
_keysanity_unique_names = {item_data.name for item_data in _keysanity_unique}


def level_key_names(naming: int) -> dict[str, str]:
    """Region name -> the key item that opens it, for the chosen KeySanity naming."""
    table = _keysanity_unique if naming == KeysanityOptions.UNIQUE_NAME else _keysanity_regular
    return {level_key_regions[item_data.m_code]: item_data.name for item_data in table}


item_descriptions = {
    # Optional: Add detailed descriptions for items here
    # "Gold (50)": "A small pouch of gold coins."
}

# Create a dictionary for quick lookup of item data by name
item_dictionary: dict[str, MedievilItemData] = {
    item_data.name: item_data for item_data in (*_all_items, *_keysanity_regular, *_keysanity_unique, *_knights)
}


def BuildItemPool(count: int, options, level_keys: Optional[List[str]] = None) -> List[str]:
    """
    Generates a list of item names to be used for the item pool.
    This function does NOT create Archipelago Item objects; it only provides their names.
    The actual Item objects are created in MedievilWorld.create_items.

    Args:
        count (int): The total number of item names to generate.
        options: The options object from the Archipelago multiworld, used for guaranteed items.
        level_keys: KeySanity level keys to put in the pool (the starting keys are left out by the caller).

    Returns:
        List[str]: A shuffled list of item names.
    """
    item_pool_names: List[str] = []

    # Add any guaranteed items specified in the options first
    if hasattr(options, "guaranteed_items") and options.guaranteed_items.value:
        for item_name in options.guaranteed_items.value:
            if item_name in item_dictionary:
                item_pool_names.append(item_name)
            else:
                print(f"Warning: Guaranteed item '{item_name}' not found in item_dictionary. Skipping.")

    # Add runes if RuneSanity is enabled
    if hasattr(options, "runesanity") and options.runesanity.value == RuneSanityToggle.option_true:
        rune_items = [item_data.name for item_data in _all_items if item_data.category == MedievilItemCategory.RUNE]
        item_pool_names.extend(rune_items)

    # Add the level keys if KeySanity is enabled
    if level_keys:
        item_pool_names.extend(level_keys)

    # Checks all other progression items

    progression_and_weapon_items = [
        item_data.name
        for item_data in _all_items
        if item_data.category == MedievilItemCategory.WEAPON
        or item_data.category == MedievilItemCategory.PROGRESSION
        or (
            hasattr(options, "include_chalices_in_checks")
            and options.include_chalices_in_checks == IncludeChalicesInChecksToggle.option_true
            and item_data.category == MedievilItemCategory.CHALICE
        )
        or (
            hasattr(options, "runesanity")
            and options.runesanity.value == RuneSanityToggle.option_true
            and item_data.category == MedievilItemCategory.RUNE
        )
    ]

    for item_name in progression_and_weapon_items:
        if item_name not in item_pool_names and len(item_pool_names) < count:
            if (
                hasattr(options, "include_ant_hill")
                and options.include_ant_hill.value == IncludeAntHillInChecksToggle.option_false
                and "Amber" in item_name
            ):
                continue
            else:
                item_pool_names.append(item_name)

    # Knights go in after everything else needed, so they never squeeze out other progression
    knights_to_find = options.knights_to_find.value if hasattr(options, "knights_to_find") else 0
    for _ in range(min(knights_to_find, count - len(item_pool_names))):
        item_pool_names.append(KNIGHT_ITEM_NAME)

    # Populate the rest of the pool with random filler items
    filler_item_names = [
        item_data.name
        for item_data in _all_items
        if item_data.category == MedievilItemCategory.GOLD_FILLER
        or (options.ammo.value == AmmoAndChargeToggle.option_true and item_data.category == MedievilItemCategory.AMMO_FILLER)
        or (options.traps.value == TrapToggle.option_true and item_data.category == MedievilItemCategory.TRAP)
    ]

    for _ in range(count - len(item_pool_names)):
        if filler_item_names:
            item_name_to_add = random.choice(filler_item_names)
            item_pool_names.append(item_name_to_add)
        else:
            print("Warning: Ran out of filler items for Medievil. Duplicating from all available items.")
            # Fallback: if no specific filler items left, pick from any available item
            item_pool_names.append(random.choice(list(item_dictionary.keys())))

    random.shuffle(item_pool_names)  # Shuffle the final list of item names
    return item_pool_names
