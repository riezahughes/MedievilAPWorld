import dataclasses
from typing import TYPE_CHECKING

from typing_extensions import override

from BaseClasses import CollectionState, Entrance, Location
from rule_builder.rules import CanReachLocation, Has, HasAll, Rule, True_, HasAny, HasFromList, AtLeast, CanReachEntrance
from .Options import IncludeAntHillInChecksToggle, IncludeChalicesInChecksToggle, BookSanityToggle, GargoyleSanityToggle, RuneSanityToggle
from .Items import _weapons, _ranged_weapons, _life_bottles

if TYPE_CHECKING:
    from . import MedievilWorld


def weapon(name: str) -> Rule:
    return Has(f"Equipment: {name}")


def key_items(*names: str) -> Rule:
    return HasAll(*[f"Key Item: {name}" for name in names])


def cleared(level: str) -> Rule:
    return CanReachLocation(f"Cleared: {level}")


DARING_DASH = Has("Skill: Daring Dash")

HoH_ACCESS = [
    CanReachEntrance("The Graveyard -> Hall of Heroes"),
    CanReachEntrance("Cemetery Hill -> Hall of Heroes"),
    CanReachEntrance("The Hilltop Mausoleum -> Hall of Heroes"),
    CanReachEntrance("Return to the Graveyard -> Hall of Heroes"),
    CanReachEntrance("Scarecrow Fields -> Hall of Heroes"),
    CanReachEntrance("Enchanted Earth -> Hall of Heroes"),
    CanReachEntrance("The Sleeping Village -> Hall of Heroes"),
    CanReachEntrance("Pools of the Ancient Dead -> Hall of Heroes"),
    CanReachEntrance("The Lake -> Hall of Heroes"),
    CanReachEntrance("The Crystal Caves -> Hall of Heroes"),
    CanReachEntrance("The Gallows Gauntlet -> Hall of Heroes"),
    CanReachEntrance("Asylum Grounds -> Hall of Heroes"),
    CanReachEntrance("Inside the Asylum -> Hall of Heroes"),
    CanReachEntrance("Pumpkin Gorge -> Hall of Heroes"),
    CanReachEntrance("Pumpkin Serpent -> Hall of Heroes"),
    CanReachEntrance("The Haunted Ruins -> Hall of Heroes"),
    CanReachEntrance("The Ghost Ship -> Hall of Heroes"),
    CanReachEntrance("The Entrance Hall -> Hall of Heroes"),
    CanReachEntrance("The Time Device -> Hall of Heroes"),
]

REQUIRED_SOULS = HasAll(*[f"Key Item: Soul Helmet {i}" for i in range(1, 9)])

# The fixed list of chalice pickup locations tracked by HasNumberOfChalices. This looks at
# vanilla chalices currently, so it's based on locations. "Chalice: Ant Hill" is appended
# conditionally in HasNumberOfChalices._instantiate when the ant hill is enabled.
CHALICE_LOCATIONS: tuple[str, ...] = (
    "Chalice: The Graveyard",
    "Chalice: Cemetery Hill",
    "Chalice: The Hilltop Mausoleum",
    "Chalice: Return to the Graveyard",
    "Chalice: Scarecrow Fields",
    "Chalice: Enchanted Earth",
    "Chalice: Sleeping Village",
    "Chalice: Pools of the Ancient Dead",
    "Chalice: The Lake",
    "Chalice: The Crystal Caves",
    "Chalice: The Gallows Gauntlet",
    "Chalice: Asylum Grounds",
    "Chalice: Inside the Asylum",
    "Chalice: Pumpkin Gorge",
    "Chalice: Pumpkin Serpent",
    "Chalice: The Haunted Ruins",
    "Chalice: Ghost Ship",
    "Chalice: The Entrance Hall",
    "Chalice: The Time Device",
)

AMBERS: tuple[str, ...] = (
    "Key Item: Amber Piece 1",
    "Key Item: Amber Piece 2",
    "Key Item: Amber Piece 3",
    "Key Item: Amber Piece 4",
    "Key Item: Amber Piece 5",
    "Key Item: Amber Piece 6",
    "Key Item: Amber Piece 7",
)


@dataclasses.dataclass()
class HasNumberOfChalices(Rule["MedievilWorld"], game="Medievil"):
    """Checks that at least `count` of the tracked chalice pickup LOCATIONS are reachable."""

    count: int

    @override
    def _instantiate(self, world: "MedievilWorld") -> Rule.Resolved:
        if world.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false:
            return True_().resolve(world)
        chalice_locations = CHALICE_LOCATIONS
        if world.options.include_ant_hill_in_checks.value == IncludeAntHillInChecksToggle.option_true:
            chalice_locations = (*chalice_locations, "Chalice: Ant Hill")
        return self.Resolved(
            chalice_locations,
            self.count,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    def __str__(self) -> str:
        return f"HasNumberOfChalices({self.count})"

    class Resolved(Rule.Resolved):
        chalice_locations: tuple[str, ...]
        count: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            collected_chalices = 0
            for chalice_location in self.chalice_locations:
                if state.can_reach_location(chalice_location, self.player):
                    collected_chalices += 1
            return collected_chalices >= self.count

        @override
        def location_dependencies(self) -> dict[str, set[int]]:
            return {name: {id(self)} for name in self.chalice_locations}

        @override
        def __str__(self) -> str:
            return f"Has {self.count} reachable chalices"


def layer_rule(world: "MedievilWorld", spot: "Location | Entrance", rule: Rule) -> None:
    """AND a rule_builder Rule onto whatever access rule is already assigned to `spot`, mirroring the
    old worlds.generic.Rules.add_rule but for Rule objects that still need to be resolved."""
    existing = spot.access_rule
    if existing is Location.access_rule or existing is Entrance.access_rule:
        world.set_rule(spot, rule)
        return
    resolved = rule.resolve(world)
    world.register_rule_dependencies(resolved)
    spot.access_rule = lambda state, e=existing, n=resolved: e(state) and n(state)


def set_vanilla_level_progression(self: "MedievilWorld") -> None:
    print("Vanilla Progression being created: ")
    # Don't need to check items since the cleared already includes them.
    self.set_rule(self.get_entrance("Map -> The Graveyard"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> Cemetery Hill"), cleared("The Graveyard"))
    self.set_rule(self.get_entrance("Map -> The Hilltop Mausoleum"), cleared("Cemetery Hill"))
    self.set_rule(self.get_entrance("Map -> Return to the Graveyard"), cleared("The Hilltop Mausoleum"))
    self.set_rule(self.get_entrance("Map -> Enchanted Earth"), cleared("Return to the Graveyard"))
    self.set_rule(self.get_entrance("Map -> Scarecrow Fields"), cleared("Return to the Graveyard"))
    self.set_rule(self.get_entrance("Map -> The Sleeping Village"), cleared("Scarecrow Fields"))
    self.set_rule(self.get_entrance("Map -> Pumpkin Gorge"), cleared("Scarecrow Fields"))
    self.set_rule(self.get_entrance("Map -> Asylum Grounds"), cleared("Sleeping Village"))
    self.set_rule(self.get_entrance("Map -> Inside the Asylum"), cleared("Asylum Grounds"))
    self.set_rule(self.get_entrance("Map -> Pumpkin Serpent"), cleared("Pumpkin Gorge"))
    self.set_rule(self.get_entrance("Map -> Pools of the Ancient Dead"), cleared("Enchanted Earth"))
    self.set_rule(self.get_entrance("Map -> The Lake"), cleared("Pools of the Ancient Dead"))
    self.set_rule(self.get_entrance("Map -> The Crystal Caves"), cleared("The Lake"))
    self.set_rule(self.get_entrance("Map -> The Gallows Gauntlet"), cleared("The Crystal Caves"))
    if self.options.runesanity.value == RuneSanityToggle.option_true:
        self.set_rule(self.get_entrance("Map -> The Haunted Ruins"), cleared("The Gallows Gauntlet") & Has("Star Rune: The Gallows Gauntlet"))
    else:
        self.set_rule(self.get_entrance("Map -> The Haunted Ruins"), cleared("The Gallows Gauntlet") & weapon("Dragon Armour"))

    self.set_rule(self.get_entrance("Map -> The Ghost Ship"), cleared("The Haunted Ruins"))
    self.set_rule(self.get_entrance("Map -> The Entrance Hall"), cleared("Ghost Ship"))
    self.set_rule(self.get_entrance("Map -> The Time Device"), cleared("The Entrance Hall"))
    self.set_rule(self.get_entrance("Map -> Zaroks Lair"), cleared("The Time Device"))


def set_open_level_progression(self: "MedievilWorld") -> None:
    self.set_rule(self.get_entrance("Map -> Dan's Crypt"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> The Graveyard"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> Return to the Graveyard"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> Cemetery Hill"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> The Hilltop Mausoleum"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> Scarecrow Fields"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> The Crystal Caves"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> The Lake"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> Pumpkin Gorge"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> Pumpkin Serpent"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> The Sleeping Village"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> Pools of the Ancient Dead"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> Asylum Grounds"), cleared("Dan's Crypt"))
    self.set_rule(
        self.get_entrance("Map -> Inside the Asylum"),
        cleared("Dan's Crypt") & (HasAny(*[weapon for weapon in _weapons]) | weapon("Chicken Drumsticks")),
    )
    self.set_rule(self.get_entrance("Map -> Enchanted Earth"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> The Gallows Gauntlet"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> The Haunted Ruins"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> The Ghost Ship"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> The Entrance Hall"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> The Time Device"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> Zaroks Lair"), cleared("Dan's Crypt"))


def set_ant_hill_rules_vanilla(self: "MedievilWorld") -> None:
    self.set_rule(
        self.get_entrance("Enchanted Earth -> Ant Hill"),
        cleared("Return to the Graveyard") & key_items("Witches Talisman"),
    )


def set_ant_hill_rules_open(self: "MedievilWorld") -> None:
    self.set_rule(self.get_entrance("Enchanted Earth -> Ant Hill"), key_items("Witches Talisman"))


def set_ant_hill_bash_rules(self: "MedievilWorld") -> None:
    set_bash_locations(
        self,
        [
            "Key Item: Amber Piece 1 - TA",
            "Key Item: Amber Piece 2 - TA",
            "Key Item: Amber Piece 3 - TA",
            "Key Item: Amber Piece 4 - TA",
            "Key Item: Amber Piece 5 - TA",
            "Key Item: Amber Piece 6 - TA",
            "Key Item: Amber Piece 7 - TA",
            "Key Item: Amber Piece 8 - TA",
            "Key Item: Amber Piece 9 - TA",
            "Key Item: Amber Piece 10 - TA",
            "Fairy 1 - TA",
            "Fairy 2 - TA",
            "Fairy 3 - TA",
            "Fairy 4 - TA",
            "Fairy 5 - TA",
            "Fairy 6 - TA",
            "Energy Vial: Before Fairy 1 - TA",
            "Energy Vial: After Amber 2 - TA",
            "Energy Vial: Fairy 2 Room Center - TA",
            "Energy Vial: Fairy 3 - TA",
            "Energy Vial: Birthing room exit - TA",
            "Gold Coins: Chest at Barrier Fairy - TA",
            "Book: Queen Ant - TA",
            "Chalice: Ant Hill",
            "Cleared: Ant Hill",
        ],
    )


def set_hall_of_heroes_progression(self: "MedievilWorld", max_chalice_count: int) -> None:
    # hall of heroes rules
    # self.set_rule(self.get_entrance("Map -> Hall of Heroes"), HasNumberOfChalices(1))
    # With AtLeast from AP 0.6.8 and list of CanReachEntrance("Hall of Heroes", parent_region_name="Level") (set up in set_HoH_entrances) we can set these properly to check chalice + cleared
    hoh_access = list(HoH_ACCESS)
    if self.options.include_ant_hill_in_checks.value == IncludeAntHillInChecksToggle.option_true:
        hoh_access.append(CanReachEntrance("Ant Hill -> Hall of Heroes"))
    for i in range(1, max_chalice_count + 1):
        location_name = f"Chalice Reward {i}"
        self.set_rule(self.get_location(location_name), AtLeast(i, *hoh_access))


def set_rune_blocks(self: "MedievilWorld", locations: list[str], runes: list[str]) -> None:
    for location in locations:
        if self.options.booksanity.value == BookSanityToggle.option_false and "Book:" in location:
            continue
        if self.options.gargoylesanity.value == GargoyleSanityToggle.option_false and "Gargoyle:" in location:
            continue
        if self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false and "Chalice:" in location:
            continue
        layer_rule(self, self.get_location(location), HasAll(*[rune for rune in runes]))


def set_bash_locations(self: "MedievilWorld", locations: list[str]) -> None:
    for location in locations:
        if self.options.booksanity.value == BookSanityToggle.option_false and "Book:" in location:
            continue
        if self.options.gargoylesanity.value == GargoyleSanityToggle.option_false and "Gargoyle:" in location:
            continue
        if self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false and "Chalice:" in location:
            continue
        layer_rule(self, self.get_location(location), weapon("Club") | weapon("Hammer") | DARING_DASH)


def set_boulder_locations(self: "MedievilWorld", locations: list[str]) -> None:
    for location in locations:
        if self.options.booksanity.value == BookSanityToggle.option_false and "Book:" in location:
            continue
        if self.options.gargoylesanity.value == GargoyleSanityToggle.option_false and "Gargoyle:" in location:
            continue
        if self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false and "Chalice:" in location:
            continue
        layer_rule(self, self.get_location(location), weapon("Club") | weapon("Hammer"))


def set_dash_locations(self: "MedievilWorld", locations: list[str]) -> None:
    for location in locations:
        if self.options.booksanity.value == BookSanityToggle.option_false and "Book:" in location:
            continue
        if self.options.gargoylesanity.value == GargoyleSanityToggle.option_false and "Gargoyle:" in location:
            continue
        if self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false and "Chalice:" in location:
            continue
        layer_rule(self, self.get_location(location), DARING_DASH)


def set_weapon_locations(self: "MedievilWorld", locations: list[str], set: tuple[str]) -> None:
    for location in locations:
        if self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false and "Chalice:" in location:
            continue
        if self.options.gargoylesanity.value == GargoyleSanityToggle.option_false and "Gargoyle:" in location:
            continue
        if self.options.booksanity.value == BookSanityToggle.option_false and "Book:" in location:
            continue
        layer_rule(self, self.get_location(location), HasAny(*[weapon for weapon in set]))


def set_golem_locations(self: "MedievilWorld", locations: list[str]) -> None:
    for location in locations:
        if self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false and "Chalice:" in location:
            continue
        if self.options.gargoylesanity.value == GargoyleSanityToggle.option_false and "Gargoyle:" in location:
            continue
        if self.options.booksanity.value == BookSanityToggle.option_false and "Book:" in location:
            continue
        layer_rule(self, self.get_location(location), DARING_DASH | weapon("Dragon Armour"))


def set_dragon_armour_locations(self: "MedievilWorld", locations: list[str]) -> None:
    for location in locations:
        if self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false and "Chalice:" in location:
            continue
        layer_rule(self, self.get_location(location), weapon("Dragon Armour"))


def set_non_runesanity_rules(self: "MedievilWorld") -> None:
    print("Non Runesanity being created: ")

    set_rune_blocks(
        self,
        [
            "Gold Coins: Chest at Catapult 1 - HR",
            "Gold Coins: Chest at Catapult 2 - HR",
            "Gold Coins: Chest at Catapult 3 - HR",
            "Book: Escape - HR",
        ],
        ["Key Item: King Peregrine's Crown"],
    )

    set_golem_locations(
        self,
        [
            "Gold Coins: Chest at Catapult 1 - HR",
            "Gold Coins: Chest at Catapult 2 - HR",
            "Gold Coins: Chest at Catapult 3 - HR",
            "Book: Escape - HR",
        ],
    )

    set_weapon_locations(self, ["Cleared: Enchanted Earth"], _ranged_weapons)


def set_runesanity_rules(self: "MedievilWorld") -> None:
    print("Runesanity being created: ")
    # Dan's Crypt
    set_rune_blocks(self, ["Book: Track Down Zarok - DC", "Cleared: Dan's Crypt"], ["Star Rune: Dan's Crypt"])

    # The Graveyard
    set_rune_blocks(self, ["Chaos Rune: The Graveyard", "Gold Coins: Near Chaos Rune - TG"], ["Earth Rune: The Graveyard"])

    set_rune_blocks(
        self,
        [
            "Life Bottle: The Graveyard",
            "Equipment: Copper Shield - TG",
            "Gold Coins: Behind Fence at Statue - TG",
            "Gold Coins: Life Bottle Left Chest - TG",
            "Gold Coins: Life Bottle Right Chest - TG",
            "Gold Coins: Shop Chest - TG",
            "Gold Coins: Bag Near Hill Fountain - TG",
            "Book: Gaze of an Angel - TG",
            "Book: Skull Key - TG",
            "Book: The Chalice - TG",
            "Gargoyle: End of Level - TG",
            "Cleared: The Graveyard",
            "Chalice: The Graveyard",
        ],
        ["Chaos Rune: The Graveyard"],
    )

    # Cemetery Hill Logic

    ## no rune logic

    # The Hilltop Mausoleum

    set_rune_blocks(
        self,
        [
            "Chaos Rune: The Hilltop Mausoleum",
            "Moon Rune: The Hilltop Mausoleum",
            "Energy Vial: Phantom of the Opera on Left - HM",
            "Energy Vial: Phantom of the Opera on Right - HM",
            "Gold Coins: After Earth Rune Door - HM",
            "Book: Phantom of the Opera - HM",
            "Book: Demon Heart - HM",
        ],
        ["Earth Rune: The Hilltop Mausoleum"],
    )

    set_rune_blocks(
        self,
        [
            "Key Item: Sheet Music - HM",
            "Energy Vial: Moon Room - HM",
            "Gold Coins: Chest in Moon Room - HM",
        ],
        ["Moon Rune: The Hilltop Mausoleum"],
    )

    set_rune_blocks(
        self,
        [
            "Key Item: Skull Key - HM",
            "Equipment: Daggers near Block Puzzle - HM",
            "Equipment: Copper Shield near Block Puzzle - HM",
            "Cleared: The Hilltop Mausoleum",
        ],
        ["Earth Rune: The Hilltop Mausoleum", "Chaos Rune: The Hilltop Mausoleum"],
    )

    set_rune_blocks(
        self,
        [
            "Gold Coins: Gold Chest at Phantom of the Opera 1 - HM",
            "Gold Coins: Gold Chest at Phantom of the Opera 2 - HM",
            "Gold Coins: Gold Chest at Phantom of the Opera 3 - HM",
        ],
        ["Earth Rune: The Hilltop Mausoleum"],
    )

    set_rune_blocks(
        self,
        ["Chalice: The Hilltop Mausoleum"],
        ["Earth Rune: The Hilltop Mausoleum", "Moon Rune: The Hilltop Mausoleum"],
    )

    # Return to the Graveyard

    set_rune_blocks(
        self,
        [
            "Skill: Daring Dash",
            "Energy Vial: Undertakers Entrance - RTG",
            "Energy Vial: Cliffs Right - RTG",
            "Energy Vial: Cliffs Left - RTG",
            "Gold Coins: Undertakers Entrance - RTG",
            "Gold Coins: Cliffs Left - RTG",
            "Gargoyle: Exit - RTG",
            "Cleared: Return to the Graveyard",
            "Chalice: Return to the Graveyard",
        ],
        ["Star Rune: Return to the Graveyard"],
    )

    # Scarecrow Fields

    set_rune_blocks(
        self,
        [
            "Earth Rune: Scarecrow Fields",
            "Equipment: Club Inside Hut - SF",
        ],
        ["Moon Rune: Scarecrow Fields"],
    )

    set_rune_blocks(self, ["Chaos Rune: Scarecrow Fields", "Equipment: Silver Shield Behind Windmill - SF"], ["Earth Rune: Scarecrow Fields"])

    set_rune_blocks(
        self,
        [
            "Key Item: Harvester Parts - SF",
            "Equipment: Copper Shield in Chest In the Barn - SF",
            "Energy Vial: Cornfield Path - SF",
            "Gold Coins: Bag in the Barn - SF",
            "Gold Coins: Cornfield Square near Barn - SF",
            "Gold Coins: Cornfield Path 1 - SF",
            "Gold Coins: Chest Under Hay Stack - SF",
            "Gold Coins: Bag under Barn Hay Stack - SF",
            "Gold Coins: Bag in the Press - SF",
            "Gold Coins: Bag in the Spinner - SF",
            "Gold Coins: Chest next to Harvester Part - SF",
            "Book: Kul Katura - SF",
            "Book: Cornfields - SF",
            "Book: Mad Machines - SF",
            "Book: Corn Cutter - SF",
            "Gargoyle: Exit - SF",
            "Cleared: Scarecrow Fields",
            "Life Bottle: Scarecrow Fields",
            "Chalice: Scarecrow Fields",
            "Gold Coins: Chest Next to Chalice - SF",
        ],
        ["Earth Rune: Scarecrow Fields", "Chaos Rune: Scarecrow Fields"],
    )

    # Enchanted Earth:

    set_rune_blocks(
        self,
        [
            "Gold Coins: Bag at Cave Entrance - EE",
            "Gargoyle: Outside Demon Entrance - EE",
        ],
        ["Earth Rune: Enchanted Earth"],
    )

    set_rune_blocks(
        self,
        [
            "Key Item: Shadow Talisman - EE",
            "Gold Coins: Chest Near Barrier - EE",
            "Energy Vial: Shadow Talisman Cave - EE",
            "Book: Take the Talisman - EE",
            "Gargoyle: Outside Demon Exit- EE",
            "Chalice: Enchanted Earth",
        ],
        ["Earth Rune: Enchanted Earth"],
    )

    set_rune_blocks(
        self,
        ["Cleared: Enchanted Earth"],
        ["Earth Rune: Enchanted Earth", "Star Rune: Enchanted Earth"],
    )
    # The Sleeping Village

    set_rune_blocks(
        self,
        [
            "Equipment: Club Chest under Inn Stairs - SV",
            "Book: Mayors Bust - SV",
            "Earth Rune: Sleeping Village",
            "Gold Coins: Bag in Barrel at bottom of Inn Stairs - SV",
            "Gold Coins: Bag in Barrel Behind Inn Stairs - SV",
        ],
        ["Moon Rune: The Sleeping Village"],
    )

    set_rune_blocks(
        self,
        [
            "Key Item: Landlords Bust - SV",
            "Energy Vial: Bust Switch - SV",
            "Gold Coins: Bag In Top Bust Barrel - SV",
            "Gold Coins: Bag In Switch Bust Barrel - SV",
            "Chalice: Sleeping Village",
            "Cleared: Sleeping Village",
        ],
        ["Moon Rune: The Sleeping Village", "Earth Rune: The Sleeping Village"],
    )

    set_rune_blocks(
        self,
        [
            "Gold Coins: Bag In Top Bust Barrel - SV",
            "Gold Coins: Bag In Switch Bust Barrel - SV",
            "Key Item: Landlords Bust - SV",
            "Cleared: Sleeping Village",
            "Chalice: Sleeping Village",
        ],
        ["Earth Rune: The Sleeping Village"],
    )

    set_rune_blocks(
        self,
        [
            "Book: History of Gallowmere 1 - SV",
            "Book: History of Gallowmere 2 - SV",
            "Book: History of Gallowmere 3 - SV",
            "Book: History of Gallowmere 4 - SV",
            "Book: Heroes From History - SV",
            "Book: Tourist Guide 1 - SV",
            "Book: Tourist Guide 2 - SV",
            "Key Item: Crucifix Cast - SV",
            "Gold Coins: Bag in Library - SV",
            "Book: Mayor Memoire - SV",
        ],
        ["Chaos Rune: The Sleeping Village"],
    )

    # Pools of the Ancient Dead

    set_rune_blocks(
        self,
        [
            "Life Bottle: Pools of the Ancient Dead",
            "Energy Vial: Chariot Right - PAD",
            "Energy Vial: Chariot Left - PAD",
            "Energy Vial: Jump Spot 1 - PAD",
            "Energy Vial: Jump Spot 2 - PAD",
            "Gold Coins: Jump Spot 1 - PAD",
            "Gold Coins: Jump Spot 2 - PAD",
            "Key Item: Soul Helmet 7 - PAD",
            "Key Item: Soul Helmet 8 - PAD",
            "Chalice: Pools of the Ancient Dead",
        ],
        ["Chaos Rune: Pools of the Ancient Dead"],
    )

    # The Lake

    set_rune_blocks(
        self,
        [
            "Equipment: Silver Shield In Whirlpool - TL",
            "Energy Vial: Whirpool Wind 1 - TL",
            "Energy Vial: Whirpool Wind 2 - TL",
            "Gold Coins: Bag at the Whirlpool Entrance - TL",
            "Gold Coins: Whirlpool Wind 1 - TL",
            "Gold Coins: Whirlpool Wind 2 - TL",
            "Gold Coins: Outside Whirlpool Exit - TL",
            "Gold Coins: Chest in Whirlpool Switch Area - TL",
            "Star Rune: The Lake",
            "Chalice: The Lake",
        ],
        ["Time Rune: The Lake", "Chaos Rune: The Lake", "Earth Rune: The Lake"],
    )

    set_rune_blocks(
        self,
        ["Cleared: The Lake"],
        ["Star Rune: The Lake"],
    )

    # Crystal Caves

    set_rune_blocks(
        self,
        [
            "Star Rune: The Crystal Caves",
            "Energy Vial: Dragon Room 1st Platform - CC",
            "Energy Vial: Dragon Room 3rd Platform - CC",
            "Gold Coins: Chest in Crystal after Pool - CC",
            "Gold Coins: Chest in Crystal After Earth Door - CC",
            "Gold Coins: Bag in Dragon Room 1 1st Platform - CC",
            "Gold Coins: Bag in Dragon Room 2 1st Platform - CC",
            "Gold Coins: Chest in Dragon Room 1st Platform - CC",
            "Gold Coins: Bag in Dragon Room 2nd Platform - CC",
            "Gold Coins: Bag in Dragon Room 1 3rd Platform - CC",
            "Gold Coins: Bag in Dragon Room 2 3rd Platform - CC",
            "Gold Coins: Chest in Dragon Room 3rd Platform - CC",
            "Gold Coins: Bag in Dragon Room 4th Platform 1 - CC",
            "Gold Coins: Chest in Dragon Room 4th Platform - CC",
            "Gold Coins: Bag in Dragon Room 4th Platform 2 - CC",
            "Gold Coins: Bag on Left of Pool - CC",
            "Gold Coins: Bag on Right of Pool - CC",
            "Book: Summon Dragon - CC",
            "Equipment: Dragon Armour - CC",
        ],
        ["Earth Rune: The Crystal Caves"],
    )

    set_rune_blocks(
        self,
        ["Chalice: The Crystal Caves"],
        ["Earth Rune: The Crystal Caves", "Star Rune: The Crystal Caves"],
    )

    set_rune_blocks(self, ["Cleared: The Crystal Caves"], ["Star Rune: The Crystal Caves"])

    #  The Gallows Gauntlet

    set_rune_blocks(self, ["Chalice: The Gallows Gauntlet"], ["Star Rune: The Gallows Gauntlet"])

    # Asylum Grounds

    set_rune_blocks(
        self,
        [
            "Energy Vial: Near Bishop - AG",
            "Energy Vial: Near King - AG",
            "Gold Coins: Behind Chaos Gate - AG",
            "Gold Coins: Behind Elephant in Grave - AG",
            "Book: Secret Exit - AG",
            "Cleared: Asylum Grounds",
            "Chalice: Asylum Grounds",
        ],
        ["Chaos Rune: The Asylum Grounds"],
    )

    # Inside the Asylum

    set_rune_blocks(
        self,
        [
            "Key Item: Dragon Gem - IA",
            "Cleared: Inside the Asylum",
        ],
        ["Earth Rune: Inside the Asylum"],
    )

    # Pumpkin Gorge

    set_rune_blocks(
        self,
        [
            "Energy Vial: In Moon Hut - PG",
            "Chaos Rune: Pumpkin Gorge",
        ],
        ["Moon Rune: Pumpkin Gorge"],
    )

    set_rune_blocks(
        self,
        [
            "Earth Rune: Pumpkin Gorge",
            "Book: Mushrooms - PG",
            "Gold Coins: Bag in Mushroom Area - PG",
        ],
        ["Chaos Rune: Pumpkin Gorge"],
    )

    set_rune_blocks(
        self,
        [
            "Star Rune: Pumpkin Gorge",
            "Energy Vial: Top of Hill - PG",
            "Equipment: Silver Shield in Chest at Top of Hill - PG",
        ],
        ["Chaos Rune: Pumpkin Gorge", "Earth Rune: Pumpkin Gorge"],
    )

    set_rune_blocks(self, ["Time Rune: Pumpkin Gorge"], ["Chaos Rune: Pumpkin Gorge", "Star Rune: Pumpkin Gorge"])

    set_rune_blocks(
        self,
        [
            "Energy Vial: Boulders After Time Rune - PG",
            "Energy Vial: Vine Patch Left - PG",
            "Energy Vial: Vine Patch Right - PG",
            "Gold Coins: Chest at Boulders after Time Rune - PG",
            "Gargoyle: Exit - PG",
            "Cleared: Pumpkin Gorge",
            "Chalice: Pumpkin Gorge",
        ],
        ["Chaos Rune: Pumpkin Gorge", "Star Rune: Pumpkin Gorge", "Time Rune: Pumpkin Gorge"],
    )

    # Pumpkin Serpent

    ## no rune logic

    # Haunted Ruins

    set_rune_blocks(
        self,
        [
            "Key Item: King Peregrine's Crown - HR",
            "Gold Coins: Bag in Crown Room - HR",
            "Book: Sad King - HR",
            "Book: Ghost King - HR",
            "Book: The Volcano - HR",
            "Earth Rune: The Haunted Ruins",
            "Chalice: The Haunted Ruins",
        ],
        ["Chaos Rune: The Haunted Ruins"],
    )

    set_rune_blocks(
        self,
        [
            "Gold Coins: Chest at Catapult 1 - HR",
            "Gold Coins: Chest at Catapult 2 - HR",
            "Gold Coins: Chest at Catapult 3 - HR",
            "Book: Escape - HR",
        ],
        ["Earth Rune: The Haunted Ruins"],
    )
    set_rune_blocks(
        self,
        [
            "Cleared: The Haunted Ruins",
        ],
        ["Earth Rune: The Haunted Ruins", "Chaos Rune: The Haunted Ruins"],
    )

    # Ghost Ship

    set_rune_blocks(
        self,
        [
            "Energy Vial: In Cabin - GS",
            "Star Rune: Ghost Ship",
        ],
        ["Moon Rune: Ghost Ship"],
    )

    set_rune_blocks(self, ["Chaos Rune: Ghost Ship"], ["Star Rune: Ghost Ship"])

    set_rune_blocks(
        self,
        [
            "Energy Vial: In Cannon Room - GS",
            "Energy Vial: Rope Bridge 1 - GS",
            "Energy Vial: Rope Bridge 2 - GS",
            "Energy Vial: Cage Lift 1 - GS",
            "Energy Vial: Cage Lift 2 - GS",
            "Gold Coins: Chest in Cannon Room - GS",
            "Gold Coins: Rope Bridge - GS",
            "Equipment: Club in Chest at Captain - GS",
            "Cleared: Ghost Ship",
            "Chalice: Ghost Ship",
            "Book: Boss Strategy - GS",
        ],
        ["Chaos Rune: Ghost Ship", "Star Rune: Ghost Ship"],
    )

    # Entrance Hall

    # has no logic or gates

    # The Time Device

    set_rune_blocks(
        self,
        [
            "Life Bottle: The Time Device",
            "Gold Coins: Laser Platform Right - TD",
            "Gold Coins: Laser Platform Left - TD",
            "Gold Coins: Lone Pillar 1 - TD",
            "Gold Coins: Lone Pillar 2 - TD",
            "Gold Coins: Lone Pillar 3 - TD",
            "Chaos Rune: The Time Device",
            "Earth Rune: The Time Device",
            "Book: The Train - TD",
        ],
        ["Time Rune: The Time Device"],
    )

    set_rune_blocks(
        self,
        [
            "Cleared: The Time Device",
        ],
        ["Time Rune: The Time Device", "Chaos Rune: The Time Device", "Moon Rune: The Time Device"],
    )

    set_rune_blocks(
        self,
        [
            "Chalice: The Time Device",
        ],
        ["Time Rune: The Time Device", "Chaos Rune: The Time Device", "Moon Rune: The Time Device", "Earth Rune: The Time Device"],
    )

    set_rune_blocks(
        self,
        [
            "Gold Coins: Bag at Earth Station 1 - TD",
            "Gold Coins: Bag at Earth Station 2 - TD",
            "Gold Coins: Bag at Earth Station 3 - TD",
            "Moon Rune: The Time Device",
        ],
        ["Time Rune: The Time Device", "Chaos Rune: The Time Device", "Earth Rune: The Time Device"],
    )


def set_weapon_dependencies(self: "MedievilWorld") -> None:
    set_dash_locations(
        self,
        [
            "Gold Coins: Lone Pillar 1 - TD",
            "Gold Coins: Lone Pillar 2 - TD",
            "Gold Coins: Lone Pillar 3 - TD",
        ],
    )

    set_boulder_locations(
        self,
        [
            "Equipment: Club - CH",
            "Book: Club - CH",
            "Book: A Guide to Covens - CH",
            "Energy Vial: Right Coffin - HM",
            "Book: Thieving Imps - HM",
            "Energy Vial: Near Rune on Left Ramp - HM",
            "Earth Rune: The Hilltop Mausoleum",
            "Gargoyle: Witch Cave - CH",
            "Chaos Rune: The Hilltop Mausoleum",
            "Moon Rune: The Hilltop Mausoleum",
            "Energy Vial: Phantom of the Opera on Left - HM",
            "Energy Vial: Phantom of the Opera on Right - HM",
            "Gold Coins: After Earth Rune Door - HM",
            "Book: Phantom of the Opera - HM",
            "Book: Demon Heart - HM",
            "Key Item: Sheet Music - HM",
            "Energy Vial: Moon Room - HM",
            "Gold Coins: Chest in Moon Room - HM",
            "Key Item: Skull Key - HM",
            "Equipment: Daggers near Block Puzzle - HM",
            "Equipment: Copper Shield near Block Puzzle - HM",
            "Cleared: The Hilltop Mausoleum",
            "Gold Coins: Gold Chest at Phantom of the Opera 1 - HM",
            "Gold Coins: Gold Chest at Phantom of the Opera 2 - HM",
            "Gold Coins: Gold Chest at Phantom of the Opera 3 - HM",
            "Chalice: The Hilltop Mausoleum",
            "Gold Coins: Bag in Left Barrel at Blacksmith - SV",
            "Gold Coins: Bag in Right Barrel at Blacksmith - SV",
            "Gold Coins: Bag in Barrel at Inn - SV",
            "Earth Rune: Sleeping Village",
            "Gold Coins: Bag in Barrel at bottom of Inn Stairs - SV",
            "Gold Coins: Bag in Barrel Behind Inn Stairs - SV",
            "Gold Coins: Bag In Top Bust Barrel - SV",
            "Gold Coins: Bag In Switch Bust Barrel - SV",
            "Equipment: Dragon Armour - CC",
            "Star Rune: Pumpkin Gorge",
            "Equipment: Silver Shield in Chest at Top of Hill - PG",
            "Energy Vial: Top of Hill - PG",
            "Energy Vial: Boulders After Time Rune - PG",
            "Gold Coins: Chest at Boulders after Time Rune - PG",
            "Chalice: Pumpkin Gorge",
            "Chalice: The Haunted Ruins",
        ],
    )

    set_bash_locations(
        self,
        [
            "Life Bottle: Dan's Crypt - Behind Wall",
            "Gold Coins: Behind Wall in Crypt - Left - DC",
            "Gold Coins: Behind Wall in Crypt - Right - DC",
            "Key Item: Crucifix Cast - SV",
            "Gold Coins: Bag in Library - SV",
            "Book: Mayor Memoire - SV",
            "Gold Coins: Bag Behind Rocks At Start - PG",
            "Gold Coins: Chest Near Chalice - PG",
            "Energy Vial: Chalice Path - PG",
            "Energy Vial: In Coop - PG",
            "Gold Coins: Chest in Coop 1 - PG",
            "Gold Coins: Chest in Coop 2 - PG",
            "Gold Coins: Chest in Coop 3 - PG",
            "Earth Rune: Pumpkin Gorge",
            "Book: Mushrooms - PG",
            "Gold Coins: Bag in Mushroom Area - PG",
            "Time Rune: Pumpkin Gorge",
            "Energy Vial: Vine Patch Left - PG",
            "Energy Vial: Vine Patch Right - PG",
            "Gargoyle: Exit - PG",
            "Cleared: Pumpkin Gorge",
            "Chaos Rune: Pumpkin Gorge",
            "Energy Vial: In Moon Hut - PG",
        ],
    )

    set_dragon_armour_locations(
        self,
        [
            "Star Rune: The Gallows Gauntlet",
            "Energy Vial: Near Chalice - GG",
            "Gold Coins: Chest at Serpent - GG",
            "Gold Coins: Chest Near Star Entrance - GG",
            "Chalice: The Gallows Gauntlet",
        ],
    )

    # All weapons without drumstick
    set_weapon_locations(
        self,
        [
            "Gargoyle: Exit - RTG",
            "Skill: Daring Dash",
            "Cleared: Return to the Graveyard",
            "Energy Vial: Left at Merchant Gargoyle - PS",
            "Energy Vial: Right at Merchant Gargoyle - PS",
            "Gold Coins: Chest at Merchant Gargoyle - PS",
            "Key Item: Dragon Gem - PS",
            "Chalice: Pumpkin Serpent",
            "Cleared: Pumpkin Serpent",
            "Cleared: Zaroks Lair",
        ],
        _weapons,
    )

    # Ranged weapons
    set_weapon_locations(
        self,
        [
            "Cleared: The Hilltop Mausoleum",
            "Key Item: Skull Key - HM",
            "Gold Coins: Chest Left of Fountain - EE",
            "Gold Coins: Chest Top of Fountain - EE",
            "Gold Coins: Chest Right of Fountain - EE",
            "Energy Vial: Left of Tree Drop - EE",
            "Energy Vial: Right of Tree Drop - EE",
            "Chalice: Enchanted Earth",
        ],
        _ranged_weapons,
    )

    set_golem_locations(
        self,
        ["Chalice: The Haunted Ruins", "Cleared: The Haunted Ruins"],
    )


def set_key_item_dependencies(self: "MedievilWorld") -> None:
    """Base-game key-item dependencies, applied in every mode."""
    self.set_rule(self.get_location("Key Item: Shadow Artefact - SV"), key_items("Safe Key") & CanReachLocation("Key Item: Landlords Bust - SV"))
    self.set_rule(self.get_location("Key Item: Crucifix - SV"), key_items("Landlords Bust", "Crucifix Cast"))
    self.set_rule(self.get_location("Cleared: Pools of the Ancient Dead"), REQUIRED_SOULS)
    self.set_rule(self.get_location("Key Item: Dragon Gem - PS"), key_items("Witches Talisman"))
    self.set_rule(self.get_location("Earth Rune: The Haunted Ruins"), key_items("King Peregrine's Crown"))
    self.set_rule(self.get_location("Cleared: The Haunted Ruins"), key_items("King Peregrine's Crown"))
    if self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_true:
        self.set_rule(self.get_location("Chalice: The Haunted Ruins"), key_items("King Peregrine's Crown"))
        self.set_rule(self.get_location("Chalice: Sleeping Village"), CanReachLocation("Key Item: Landlords Bust - SV"))
        set_weapon_locations(self, ["Chalice: The Entrance Hall"], _weapons)
        if self.options.runesanity.value == RuneSanityToggle.option_true:
            self.set_rule(self.get_location("Chalice: Ghost Ship"), Has("Moon Rune: Ghost Ship") | weapon("Club"))
    self.set_rule(self.get_location("Cleared: Ghost Ship"), weapon("Club"))
    self.set_rule(self.get_location("Cleared: Zaroks Lair"), weapon("Good Lightning") & HasFromList(*_life_bottles, count=5))
    self.set_rule(self.get_location("Cleared: Sleeping Village"), CanReachLocation("Key Item: Landlords Bust - SV"))
    self.set_rule(self.get_location("Equipment: Dragon Armour - CC"), key_items("Dragon Gem - Pumpkin Serpent", "Dragon Gem - Inside the Asylum"))
    if self.options.include_ant_hill_in_checks.value == IncludeAntHillInChecksToggle.option_true:
        self.set_rule(self.get_location("Equipment: Chicken Drumsticks - TA"), HasAll(*[amber for amber in AMBERS]))


def set_locked_items_locations(self: "MedievilWorld") -> None:
    self.set_rule(self.get_entrance("Dan's Crypt -> Dan's Crypt Locked Items"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Dan's Crypt -> Map"), cleared("Dan's Crypt"))
    self.set_rule(
        self.get_entrance("Cemetery Hill -> Cemetery Hill Locked Items"), weapon("Club")
    )  # needed for lighting on fire. The hammer won't do it.
    self.set_rule(self.get_entrance("The Hilltop Mausoleum -> The Hilltop Mausoleum Locked Items"), key_items("Sheet Music"))
    self.set_rule(self.get_entrance("Return to the Graveyard -> Return to the Graveyard Locked Items"), key_items("Skull Key"))
    self.set_rule(self.get_entrance("Scarecrow Fields -> Scarecrow Fields Locked Items"), key_items("Harvester Parts"))
    self.set_rule(self.get_entrance("The Sleeping Village -> The Sleeping Village Locked Items"), key_items("Crucifix"))
    self.set_rule(self.get_entrance("Enchanted Earth -> Enchanted Earth Locked Items"), key_items("Shadow Artefact", "Shadow Talisman"))


def set_HoH_entrances(self: "MedievilWorld") -> None:
    self.set_rule(self.get_entrance("The Graveyard -> Hall of Heroes"), cleared("The Graveyard") & CanReachLocation("Chalice: The Graveyard"))
    self.set_rule(
        self.get_entrance("Return to the Graveyard -> Hall of Heroes"),
        cleared("Return to the Graveyard") & CanReachLocation("Chalice: Return to the Graveyard"),
    )
    self.set_rule(self.get_entrance("Cemetery Hill -> Hall of Heroes"), cleared("Cemetery Hill") & CanReachLocation("Chalice: Cemetery Hill"))
    self.set_rule(
        self.get_entrance("The Hilltop Mausoleum -> Hall of Heroes"),
        cleared("The Hilltop Mausoleum") & CanReachLocation("Chalice: The Hilltop Mausoleum"),
    )
    self.set_rule(
        self.get_entrance("Scarecrow Fields -> Hall of Heroes"), cleared("Scarecrow Fields") & CanReachLocation("Chalice: Scarecrow Fields")
    )
    self.set_rule(
        self.get_entrance("The Crystal Caves -> Hall of Heroes"), cleared("The Crystal Caves") & CanReachLocation("Chalice: The Crystal Caves")
    )
    self.set_rule(self.get_entrance("The Lake -> Hall of Heroes"), cleared("The Lake") & CanReachLocation("Chalice: The Lake"))
    self.set_rule(self.get_entrance("Pumpkin Gorge -> Hall of Heroes"), cleared("Pumpkin Gorge") & CanReachLocation("Chalice: Pumpkin Gorge"))
    self.set_rule(self.get_entrance("Pumpkin Serpent -> Hall of Heroes"), cleared("Pumpkin Serpent") & CanReachLocation("Chalice: Pumpkin Serpent"))
    self.set_rule(
        self.get_entrance("The Sleeping Village -> Hall of Heroes"), cleared("Sleeping Village") & CanReachLocation("Chalice: Sleeping Village")
    )
    self.set_rule(
        self.get_entrance("Pools of the Ancient Dead -> Hall of Heroes"),
        cleared("Pools of the Ancient Dead") & CanReachLocation("Chalice: Pools of the Ancient Dead"),
    )
    self.set_rule(self.get_entrance("Asylum Grounds -> Hall of Heroes"), cleared("Asylum Grounds") & CanReachLocation("Chalice: Asylum Grounds"))
    self.set_rule(
        self.get_entrance("Inside the Asylum -> Hall of Heroes"), cleared("Inside the Asylum") & CanReachLocation("Chalice: Inside the Asylum")
    )
    self.set_rule(self.get_entrance("Enchanted Earth -> Hall of Heroes"), cleared("Enchanted Earth") & CanReachLocation("Chalice: Enchanted Earth"))
    self.set_rule(
        self.get_entrance("The Gallows Gauntlet -> Hall of Heroes"),
        cleared("The Gallows Gauntlet") & CanReachLocation("Chalice: The Gallows Gauntlet"),
    )
    self.set_rule(
        self.get_entrance("The Haunted Ruins -> Hall of Heroes"), cleared("The Haunted Ruins") & CanReachLocation("Chalice: The Haunted Ruins")
    )
    self.set_rule(self.get_entrance("The Ghost Ship -> Hall of Heroes"), cleared("Ghost Ship") & CanReachLocation("Chalice: Ghost Ship"))
    self.set_rule(
        self.get_entrance("The Entrance Hall -> Hall of Heroes"), cleared("The Entrance Hall") & CanReachLocation("Chalice: The Entrance Hall")
    )
    self.set_rule(self.get_entrance("The Time Device -> Hall of Heroes"), cleared("The Time Device") & CanReachLocation("Chalice: The Time Device"))
    if self.options.include_ant_hill_in_checks.value == IncludeAntHillInChecksToggle.option_true:
        self.set_rule(self.get_entrance("Ant Hill -> Hall of Heroes"), cleared("Ant Hill") & CanReachLocation("Chalice: Ant Hill"))
