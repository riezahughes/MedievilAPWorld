import dataclasses
from typing import TYPE_CHECKING

from typing_extensions import override

from BaseClasses import CollectionState, Entrance, Location
from rule_builder.rules import CanReachLocation, Has, HasAll, Rule, True_
from .Options import IncludeAntHillInChecksToggle, IncludeChalicesInChecksToggle, BookSanityToggle, GargoyleSanityToggle

if TYPE_CHECKING:
    from . import MedievilWorld


def weapon(name: str) -> Rule:
    return Has(f"Equipment: {name}")


def key_items(*names: str) -> Rule:
    return HasAll(*[f"Key Item: {name}" for name in names])


def cleared(level: str) -> Rule:
    return CanReachLocation(f"Cleared: {level}")


DARING_DASH = Has("Skill: Daring Dash")

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
    self.set_rule(self.get_entrance("Map -> The Graveyard"), cleared("Dan's Crypt"))
    self.set_rule(self.get_entrance("Map -> Cemetery Hill"), cleared("The Graveyard"))
    self.set_rule(
        self.get_entrance("Map -> The Hilltop Mausoleum"),
        cleared("Cemetery Hill") & (weapon("Club") | weapon("Hammer")),
    )
    self.set_rule(
        self.get_entrance("Map -> Return to the Graveyard"),
        cleared("The Hilltop Mausoleum") & key_items("Skull Key"),
    )
    self.set_rule(self.get_entrance("Map -> Enchanted Earth"), cleared("Return to the Graveyard"))
    self.set_rule(self.get_entrance("Map -> Scarecrow Fields"), cleared("Return to the Graveyard"))
    self.set_rule(self.get_entrance("Map -> The Sleeping Village"), cleared("Scarecrow Fields"))
    self.set_rule(self.get_entrance("Map -> Pumpkin Gorge"), cleared("Scarecrow Fields"))
    self.set_rule(
        self.get_entrance("Map -> Asylum Grounds"),
        cleared("Sleeping Village") & key_items("Crucifix Cast", "Landlords Bust", "Crucifix"),
    )
    self.set_rule(self.get_entrance("Map -> Inside the Asylum"), cleared("Asylum Grounds"))
    self.set_rule(
        self.get_entrance("Map -> Pumpkin Serpent"),
        cleared("Pumpkin Gorge") & key_items("Witches Talisman"),
    )
    self.set_rule(
        self.get_entrance("Map -> Pools of the Ancient Dead"),
        cleared("Enchanted Earth") & key_items("Shadow Talisman", "Shadow Artefact") & REQUIRED_SOULS,
    )
    self.set_rule(self.get_entrance("Map -> The Lake"), cleared("Pools of the Ancient Dead"))
    self.set_rule(self.get_entrance("Map -> The Crystal Caves"), cleared("The Lake"))
    self.set_rule(
        self.get_entrance("Map -> The Gallows Gauntlet"),
        cleared("The Crystal Caves")
        & weapon("Dragon Armour")
        & key_items("Dragon Gem - Pumpkin Serpent", "Dragon Gem - Inside the Asylum"),
    )
    self.set_rule(
        self.get_entrance("Map -> The Haunted Ruins"),
        cleared("The Gallows Gauntlet") & key_items("King Peregrine's Crown") & DARING_DASH,
    )
    self.set_rule(self.get_entrance("Map -> The Ghost Ship"), cleared("The Haunted Ruins"))
    self.set_rule(self.get_entrance("Map -> The Entrance Hall"), cleared("Ghost Ship"))
    self.set_rule(self.get_entrance("Map -> The Time Device"), cleared("The Entrance Hall"))
    self.set_rule(self.get_entrance("Map -> Zaroks Lair"), cleared("The Time Device"))


def set_open_level_progression(self: "MedievilWorld") -> None:
    self.set_rule(self.get_entrance("Map -> Cemetery Hill"), weapon("Club") | weapon("Hammer"))
    self.set_rule(self.get_entrance("Map -> Return to the Graveyard"), key_items("Skull Key"))
    self.set_rule(
        self.get_entrance("Map -> Asylum Grounds"), key_items("Crucifix Cast", "Landlords Bust", "Crucifix")
    )
    self.set_rule(self.get_entrance("Map -> Pumpkin Serpent"), key_items("Witches Talisman"))
    self.set_rule(
        self.get_entrance("Map -> Pools of the Ancient Dead"),
        key_items("Shadow Talisman", "Shadow Artefact") & REQUIRED_SOULS,
    )
    self.set_rule(self.get_entrance("Map -> The Gallows Gauntlet"), weapon("Dragon Armour"))
    self.set_rule(
        self.get_entrance("Map -> The Haunted Ruins"), key_items("King Peregrine's Crown") & DARING_DASH
    )


def set_ant_hill_rules_vanilla(self: "MedievilWorld") -> None:
    self.set_rule(
        self.get_entrance("Enchanted Earth -> Ant Hill"),
        cleared("Return to the Graveyard") & key_items("Witches Talisman"),
    )


def set_ant_hill_rules_open(self: "MedievilWorld") -> None:
    self.set_rule(self.get_entrance("Enchanted Earth -> Ant Hill"), key_items("Witches Talisman"))


def set_hall_of_heroes_progression(self: "MedievilWorld", max_chalice_count: int) -> None:
    # hall of heroes rules
    self.set_rule(self.get_entrance("Map -> Hall of Heroes"), HasNumberOfChalices(1))

    for i in range(1, max_chalice_count + 1):
        location_name = f"Chalice Reward {i}"
        self.set_rule(self.get_location(location_name), HasNumberOfChalices(i))


def set_rune_blocks(self: "MedievilWorld", locations: list[str], rune: str) -> None:
    for location in locations:
        if self.options.booksanity.value == BookSanityToggle.option_false and "Book:" in location:
            continue
        if self.options.gargoylesanity.value == GargoyleSanityToggle.option_false and "Gargoyle:" in location:
            continue
        if self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false and "Chalice:" in location:
            continue
        layer_rule(self, self.get_location(location), Has(rune))


def set_breakable_locations(self: "MedievilWorld", locations: list[str]) -> None:
    for location in locations:
        if self.options.booksanity.value == BookSanityToggle.option_false and "Book:" in location:
            continue
        if self.options.gargoylesanity.value == GargoyleSanityToggle.option_false and "Gargoyle:" in location:
            continue
        if self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false and "Chalice:" in location:
            continue
        layer_rule(self, self.get_location(location), weapon("Club") | weapon("Hammer"))


def set_dashable_locations(self: "MedievilWorld", locations: list[str]) -> None:
    for location in locations:
        if self.options.booksanity.value == BookSanityToggle.option_false and "Book:" in location:
            continue
        if self.options.gargoylesanity.value == GargoyleSanityToggle.option_false and "Gargoyle:" in location:
            continue
        if self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false and "Chalice:" in location:
            continue
        layer_rule(self, self.get_location(location), DARING_DASH)


def set_vanilla_runesanity_rules(self: "MedievilWorld") -> None:
    print("Vanilla Runesanity being created: ")
    layer_rule(
        self,
        self.get_entrance("Map -> The Graveyard"),
        HasAll("Earth Rune: The Graveyard", "Chaos Rune: The Graveyard"),
    )
    layer_rule(
        self,
        self.get_entrance("Map -> The Hilltop Mausoleum"),
        HasAll(
            "Moon Rune: The Hilltop Mausoleum", "Earth Rune: The Hilltop Mausoleum", "Chaos Rune: The Hilltop Mausoleum"
        ),
    )
    layer_rule(
        self, self.get_entrance("Map -> Return to the Graveyard"), Has("Star Rune: Return to the Graveyard")
    )
    layer_rule(
        self,
        self.get_entrance("Map -> Enchanted Earth"),
        HasAll("Earth Rune: Enchanted Earth", "Star Rune: Enchanted Earth"),
    )
    layer_rule(
        self,
        self.get_entrance("Map -> Scarecrow Fields"),
        HasAll("Earth Rune: Scarecrow Fields", "Chaos Rune: Scarecrow Fields", "Moon Rune: Scarecrow Fields"),
    )
    layer_rule(
        self,
        self.get_entrance("Map -> The Sleeping Village"),
        HasAll(
            "Earth Rune: The Sleeping Village", "Chaos Rune: The Sleeping Village", "Moon Rune: The Sleeping Village"
        ),
    )
    layer_rule(
        self,
        self.get_entrance("Map -> Pumpkin Gorge"),
        HasAll(
            "Earth Rune: Pumpkin Gorge",
            "Chaos Rune: Pumpkin Gorge",
            "Moon Rune: Pumpkin Gorge",
            "Time Rune: Pumpkin Gorge",
            "Star Rune: Pumpkin Gorge",
        ),
    )
    layer_rule(self, self.get_entrance("Map -> Asylum Grounds"), Has("Chaos Rune: The Asylum Grounds"))
    layer_rule(self, self.get_entrance("Map -> Inside the Asylum"), Has("Earth Rune: Inside the Asylum"))
    layer_rule(
        self, self.get_entrance("Map -> Pools of the Ancient Dead"), Has("Chaos Rune: Pools of the Ancient Dead")
    )
    layer_rule(
        self,
        self.get_entrance("Map -> The Lake"),
        HasAll("Chaos Rune: The Lake", "Earth Rune: The Lake", "Star Rune: The Lake", "Time Rune: The Lake"),
    )
    layer_rule(
        self,
        self.get_entrance("Map -> The Crystal Caves"),
        HasAll("Earth Rune: The Crystal Caves", "Star Rune: The Crystal Caves"),
    )
    layer_rule(self, self.get_entrance("Map -> The Gallows Gauntlet"), Has("Star Rune: The Gallows Gauntlet"))
    layer_rule(
        self,
        self.get_entrance("Map -> The Haunted Ruins"),
        HasAll("Chaos Rune: The Haunted Ruins", "Earth Rune: The Haunted Ruins"),
    )
    layer_rule(
        self,
        self.get_entrance("Map -> The Ghost Ship"),
        HasAll("Chaos Rune: Ghost Ship", "Moon Rune: Ghost Ship", "Star Rune: Ghost Ship"),
    )
    layer_rule(
        self,
        self.get_entrance("Map -> The Time Device"),
        HasAll(
            "Chaos Rune: The Time Device", "Earth Rune: The Time Device", "Moon Rune: The Time Device", "Time Rune: The Time Device"
        ),
    )


def set_open_runesanity_rules(self: "MedievilWorld") -> None:
    print(" Open Runesanity being created: ")

    # The Graveyard
    set_rune_blocks(self, ["Chaos Rune: The Graveyard", "Gold Coins: Near Chaos Rune - TG"], "Earth Rune: The Graveyard")

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
            "Gargoyle: End of Level - TG",
            "Cleared: The Graveyard",
            "Chalice: The Graveyard",
        ],
        "Chaos Rune: The Graveyard",
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
            "Book: Thieving Imps - HM",
            "Chalice: The Hilltop Mausoleum",
        ],
        "Earth Rune: The Hilltop Mausoleum",
    )

    set_rune_blocks(
        self,
        [
            "Key Item: Sheet Music - HM",
            "Energy Vial: Moon Room - HM",
            "Gold Coins: Chest in Moon Room - HM",
        ],
        "Moon Rune: The Hilltop Mausoleum",
    )

    set_rune_blocks(
        self,
        [
            "Key Item: Skull Key - HM",
            "Equipment: Daggers near Block Puzzle - HM",
            "Equipment: Copper Shield near Block Puzzle - HM",
            "Cleared: The Hilltop Mausoleum",
        ],
        "Chaos Rune: The Hilltop Mausoleum",
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
            "Book: Daring Dash - RTG",
            "Gargoyle: Exit - RTG",
            "Cleared: Return to the Graveyard",
            "Chalice: Return to the Graveyard",
        ],
        "Star Rune: Return to the Graveyard",
    )

    # Scarecrow Fields

    set_rune_blocks(
        self,
        [
            "Earth Rune: Scarecrow Fields",
            "Equipment: Club Inside Hut - SF",
        ],
        "Moon Rune: Scarecrow Fields",
    )

    set_rune_blocks(self, ["Chaos Rune: Scarecrow Fields", "Equipment: Silver Shield Behind Windmill - SF"], "Earth Rune: Scarecrow Fields")

    set_rune_blocks(
        self,
        [
            "Key Item: Harvester Parts - SF",
            "Equipment: Copper Shield in Chest In the Barn - SF",
            "Gold Coins: Bag in the Barn - SF",
            "Gold Coins: Cornfield Square near Barn - SF",
            "Gold Coins: Cornfield Path 1 - SF",
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
        ],
        "Chaos Rune: Scarecrow Fields",
    )

    # Enchanted Earth:

    set_rune_blocks(
        self,
        [
            "Key Item: Shadow Talisman - EE",
            "Star Rune: Enchanted Earth",
            "Energy Vial: Shadow Talisman Cave - EE",
            "Book: Take the Talisman - EE",
            "Gargoyle: Outside Demon Entrance - EE",
            "Gargoyle: Outside Demon Exit- EE",
        ],
        "Earth Rune: Enchanted Earth",
    )

    set_rune_blocks(
        self,
        [
            "Energy Vial: Left of Tree Drop - EE",
            "Energy Vial: Right of Tree Drop - EE",
            "Gold Coins: Chest Left of Fountain - EE",
            "Gold Coins: Chest Top of Fountain - EE",
            "Gold Coins: Chest Right of Fountain - EE",
            "Cleared: Enchanted Earth",
            "Chalice: Enchanted Earth",
        ],
        "Star Rune: Enchanted Earth",
    )

    # The Sleeping Village

    set_rune_blocks(
        self,
        [
            "Earth Rune: Sleeping Village",
            "Gold Coins: Bag in Barrel at Inn - SV",
            "Gold Coins: Bag in Barrel at bottom of Inn Stairs - SV",
            "Gold Coins: Bag in Barrel Behind Inn Stairs - SV",
            "Book: Mayors Bust - SV",
        ],
        "Moon Rune: The Sleeping Village",
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
        "Earth Rune: The Sleeping Village",
    )

    set_rune_blocks(
        self,
        [
            "Gold Coins: Bag in Library - SV",
            "Key Item: Crucifix Cast - SV",
            "Book: History of Gallowmere 1 - SV",
            "Book: History of Gallowmere 2 - SV",
            "Book: History of Gallowmere 3- SV",
            "Book: History of Gallowmere 4- SV",
            "Book: Heroes From History- SV",
            "Book: Tourist Guide 1 - SV",
            "Book: Tourist Guide 2 - SV",
            "Book: Mayor Memoire - SV",
        ],
        "Chaos Rune: The Sleeping Village",
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
            "Key Item: Soul Helmet 8 - PAD",
            "Cleared: Pools of the Ancient Dead",
            "Chalice: Pools of the Ancient Dead",
        ],
        "Chaos Rune: Pools of the Ancient Dead",
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
        ],
        "Time Rune: The Lake",
    )

    set_rune_blocks(
        self,
        [
            "Cleared: The Lake",
            "Chalice: The Lake",
        ],
        "Star Rune: The Lake",
    )

    # Crystal Caves

    set_rune_blocks(
        self,
        [
            "Equipment: Dragon Armour - CC",
            "Energy Vial: Dragon Room 1st Platform - CC",
            "Energy Vial: Dragon Room 3rd Platform - CC",
            "Gold Coins: Chest in Crystal after Pool - CC",
            "Gold Coins: Chest in Crystal After Earth Door - CC",
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
            "Star Rune: The Crystal Caves",
        ],
        "Earth Rune: The Crystal Caves",
    )

    set_rune_blocks(self, ["Cleared: The Crystal Caves", "Chalice: The Crystal Caves"], "Star Rune: The Crystal Caves")

    #  The Gallows Gauntlet

    set_rune_blocks(self, ["Cleared: The Gallows Gauntlet", "Chalice: The Gallows Gauntlet"], "Star Rune: The Gallows Gauntlet")

    # Asylum Grounds

    set_rune_blocks(
        self,
        [
            "Energy Vial: Near Bishop - AG",
            "Energy Vial: Near King - AG",
            "Gold Coins: Bag in Rat Grave - AG",
            "Gold Coins: Behind Chaos Gate - AG",
            "Gold Coins: Behind Elephant in Grave - AG",
            "Cleared: Asylum Grounds",
            "Chalice: Asylum Grounds",
        ],
        "Chaos Rune: The Asylum Grounds",
    )

    # Inside the Asylum

    set_rune_blocks(self, ["Key Item: Dragon Gem - IA"], "Earth Rune: Inside the Asylum")

    # Pumpkin Gorge

    set_rune_blocks(
        self,
        [
            "Energy Vial: In Moon Hut - PG",
            "Chaos Rune: Pumpkin Gorge",
        ],
        "Moon Rune: Pumpkin Gorge",
    )

    set_rune_blocks(
        self,
        [
            "Earth Rune: Pumpkin Gorge",
        ],
        "Chaos Rune: Pumpkin Gorge",
    )

    set_rune_blocks(
        self,
        [
            "Star Rune: Pumpkin Gorge",
            "Energy Vial: Top of Hill - PG",
            "Equipment: Silver Shield in Chest at Top of Hill - PG",
        ],
        "Earth Rune: Pumpkin Gorge",
    )

    set_rune_blocks(self, ["Time Rune: Pumpkin Gorge"], "Star Rune: Pumpkin Gorge")

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
        "Time Rune: Pumpkin Gorge",
    )

    # Pumpkin Serpent

    ## no rune logic

    # Haunted Ruins

    set_rune_blocks(self, ["Earth Rune: The Haunted Ruins"], "Chaos Rune: The Haunted Ruins")

    set_rune_blocks(
        self,
        [
            "Gold Coins: Chest at Catapult 1 - HR",
            "Gold Coins: Chest at Catapult 2 - HR",
            "Gold Coins: Chest at Catapult 3 - HR",
            "Book: Escape - HR",
            "Cleared: The Haunted Ruins",
            "Chalice: The Haunted Ruins",
        ],
        "Earth Rune: The Haunted Ruins",
    )

    # Ghost Ship

    set_rune_blocks(
        self,
        [
            "Energy Vial: In Cabin - GS",
            "Star Rune: Ghost Ship",
        ],
        "Moon Rune: Ghost Ship",
    )

    set_rune_blocks(self, ["Chaos Rune: Ghost Ship"], "Star Rune: Ghost Ship")

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
        "Chaos Rune: Ghost Ship",
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
        "Time Rune: The Time Device",
    )

    set_rune_blocks(
        self,
        [
            "Gold Coins: Bag at Earth Station 1 - TD",
            "Gold Coins: Bag at Earth Station 2 - TD",
            "Gold Coins: Bag at Earth Station 3 - TD",
            "Moon Rune: The Time Device",
            "Cleared: The Time Device",
            "Chalice: The Time Device",
        ],
        "Earth Rune: The Time Device",
    )

    set_dashable_locations(
        self,
        [
            "Earth Rune: The Hilltop Mausoleum",
            "Gold Coins: Lone Pillar 1 - TD",
            "Gold Coins: Lone Pillar 2 - TD",
            "Gold Coins: Lone Pillar 3 - TD",
            "Life Bottle: Dan's Crypt - Behind Wall",
            "Gold Coins: Behind Wall in Crypt - Left - DC",
            "Gold Coins: Behind Wall in Crypt - Right - DC",
        ],
    )

    set_breakable_locations(
        self,
        [
            "Earth Rune: The Hilltop Mausoleum",
            "Energy Vial: Right Coffin - HM",
            "Energy Vial: Near Rune on Left Ramp - HM",
            "Book: Thieving Imps - HM",
            "Key Item: Sheet Music - HM",
            "Energy Vial: Moon Room - HM",
            "Gold Coins: Chest in Moon Room - HM",
            "Key Item: Skull Key - HM",
            "Equipment: Daggers near Block Puzzle - HM",
            "Equipment: Copper Shield near Block Puzzle - HM",
            "Cleared: The Hilltop Mausoleum",
            "Gold Coins: Bag in Left Barrel at Blacksmith - SV",
            "Gold Coins: Bag in Right Barrel at Blacksmith - SV",
            "Gold Coins: Bag in Barrel at Inn - SV",
            "Key Item: Crucifix Cast - SV",
            "Gold Coins: Bag in Library - SV",
            "Book: Mayor Memoire - SV",
            "Earth Rune: Sleeping Village",
            "Gold Coins: Bag in Barrel at bottom of Inn Stairs - SV",
            "Gold Coins: Bag in Barrel Behind Inn Stairs - SV",
            "Gold Coins: Bag In Switch Bust Barrel - SV",
            "Gold Coins: Bag In Top Bust Barrel - SV",
            "Equipment: Dragon Armour - CC",
            "Moon Rune: Pumpkin Gorge",
            "Equipment: Club in Chest in Tunnel - PG",
            "Energy Vial: In Coop - PG",
            "Energy Vial: Chalice Path - PG",
            "Gold Coins: Bag Behind Rocks At Start - PG",
            "Gold Coins: Chest in Coop 1 - PG",
            "Gold Coins: Chest in Coop 2 - PG",
            "Gold Coins: Chest in Coop 3 - PG",
            "Gold Coins: Chest Near Chalice - PG",
            "Chaos Rune: Pumpkin Gorge",
            "Energy Vial: In Moon Hut - PG",
            "Earth Rune: Pumpkin Gorge",
            "Gold Coins: Bag in Mushroom Area - PG",
            "Book: Mushrooms - PG",
            "Star Rune: Pumpkin Gorge",
            "Equipment: Silver Shield in Chest at Top of Hill - PG",
            "Energy Vial: Top of Hill - PG",
            "Time Rune: Pumpkin Gorge",
            "Energy Vial: Vine Patch Left - PG",
            "Energy Vial: Vine Patch Right - PG",
            "Energy Vial: Boulders After Time Rune - PG",
            "Gold Coins: Chest at Boulders after Time Rune - PG",
            "Gargoyle: Exit - PG",
            "Cleared: Pumpkin Gorge",
            "Chalice: Pumpkin Gorge",
            "Chalice: The Haunted Ruins",
            "Cleared: Ghost Ship",
            "Life Bottle: Dan's Crypt - Behind Wall",
            "Gold Coins: Behind Wall in Crypt - Left - DC",
            "Gold Coins: Behind Wall in Crypt - Right - DC",
        ],
    )


def set_locked_items_locations(self: "MedievilWorld") -> None:
    self.set_rule(
        self.get_entrance("Cemetery Hill -> Locked Items CH"),
        DARING_DASH | weapon("Club") | weapon("Hammer"),
    )
    self.set_rule(self.get_entrance("The Hilltop Mausoleum -> Locked Items HM"), key_items("Sheet Music"))
    self.set_rule(self.get_entrance("Scarecrow Fields -> Locked Items SF"), key_items("Harvester Parts"))
    self.set_rule(self.get_entrance("The Sleeping Village -> Locked Items SV"), key_items("Crucifix"))
