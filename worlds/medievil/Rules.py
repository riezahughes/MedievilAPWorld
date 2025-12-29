from worlds.generic.Rules import set_rule, add_rule
from BaseClasses import CollectionState, Iterable
from .Options import IncludeAntHillInChecksToggle, IncludeChalicesInChecksToggle, BookSanityToggle, GargoyleSanityToggle


def is_level_cleared(self, location: str, state: CollectionState):
    return state.can_reach_location("Cleared: " + location, self.player)


def has_daring_dash(self, state: CollectionState):
    return state.has("Skill: Daring Dash", self.player)


def is_boss_defeated(self, boss: str, state: CollectionState):  # can used later
    return state.has("Boss: " + boss, self.player, 1)


def has_keyitems_required(self, items: list[str], state: CollectionState):
    passed_check = True
    for item in items:
        if state.has("Key Item: " + item, self.player, 1) is False:
            passed_check = False
    return passed_check


def has_weapon_required(self, weapon: str, state: CollectionState):
    return state.has("Equipment: " + weapon, self.player, 1)


def has_required_souls(self, state: CollectionState):
    return state.has_all(
        [
            "Key Item: Soul Helmet 1",
            "Key Item: Soul Helmet 2",
            "Key Item: Soul Helmet 3",
            "Key Item: Soul Helmet 4",
            "Key Item: Soul Helmet 5",
            "Key Item: Soul Helmet 6",
            "Key Item: Soul Helmet 7",
            "Key Item: Soul Helmet 8",
        ],
        self.player,
    )


def has_required_amber(self, state: CollectionState):
    return state.has_all(
        [
            "Key Item: Amber 1",
            "Key Item: Amber 2",
            "Key Item: Amber 3",
            "Key Item: Amber 4",
            "Key Item: Amber 5",
            "Key Item: Amber 6",
            "Key Item: Amber 7",
        ],
        self.player,
    )


def has_number_of_chalices(self, count, state: CollectionState):
    if self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false:
        return True
    # looks at vanilla chalices currently. So it's based on locations
    chalice_list = [
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
    ]

    # adds ant hill chalice if it's not excluded
    if self.options.include_ant_hill_in_checks.value == IncludeAntHillInChecksToggle.option_true:
        chalice_list.append("Chalice: Ant Hill")

    collected_chalices = 0
    for chalice_location in chalice_list:
        if state.can_reach_location(chalice_location, self.player):
            collected_chalices += 1
    return collected_chalices >= count


def set_vanilla_level_progression(self):
    print("Vanilla Progression being created: ")
    set_rule(self.get_entrance("Map -> The Graveyard"), lambda state: is_level_cleared(self, "Dan's Crypt", state))
    set_rule(self.get_entrance("Map -> Cemetery Hill"), lambda state: is_level_cleared(self, "The Graveyard", state))
    set_rule(
        self.get_entrance("Map -> The Hilltop Mausoleum"),
        lambda state: is_level_cleared(self, "Cemetery Hill", state)
        and (has_weapon_required(self, "Club", state) or has_weapon_required(self, "Hammer", state)),
    )
    set_rule(
        self.get_entrance("Map -> Return to the Graveyard"),
        lambda state: is_level_cleared(self, "The Hilltop Mausoleum", state) and has_keyitems_required(self, ["Skull Key"], state),
    )
    set_rule(self.get_entrance("Map -> Enchanted Earth"), lambda state: is_level_cleared(self, "Return to the Graveyard", state))
    set_rule(self.get_entrance("Map -> Scarecrow Fields"), lambda state: is_level_cleared(self, "Return to the Graveyard", state))
    set_rule(self.get_entrance("Map -> The Sleeping Village"), lambda state: is_level_cleared(self, "Scarecrow Fields", state))
    set_rule(self.get_entrance("Map -> Pumpkin Gorge"), lambda state: is_level_cleared(self, "Scarecrow Fields", state))
    set_rule(
        self.get_entrance("Map -> Asylum Grounds"),
        lambda state: is_level_cleared(self, "Sleeping Village", state)
        and has_keyitems_required(self, ["Crucifix Cast", "Landlords Bust", "Crucifix"], state),
    )
    set_rule(self.get_entrance("Map -> Inside the Asylum"), lambda state: is_level_cleared(self, "Asylum Grounds", state))
    set_rule(
        self.get_entrance("Map -> Pumpkin Serpent"),
        lambda state: is_level_cleared(self, "Pumpkin Gorge", state) and has_keyitems_required(self, ["Witches Talisman"], state),
    )
    set_rule(
        self.get_entrance("Map -> Pools of the Ancient Dead"),
        lambda state: is_level_cleared(self, "Enchanted Earth", state)
        and has_keyitems_required(self, ["Shadow Talisman", "Shadow Artefact"], state)
        and has_required_souls(self, state),
    )
    set_rule(self.get_entrance("Map -> The Lake"), lambda state: is_level_cleared(self, "Pools of the Ancient Dead", state))
    set_rule(self.get_entrance("Map -> The Crystal Caves"), lambda state: is_level_cleared(self, "The Lake", state))
    set_rule(
        self.get_entrance("Map -> The Gallows Gauntlet"),
        lambda state: is_level_cleared(self, "The Crystal Caves", state)
        and has_keyitems_required(self, ["Dragon Gem - Pumpkin Serpent", "Dragon Gem - Inside the Asylum"], state),
    )
    set_rule(
        self.get_entrance("Map -> The Haunted Ruins"),
        lambda state: is_level_cleared(self, "The Gallows Gauntlet", state)
        and has_keyitems_required(self, ["King Peregrine's Crown"], state)
        and has_daring_dash(self, state),
    )
    set_rule(self.get_entrance("Map -> The Ghost Ship"), lambda state: is_level_cleared(self, "The Haunted Ruins", state))
    set_rule(self.get_entrance("Map -> The Entrance Hall"), lambda state: is_level_cleared(self, "Ghost Ship", state))
    set_rule(self.get_entrance("Map -> The Time Device"), lambda state: is_level_cleared(self, "The Entrance Hall", state))
    set_rule(self.get_entrance("Map -> Zaroks Lair"), lambda state: is_level_cleared(self, "The Time Device", state))


def set_open_level_progression(self):
    set_rule(
        self.get_entrance("Map -> Cemetery Hill"),
        lambda state: has_weapon_required(self, "Club", state) or has_weapon_required(self, "Hammer", state),
    )
    set_rule(self.get_entrance("Map -> Return to the Graveyard"), lambda state: has_keyitems_required(self, ["Skull Key"], state))
    set_rule(
        self.get_entrance("Map -> Asylum Grounds"), lambda state: has_keyitems_required(self, ["Crucifix Cast", "Landlords Bust", "Crucifix"], state)
    )
    set_rule(self.get_entrance("Map -> Pumpkin Serpent"), lambda state: has_keyitems_required(self, ["Witches Talisman"], state))
    set_rule(
        self.get_entrance("Map -> Pools of the Ancient Dead"),
        lambda state: has_keyitems_required(self, ["Shadow Talisman", "Shadow Artefact"], state) and has_required_souls(self, state),
    )
    set_rule(
        self.get_entrance("Map -> The Gallows Gauntlet"),
        lambda state: has_keyitems_required(self, ["Dragon Gem - Pumpkin Serpent", "Dragon Gem - Inside the Asylum"], state),
    )
    set_rule(
        self.get_entrance("Map -> The Haunted Ruins"),
        lambda state: has_keyitems_required(self, ["King Peregrine's Crown"], state) and has_daring_dash(self, state),
    )


def set_ant_hill_rules_vanilla(self):
    set_rule(
        self.get_entrance("Enchanted Earth -> Ant Hill"),
        lambda state: is_level_cleared(self, "Return to the Graveyard", state) and has_keyitems_required(self, ["Witches Talisman"], state),
    )


def set_ant_hill_rules_open(self):
    set_rule(self.get_entrance("Enchanted Earth -> Ant Hill"), lambda state: has_keyitems_required(self, ["Witches Talisman"], state))


def set_ant_hill_chalice(self):
    if self.options.chalice_win_count.value > 19:
        add_rule(self.get_location("Chalice Reward 20"), lambda state: has_number_of_chalices(self, 20, state))


def has_required_runes(self, runes: Iterable[str], state: CollectionState):
    return state.has_all(runes, self.player)


def set_rune_blocks(self, locations: list[str], rune: str):
    for location in locations:
        if self.options.booksanity.value == BookSanityToggle.option_false and "Book:" in location:
            continue
        if self.options.gargoylesanity.value == GargoyleSanityToggle.option_false and "Gargoyle:" in location:
            continue
        if self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false and "Chalice:" in location:
            continue
        set_rule(self.get_location(location), lambda state: has_required_runes(self, [rune], state))


def set_breakable_locations(self, locations: list[str]):
    for location in locations:
        if self.options.booksanity.value == BookSanityToggle.option_false and "Book:" in location:
            continue
        if self.options.gargoylesanity.value == GargoyleSanityToggle.option_false and "Gargoyle:" in location:
            continue
        if self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false and "Chalice:" in location:
            continue
        add_rule(self.get_location(location), lambda state: (has_weapon_required(self, "Club", state) or has_weapon_required(self, "Hammer", state)))


def set_dashable_locations(self, locations: list[str]):
    for location in locations:
        if self.options.booksanity.value == BookSanityToggle.option_false and "Book:" in location:
            continue
        if self.options.gargoylesanity.value == GargoyleSanityToggle.option_false and "Gargoyle:" in location:
            continue
        if self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false and "Chalice:" in location:
            continue
        add_rule(self.get_location(location), lambda state: has_daring_dash(self, state))


def set_vanilla_runesanity_rules(self):
    print("Vanilla Runesanity being created: ")
    add_rule(
        self.get_entrance("Map -> The Graveyard"),
        lambda state: has_required_runes(self, ["Earth Rune: The Graveyard", "Chaos Rune: The Graveyard"], state),
    )
    add_rule(
        self.get_entrance("Map -> The Hilltop Mausoleum"),
        lambda state: has_required_runes(
            self, ["Moon Rune: The Hilltop Mausoleum", "Earth Rune: The Hilltop Mausoleum", "Chaos Rune: The Hilltop Mausoleum"], state
        ),
    )
    add_rule(
        self.get_entrance("Map -> Return to the Graveyard"), lambda state: has_required_runes(self, ["Star Rune: Return to the Graveyard"], state)
    )
    add_rule(
        self.get_entrance("Map -> Enchanted Earth"),
        lambda state: has_required_runes(self, ["Earth Rune: Enchanted Earth", "Star Rune: Enchanted Earth"], state),
    )
    add_rule(
        self.get_entrance("Map -> Scarecrow Fields"),
        lambda state: has_required_runes(
            self, ["Earth Rune: Scarecrow Fields", "Chaos Rune: Scarecrow Fields", "Moon Rune: Scarecrow Fields"], state
        ),
    )
    add_rule(
        self.get_entrance("Map -> The Sleeping Village"),
        lambda state: has_required_runes(
            self, ["Earth Rune: The Sleeping Village", "Chaos Rune: The Sleeping Village", "Moon Rune: The Sleeping Village"], state
        ),
    )
    add_rule(
        self.get_entrance("Map -> Pumpkin Gorge"),
        lambda state: has_required_runes(
            self,
            [
                "Earth Rune: Pumpkin Gorge",
                "Chaos Rune: Pumpkin Gorge",
                "Moon Rune: Pumpkin Gorge",
                "Time Rune: Pumpkin Gorge",
                "Star Rune: Pumpkin Gorge",
            ],
            state,
        ),
    )
    add_rule(self.get_entrance("Map -> Asylum Grounds"), lambda state: has_required_runes(self, ["Chaos Rune: The Asylum Grounds"], state))
    add_rule(self.get_entrance("Map -> Inside the Asylum"), lambda state: has_required_runes(self, ["Earth Rune: Inside the Asylum"], state))
    add_rule(
        self.get_entrance("Map -> Pools of the Ancient Dead"),
        lambda state: has_required_runes(self, ["Chaos Rune: Pools of the Ancient Dead"], state),
    )
    add_rule(
        self.get_entrance("Map -> The Lake"),
        lambda state: has_required_runes(self, ["Chaos Rune: The Lake", "Earth Rune: The Lake", "Star Rune: The Lake", "Time Rune: The Lake"], state),
    )
    add_rule(
        self.get_entrance("Map -> The Crystal Caves"),
        lambda state: has_required_runes(self, ["Earth Rune: The Crystal Caves", "Star Rune: The Crystal Caves"], state),
    )
    add_rule(self.get_entrance("Map -> The Gallows Gauntlet"), lambda state: has_required_runes(self, ["Star Rune: The Gallows Gauntlet"], state))
    add_rule(
        self.get_entrance("Map -> The Haunted Ruins"),
        lambda state: has_required_runes(self, ["Chaos Rune: The Haunted Ruins", "Earth Rune: The Haunted Ruins"], state),
    )
    add_rule(
        self.get_entrance("Map -> The Ghost Ship"),
        lambda state: has_required_runes(self, ["Chaos Rune: Ghost Ship", "Moon Rune: Ghost Ship", "Star Rune: Ghost Ship"], state),
    )
    add_rule(
        self.get_entrance("Map -> The Time Device"),
        lambda state: has_required_runes(
            self, ["Chaos Rune: The Time Device", "Earth Rune: The Time Device", "Moon Rune: The Time Device", "Time Rune: The Time Device"], state
        ),
    )


def set_open_runesanity_rules(self):
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
            "Life Bottle: Dan's Crypt",
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


def set_hall_of_heroes_progression(self, max_chalice_count):
    # hall of heroes rules

    set_rule(self.get_entrance("Map -> Hall of Heroes"), lambda state: has_number_of_chalices(self, 1, state))

    for i in range(1, max_chalice_count + 1):
        location_name = f"Chalice Reward {i}"
        set_rule(self.get_location(location_name), lambda state: has_number_of_chalices(self, i, state))

    # keeping a copy of these for the history

    # # Canny Tim
    # set_rule(self.get_location("Chalice Reward 1"), lambda state: has_number_of_chalices(self, 1, state))
    # set_rule(self.get_location("Chalice Reward 2"), lambda state: has_number_of_chalices(self, 2, state))
    # # Stanyer Iron Hewer
    # set_rule(self.get_location("Chalice Reward 3"), lambda state: has_number_of_chalices(self, 3, state))
    # set_rule(self.get_location("Chalice Reward 4"), lambda state: has_number_of_chalices(self, 4, state))

    # # Woden the Mighty
    # set_rule(self.get_location("Chalice Reward 5"), lambda state: has_number_of_chalices(self, 5, state))
    # set_rule(self.get_location("Chalice Reward 6"), lambda state: has_number_of_chalices(self, 6, state))

    # # Imanzi Shongama
    # set_rule(self.get_location("Chalice Reward 7"), lambda state: has_number_of_chalices(self, 7, state))

    # # Ravenhooves the Archer
    # set_rule(self.get_location("Chalice Reward 8"), lambda state: has_number_of_chalices(self, 8, state))

    # # Bloodmonath
    # set_rule(self.get_location("Chalice Reward 9"), lambda state: has_number_of_chalices(self, 9, state))

    # # Ravenhooves the Archer
    # set_rule(self.get_location("Chalice Reward 10"), lambda state: has_number_of_chalices(self, 10, state))

    # # Karl Sturngard
    # set_rule(self.get_location("Chalice Reward 11"), lambda state: has_number_of_chalices(self, 11, state))

    # # Bloodmonath
    # set_rule(self.get_location("Chalice Reward 12"), lambda state: has_number_of_chalices(self, 12, state))

    # # Dirk Steadfast
    # set_rule(self.get_location("Chalice Reward 13"), lambda state: has_number_of_chalices(self, 13, state))

    # # Ravenhooves the Archer
    # set_rule(self.get_location("Chalice Reward 14"), lambda state: has_number_of_chalices(self, 14, state))

    # # Megwynne Stormbinder
    # set_rule(self.get_location("Chalice Reward 15"), lambda state: has_number_of_chalices(self, 15, state))

    # # Ravenhooves the Archer
    # set_rule(self.get_location("Chalice Reward 16"), lambda state: has_number_of_chalices(self, 16, state))

    # # Imanzi Shongama
    # set_rule(self.get_location("Chalice Reward 17"), lambda state: has_number_of_chalices(self, 17, state))

    # # Karl Sturngard
    # set_rule(self.get_location("Chalice Reward 18"), lambda state: has_number_of_chalices(self, 18, state))

    # # Dirk Steadfast
    # set_rule(self.get_location("Chalice Reward 19"), lambda state: has_number_of_chalices(self, 19, state))


def set_locked_items_locations(self):
    set_rule(
        self.get_entrance("Cemetery Hill -> Locked Items CH"),
        lambda state: (has_daring_dash(self, state) or has_weapon_required(self, "Club", state) or has_weapon_required(self, "Hammer", state)),
    )
    set_rule(self.get_entrance("The Hilltop Mausoleum -> Locked Items HM"), lambda state: has_keyitems_required(self, ["Sheet Music"], state))
    set_rule(self.get_entrance("Scarecrow Fields -> Locked Items SF"), lambda state: has_keyitems_required(self, ["Harvester Parts"], state))
