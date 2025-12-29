# world/dc2/__init__.py
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification, CollectionState
from Options import Toggle

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule

from .Items import MedievilItem, MedievilItemCategory, item_dictionary, key_item_names, item_descriptions, BuildItemPool
from .Locations import MedievilLocation, MedievilLocationCategory, MedievilLocationData, location_tables, location_dictionary
from .Options import (
    MedievilOption,
    GoalOptions,
    IncludeAntHillInChecksToggle,
    IncludeChalicesInChecksToggle,
    BookSanityToggle,
    GargoyleSanityToggle,
    ProgressionOptions,
    RuneSanityToggle,
)
from .Rules import (
    set_ant_hill_rules_open,
    set_ant_hill_rules_vanilla,
    set_vanilla_level_progression,
    set_open_level_progression,
    set_ant_hill_chalice,
    set_hall_of_heroes_progression,
    set_locked_items_locations,
    set_open_runesanity_rules,
    set_vanilla_runesanity_rules,
)
from .VictoryConditions import defeat_zarok_and_get_chalices_victory, defeat_zarok_victory, get_chalices_victory


class MedievilWeb(WebWorld):
    bug_report_page = ""
    theme = "stone"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Medievil randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["RiezaHughes"],
    )

    tutorials = [setup_en]


class MedievilWorld(World):
    """
    Medievil is a game about an idiot who died and was accidentally resurrected as a one eyed bandit to fight knockoff voldemort.
    """

    game: str = "Medievil"
    explicit_indirect_conditions = False
    options_dataclass = MedievilOption
    options: MedievilOption
    topology_present: bool = True
    web = MedievilWeb()
    data_version = 0
    base_id = 1230000
    enabled_location_categories: Set[MedievilLocationCategory]
    required_client_version = (0, 5, 0)
    item_name_to_id = MedievilItem.get_name_to_id()
    location_name_to_id = MedievilLocation.get_name_to_id()
    item_name_groups = {}
    item_descriptions = item_descriptions

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []
        self.enabled_location_categories = set()

    def generate_early(self):
        self.enabled_location_categories.add(MedievilLocationCategory.PROGRESSION)
        self.enabled_location_categories.add(MedievilLocationCategory.WEAPON)
        self.enabled_location_categories.add(MedievilLocationCategory.CHALICE_PICKUP)
        self.enabled_location_categories.add(MedievilLocationCategory.CHALICE_REWARD)
        self.enabled_location_categories.add(MedievilLocationCategory.BOOK)
        self.enabled_location_categories.add(MedievilLocationCategory.GARGOYLE)
        self.enabled_location_categories.add(MedievilLocationCategory.FUN)
        self.enabled_location_categories.add(MedievilLocationCategory.LEVEL_END)
        self.enabled_location_categories.add(MedievilLocationCategory.DYNAMIC_ITEM)

    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}

        regions["Menu"] = self.create_region("Menu", [])

        list_of_regions = [
            "Map",
            "Hall of Heroes",
            "Dan's Crypt",
            "The Graveyard",
            "Return to the Graveyard",
            "Cemetery Hill",
            "The Hilltop Mausoleum",
            "Scarecrow Fields",
            "The Crystal Caves",
            "The Lake",
            "Pumpkin Gorge",
            "Pumpkin Serpent",
            "The Sleeping Village",
            "Pools of the Ancient Dead",
            "Asylum Grounds",
            "Inside the Asylum",
            "Enchanted Earth",
            "The Gallows Gauntlet",
            "The Haunted Ruins",
            "The Ghost Ship",
            "The Entrance Hall",
            "The Time Device",
            "Zaroks Lair",
            "Locked Items DC",
            "Locked Items CH",
            "Locked Items HM",
            "Locked Items SF",
        ]

        if self.options.include_ant_hill_in_checks.value == IncludeAntHillInChecksToggle.option_true:
            list_of_regions.insert(8, "Ant Hill")
        # else:
        #     location_tables.pop("Ant Hill")

        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in list_of_regions})

        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{from_region} -> {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])

        create_connection("Menu", "Dan's Crypt")

        # Can go from the map to every location
        create_connection("Map", "Dan's Crypt")
        create_connection("Map", "The Graveyard")
        create_connection("Map", "Return to the Graveyard")
        create_connection("Map", "Cemetery Hill")
        create_connection("Map", "The Hilltop Mausoleum")
        create_connection("Map", "Scarecrow Fields")
        create_connection("Map", "The Crystal Caves")
        create_connection("Map", "The Lake")
        create_connection("Map", "Pumpkin Gorge")
        create_connection("Map", "Pumpkin Serpent")
        create_connection("Map", "The Sleeping Village")
        create_connection("Map", "Pools of the Ancient Dead")
        create_connection("Map", "Asylum Grounds")
        create_connection("Map", "Inside the Asylum")
        create_connection("Map", "Enchanted Earth")
        create_connection("Map", "The Gallows Gauntlet")
        create_connection("Map", "The Haunted Ruins")
        create_connection("Map", "The Ghost Ship")
        create_connection("Map", "The Entrance Hall")
        create_connection("Map", "The Time Device")
        create_connection("Map", "Zaroks Lair")

        # can go from every location back to the map
        create_connection("Dan's Crypt", "Map")
        create_connection("The Graveyard", "Map")
        create_connection("Return to the Graveyard", "Map")
        create_connection("Cemetery Hill", "Map")
        create_connection("The Hilltop Mausoleum", "Map")
        create_connection("Scarecrow Fields", "Map")
        create_connection("Enchanted Earth", "Map")
        create_connection("The Crystal Caves", "Map")
        create_connection("The Lake", "Map")
        create_connection("Pumpkin Gorge", "Map")
        create_connection("Pumpkin Serpent", "Map")
        create_connection("The Sleeping Village", "Map")
        create_connection("Pools of the Ancient Dead", "Map")
        create_connection("Asylum Grounds", "Map")
        create_connection("Inside the Asylum", "Map")
        create_connection("The Gallows Gauntlet", "Map")
        create_connection("The Haunted Ruins", "Map")
        create_connection("The Ghost Ship", "Map")
        create_connection("The Entrance Hall", "Map")
        create_connection("The Time Device", "Map")

        if self.options.include_ant_hill_in_checks.value == IncludeAntHillInChecksToggle.option_true:
            create_connection("Enchanted Earth", "Ant Hill")

        # # hall of heroes
        create_connection("Map", "Hall of Heroes")

        create_connection("Dan's Crypt", "Locked Items DC")
        create_connection("Cemetery Hill", "Locked Items CH")
        create_connection("The Hilltop Mausoleum", "Locked Items HM")
        create_connection("Scarecrow Fields", "Locked Items SF")
        create_connection("Hall of Heroes", "Map")

    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)

        chalice_count = 0
        # if self.options.include_ant_hill_in_checks.value == IncludeAntHillInChecksToggle.option_true and self.options.chalice_win_count.value > 19:
        #     chalice_count = -1

        for location in location_table:
            # keep track of chalices collected for logic purposes
            if "Chalice Reward" in location.name and chalice_count <= self.options.chalice_win_count.value:
                chalice_count += 1
            # if ant hill is disabled, make sure that it's skipped correctly.
            if (
                self.options.include_ant_hill_in_checks.value == IncludeAntHillInChecksToggle.option_false
                and "Chalice Reward" in location.name
                and self.options.chalice_win_count.value > 19
                and chalice_count > 19
            ):
                continue
            # if the chalice reward count is higher than implied, then skip
            if chalice_count > self.options.chalice_win_count.value and "Chalice Reward" in location.name:
                continue

            if (
                self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false
                and location.category == MedievilLocationCategory.CHALICE_PICKUP
            ):
                continue
            if self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false and region_name == "Hall of Heroes":
                continue
            if self.options.booksanity.value == BookSanityToggle.option_false and location.category == MedievilLocationCategory.BOOK:
                continue
            if self.options.gargoylesanity.value == GargoyleSanityToggle.option_false and location.category == MedievilLocationCategory.GARGOYLE:
                continue

            if location.name == "Equipment: Good Lightning - ZL":
                good_lightning = MedievilItem("Equipment: Good Lightning", ItemClassification.useful, 9901045, self.player)
                new_location = MedievilLocation(
                    self.player,
                    "Equipment: Good Lightning - ZL",
                    MedievilLocationCategory.WEAPON,
                    "Equipment: Good Lightning",
                    self.location_name_to_id["Equipment: Good Lightning - ZL"],
                    new_region,
                )
                new_location.place_locked_item(good_lightning)

            elif self.options.runesanity.value == RuneSanityToggle.option_true and location.name == "Star Rune: Dan's Crypt":
                first_star_rune = MedievilItem("Star Rune: Dan's Crypt", ItemClassification.progression, 9901146, self.player)
                new_location = MedievilLocation(
                    self.player,
                    "Star Rune: Dan's Crypt",
                    MedievilLocationCategory.RUNE,
                    "Star Rune: Dan's Crypt",
                    self.location_name_to_id["Star Rune: Dan's Crypt"],
                    new_region,
                )
                new_location.place_locked_item(first_star_rune)

            elif location.category in self.enabled_location_categories:
                new_location = MedievilLocation(
                    self.player, location.name, location.category, location.default_item, self.location_name_to_id[location.name], new_region
                )
            else:
                event_item = self.create_item(location.default_item)
                new_location = MedievilLocation(self.player, location.name, location.category, location.default_item, None, new_region)
                event_item.code = None
            # print(f"{self.location_name_to_id[location.name]}: {location.name}")
            new_region.locations.append(new_location)

        self.multiworld.regions.append(new_region)
        return new_region

    def create_items(self):
        randomized_location_count = 0
        for location in self.multiworld.get_locations(self.player):
            if not location.locked and location.address is not None:
                randomized_location_count += 1

        print(f"Requesting itempool size for randomized locations: {randomized_location_count}")

        # Call BuildItemPool to get a list of item NAMES (strings)
        item_names_to_add = BuildItemPool(randomized_location_count, self.options)

        generated_items: List[Item] = []
        for item_name in item_names_to_add:
            new_item = self.create_item(item_name)
            generated_items.append(new_item)

        print(f"Created item pool size: {len(generated_items)}")

        # Add the generated MedievilItem objects to the multiworld's item pool
        self.multiworld.itempool.extend(generated_items)

        # print(self.options.runesanity.value)

        # print("Final Item pool: ")
        # for item in self.multiworld.itempool:
        #     print(item.name)

    def create_item(self, name: str) -> Item:
        item_data = item_dictionary.get(name)

        if not item_data:
            # Fallback for unknown items. This indicates a data inconsistency.
            print(f"Warning: Attempted to create unknown item: {name}. Falling back to filler.")
            return MedievilItem(name, ItemClassification.filler, None, self.player)

        # Determine the Archipelago ItemClassification based on MedievilItemData.
        item_classification: ItemClassification

        if item_data.progression or item_data.category == MedievilItemCategory.PROGRESSION or item_data.category == MedievilItemCategory.LEVEL_END:
            item_classification = ItemClassification.progression
        elif (
            item_data.category == MedievilItemCategory.FUN
            or item_data.category == MedievilItemCategory.WEAPON
            or item_data.category == MedievilItemCategory.CHALICE
        ):
            item_classification = ItemClassification.useful
        else:  # Default for FILLER or other categories not explicitly useful/progression
            item_classification = ItemClassification.filler

        return MedievilItem(name, item_classification, MedievilItem.get_name_to_id()[name], self.player)

    def get_filler_item_name(self) -> str:
        return "Gold (50)"  # this clearly needs looked into

    def set_rules(self) -> None:
        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                set_rule(location, lambda state: True)

        max_chalice_count = self.options.chalice_win_count.value

        if self.options.include_ant_hill_in_checks.value == IncludeAntHillInChecksToggle.option_false and max_chalice_count > 19:
            max_chalice_count = 19

        if self.options.goal.value == GoalOptions.DEFEAT_ZAROK:
            self.multiworld.completion_condition[self.player] = lambda state: defeat_zarok_victory(self, max_chalice_count, state)
        elif self.options.goal.value == GoalOptions.CHALICE:
            self.multiworld.completion_condition[self.player] = lambda state: get_chalices_victory(self, max_chalice_count, state)
        elif self.options.goal.value == GoalOptions.BOTH:
            self.multiworld.completion_condition[self.player] = lambda state: defeat_zarok_and_get_chalices_victory(self, max_chalice_count, state)
        # Map rules

        for location in self.multiworld.get_locations(self.player):
            # Check if the location is within "Dan's Crypt" or "Locked Items DC"
            if location.parent_region.name in ["Dan's Crypt", "Locked Items DC"]:
                add_item_rule(location, lambda item: item.name != "Equipment: Hammer")
                add_item_rule(location, lambda item: item.name != "Equipment: Club")
                add_item_rule(location, lambda item: item.name != "Skill: Daring Dash")

            if location.parent_region.name in ["Locked Items DC", "Locked Items CH", "Locked Items HM", "Locked Items SF"]:
                add_item_rule(location, lambda item: item.name != "Key Item: Skull Key")

            if "Chalice Reward" in location.name:
                add_item_rule(location, lambda item: "Key Item" not in item.name)

        # ant hill checks
        if self.options.include_ant_hill_in_checks.value == IncludeAntHillInChecksToggle.option_true:
            if self.options.progression_option.value == ProgressionOptions.OPEN:
                set_ant_hill_rules_open(self)
            else:
                set_ant_hill_rules_vanilla(self)

        if (
            self.options.include_ant_hill_in_checks.value == IncludeAntHillInChecksToggle.option_true
            and self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_true
        ):
            set_ant_hill_chalice(self)

        # level progression
        if self.options.progression_option.value == ProgressionOptions.VANILLA:
            set_vanilla_level_progression(self)
        elif self.options.progression_option.value == ProgressionOptions.OPEN:
            set_open_level_progression(self)

        # hall of heroes
        if self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_true:
            set_hall_of_heroes_progression(self, max_chalice_count)

        # runesanity options

        if self.options.runesanity.value == RuneSanityToggle.option_true:
            if self.options.progression_option.value == ProgressionOptions.VANILLA:
                set_vanilla_runesanity_rules(self)
            elif self.options.progression_option.value == ProgressionOptions.OPEN:
                set_open_runesanity_rules(self)

        # locked chalice items
        set_locked_items_locations(self)

        # Get a birds eye view of everything

        # from Utils import visualize_regions
        # state = self.multiworld.get_all_state(False)
        # state.update_reachable_regions(self.player)
        # visualize_regions(self.get_region("Menu"), "medievil_layout.puml", show_entrance_names=True,
        #                 regions_to_highlight=state.reachable_regions[self.player])

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        name_to_medievil_code = {item.name: item.m_code for item in item_dictionary.values()}
        # Create the mandatory lists to generate the player's output file
        items_id = []
        items_address = []
        locations_id = []
        locations_address = []
        locations_target = []
        for location in self.multiworld.get_filled_locations():
            if location.item.player == self.player:
                # we are the receiver of the item
                items_id.append(location.item.code)
                items_address.append(name_to_medievil_code[location.item.name])

            if location.player == self.player:
                # we are the sender of the location check
                locations_address.append(item_dictionary[location_dictionary[location.name].default_item].m_code)
                locations_id.append(location.address)
                if location.item.player == self.player:
                    locations_target.append(name_to_medievil_code[location.item.name])
                else:
                    locations_target.append(0)

        slot_data = {
            "options": {
                "guaranteed_items": self.options.guaranteed_items.value,
                "goal": self.options.goal.value,
                "progression_option": self.options.progression_option.value,
                "include_ant_hill_in_checks": self.options.include_ant_hill_in_checks.value,
                "include_chalices_in_checks": self.options.include_chalices_in_checks.value,
                "chalice_win_count": self.options.chalice_win_count.value,
                "traps": self.options.traps.value,
                "ammo": self.options.ammo.value,
                "deathlink": self.options.deathlink.value,
                "break_ammo_limit": self.options.break_ammo_limit.value,
                "break_percentage_limit": self.options.break_percentage_limit.value,
                "cheat_menu": self.options.cheat_menu.value,
                "runesanity": self.options.runesanity.value,
                "gargoylesanity": self.options.gargoylesanity.value,
                "booksanity": self.options.booksanity.value,
            },
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.multiworld.player_name[self.player],  # to connect to server
            "base_id": self.base_id,  # to merge location and items lists
            "locationsId": locations_id,
            "locationsAddress": locations_address,
            "locationsTarget": locations_target,
            "itemsId": items_id,
            "itemsAddress": items_address,
        }

        return slot_data
