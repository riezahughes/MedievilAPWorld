from worlds.generic.Rules import set_rule
from BaseClasses import CollectionState
from .Options import IncludeAntHillInChecksToggle, IncludeChalicesInChecksToggle



def is_level_cleared(self, location: str, state: CollectionState):
    return state.can_reach_location("Cleared: " + location, self.player)

def has_daring_dash(self, state: CollectionState):
    return state.has("Skill: Daring Dash", self.player)

def is_boss_defeated(self, boss: str, state: CollectionState): # can used later
    return state.has("Boss: " + boss, self.player, 1)

def has_keyitems_required(self, items: list[str], state: CollectionState):
    passed_check = True
    for item in items:
        if(state.has("Key Item: " + item, self.player, 1) is False):
            passed_check = False
    return passed_check

def has_weapon_required(self, weapon: str, state: CollectionState):
    return state.has("Equipment: " + weapon, self.player, 1)

def has_required_souls(self, state: CollectionState):
    return state.has_all([
        "Key Item: Soul Helmet 1",
        "Key Item: Soul Helmet 2",
        "Key Item: Soul Helmet 3",
        "Key Item: Soul Helmet 4",
        "Key Item: Soul Helmet 5",
        "Key Item: Soul Helmet 6",
        "Key Item: Soul Helmet 7",
        "Key Item: Soul Helmet 8"
    ], self.player)
    
def has_required_runes(self, runes, state:CollectionState):
    return state.has_all(runes, self.player)

def has_required_amber(self, state: CollectionState):
    return state.has_all([
        "Key Item: Amber 1",
        "Key Item: Amber 2",
        "Key Item: Amber 3",
        "Key Item: Amber 4",
        "Key Item: Amber 5",
        "Key Item: Amber 6",
        "Key Item: Amber 7"
    ], self.player)

def has_number_of_chalices(self, count, state: CollectionState):
    
    if(self.options.include_chalices_in_checks.value == IncludeChalicesInChecksToggle.option_false):
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
        "Chalice: The Time Device"
    ]
    
    # adds ant hill chalice if it's not excluded
    if self.options.include_ant_hill_in_checks.value == IncludeAntHillInChecksToggle.option_true:
        chalice_list.append("Chalice: Ant Hill")
    
    collected_chalices = 0
    for chalice_location in chalice_list:
        if state.can_reach_location(chalice_location, self.player):
            collected_chalices += 1
    return collected_chalices >= count  

def set_ant_hill_rules_vanilla(self):
     set_rule(self.get_entrance("Enchanted Earth -> Ant Hill"), lambda state: is_level_cleared(self, "Return to the Graveyard" , state) and has_keyitems_required(self, ["Witches Talisman"] , state))
    
def set_ant_hill_rules_open(self):
    set_rule(self.get_entrance("Enchanted Earth -> Ant Hill"), lambda state: has_keyitems_required(self, ["Witches Talisman"] , state))    

def set_ant_hill_chalice(self):
    set_rule(self.get_location("Chalice Reward 20"), lambda state: has_number_of_chalices(self, 20, state))

def set_vanilla_level_progression(self):
    set_rule(self.get_entrance("Map -> The Graveyard"), lambda state: is_level_cleared(self, "Dan's Crypt" , state))
    set_rule(self.get_entrance("Map -> Cemetery Hill"), lambda state: is_level_cleared(self, "The Graveyard" , state) and (has_weapon_required(self, "Club", state) or has_weapon_required(self, "Hammer", state)))
    set_rule(self.get_entrance("Map -> The Hilltop Mausoleum"), lambda state: is_level_cleared(self, "Cemetery Hill" , state))
    set_rule(self.get_entrance("Map -> Return to the Graveyard"), lambda state: is_level_cleared(self, "The Hilltop Mausoleum" , state) and has_keyitems_required(self, ["Skull Key"] , state )) 
    set_rule(self.get_entrance("Map -> Enchanted Earth"), lambda state: is_level_cleared(self, "Return to the Graveyard" , state))
    set_rule(self.get_entrance("Map -> Scarecrow Fields"), lambda state: is_level_cleared(self, "Return to the Graveyard" , state))
    set_rule(self.get_entrance("Map -> The Sleeping Village"), lambda state: is_level_cleared(self, "Scarecrow Fields" , state)) 
    set_rule(self.get_entrance("Map -> Pumpkin Gorge"), lambda state: is_level_cleared(self, "Scarecrow Fields" , state)) 
    set_rule(self.get_entrance("Map -> Asylum Grounds"), lambda state: is_level_cleared(self, "Sleeping Village" , state) and has_keyitems_required(self, ["Crucifix Cast", "Landlords Bust", "Crucifix"] , state))
    set_rule(self.get_entrance("Map -> Inside the Asylum"), lambda state: is_level_cleared(self, "Asylum Grounds" , state)) 
    set_rule(self.get_entrance("Map -> Pumpkin Serpent"), lambda state: is_level_cleared(self, "Pumpkin Gorge" , state) and has_keyitems_required(self, ["Witches Talisman"] , state)) 
    set_rule(self.get_entrance("Map -> Pools of the Ancient Dead"), lambda state: is_level_cleared(self, "Enchanted Earth" , state) and has_keyitems_required(self, ["Shadow Talisman", "Shadow Artefact"] , state) and has_required_souls(self, state)) 
    set_rule(self.get_entrance("Map -> The Lake"), lambda state: is_level_cleared(self, "Pools of the Ancient Dead" , state))
    set_rule(self.get_entrance("Map -> The Crystal Caves"), lambda state: is_level_cleared(self, "The Lake" , state)) 
    set_rule(self.get_entrance("Map -> The Gallows Gauntlet"), lambda state: is_level_cleared(self, "The Crystal Caves" , state) and has_keyitems_required(self, ["Dragon Gem - Pumpkin Serpent", "Dragon Gem - Inside the Asylum"] , state)) 
    set_rule(self.get_entrance("Map -> The Haunted Ruins"), lambda state: is_level_cleared(self, "The Gallows Gauntlet" , state) and has_keyitems_required(self, ["King Peregrine's Crown"] , state) and has_daring_dash(self, state)) 
    set_rule(self.get_entrance("Map -> The Ghost Ship"), lambda state: is_level_cleared(self, "The Haunted Ruins" , state)) 
    set_rule(self.get_entrance("Map -> The Entrance Hall"), lambda state: is_level_cleared(self, "Ghost Ship" , state)) 
    set_rule(self.get_entrance("Map -> The Time Device"), lambda state: is_level_cleared(self, "The Entrance Hall" , state)) 
    set_rule(self.get_entrance("Map -> Zaroks Lair"), lambda state: is_level_cleared(self, "The Time Device" , state))
    
# def set_open_level_progression(self):
    # set_rule(self.get_entrance("Map -> The Graveyard"), lambda state: is_level_cleared(self, "Dan's Crypt" , state))
    # set_rule(self.get_entrance("Map -> Cemetery Hill"), lambda state: (has_weapon_required(self, "Club", state) or has_weapon_required(self, "Hammer", state)))
    # set_rule(self.get_entrance("Map -> The Hilltop Mausoleum"), lambda state: is_level_cleared(self, "Cemetery Hill" , state))
    # set_rule(self.get_entrance("Map -> Return to the Graveyard"), lambda state: has_keyitems_required(self, ["Skull Key"] , state )) 
    # set_rule(self.get_entrance("Map -> Enchanted Earth"), lambda state: is_level_cleared(self, "Return to the Graveyard" , state))
    # set_rule(self.get_entrance("Map -> Scarecrow Fields"), lambda state: is_level_cleared(self, "Return to the Graveyard" , state))
    # set_rule(self.get_entrance("Map -> The Sleeping Village"), lambda state: is_level_cleared(self, "Scarecrow Fields" , state)) 
    # set_rule(self.get_entrance("Map -> Pumpkin Gorge"), lambda state: is_level_cleared(self, "Scarecrow Fields" , state)) 
    # set_rule(self.get_entrance("Map -> Asylum Grounds"), lambda state: has_keyitems_required(self, ["Crucifix Cast", "Landlords Bust", "Crucifix"] , state))
    # set_rule(self.get_entrance("Map -> Inside the Asylum"), lambda state: is_level_cleared(self, "Asylum Grounds" , state)) 
    # set_rule(self.get_entrance("Map -> Pumpkin Serpent"), lambda state: has_keyitems_required(self, ["Witches Talisman"] , state)) 
    # set_rule(self.get_entrance("Map -> Pools of the Ancient Dead"), lambda state: has_keyitems_required(self, ["Shadow Talisman", "Shadow Artefact"] , state) and has_required_souls(self, state)) 
    # set_rule(self.get_entrance("Map -> The Lake"), lambda state: is_level_cleared(self, "Pools of the Ancient Dead" , state))
    # set_rule(self.get_entrance("Map -> The Crystal Caves"), lambda state: is_level_cleared(self, "The Lake" , state)) 
    # set_rule(self.get_entrance("Map -> The Gallows Gauntlet"), lambda state: has_keyitems_required(self, ["Dragon Gem - Pumpkin Serpent", "Dragon Gem - Inside the Asylum"] , state)) 
    # set_rule(self.get_entrance("Map -> The Haunted Ruins"), lambda state: has_keyitems_required(self, ["King Peregrine's Crown"] , state) and has_daring_dash(self, state)) 
    # set_rule(self.get_entrance("Map -> The Ghost Ship"), lambda state: is_level_cleared(self, "The Haunted Ruins" , state)) 
    # set_rule(self.get_entrance("Map -> The Entrance Hall"), lambda state: is_level_cleared(self, "Ghost Ship" , state)) 
    # set_rule(self.get_entrance("Map -> The Time Device"), lambda state: is_level_cleared(self, "The Entrance Hall" , state)) 
    # set_rule(self.get_entrance("Map -> Zaroks Lair"), lambda state: is_level_cleared(self, "The Time Device" , state))
    
        
def set_hall_of_heroes_progression(self):
    # hall of heroes rules
    
    set_rule(self.get_entrance("Map -> Hall of Heroes"), lambda state: has_number_of_chalices(self, 1, state))
    
    # Canny Tim
    set_rule(self.get_location("Chalice Reward 1"), lambda state: has_number_of_chalices(self, 1, state))
    set_rule(self.get_location("Chalice Reward 2"), lambda state: has_number_of_chalices(self, 2, state))

    # Stanyer Iron Hewer
    set_rule(self.get_location("Chalice Reward 3"), lambda state: has_number_of_chalices(self, 3, state))
    set_rule(self.get_location("Chalice Reward 4"), lambda state: has_number_of_chalices(self, 4, state))

    # Woden the Mighty
    set_rule(self.get_location("Chalice Reward 5"), lambda state: has_number_of_chalices(self, 5, state))
    set_rule(self.get_location("Chalice Reward 6"), lambda state: has_number_of_chalices(self, 6, state))

    # Imanzi Shongama
    set_rule(self.get_location("Chalice Reward 7"), lambda state: has_number_of_chalices(self, 7, state))

    # Ravenhooves the Archer
    set_rule(self.get_location("Chalice Reward 8"), lambda state: has_number_of_chalices(self, 8, state))

    # Bloodmonath
    set_rule(self.get_location("Chalice Reward 9"), lambda state: has_number_of_chalices(self, 9, state))

    # Ravenhooves the Archer
    set_rule(self.get_location("Chalice Reward 10"), lambda state: has_number_of_chalices(self, 10, state))

    # Karl Sturngard
    set_rule(self.get_location("Chalice Reward 11"), lambda state: has_number_of_chalices(self, 11, state))

    # Bloodmonath
    set_rule(self.get_location("Chalice Reward 12"), lambda state: has_number_of_chalices(self, 12, state))

    # Dirk Steadfast
    set_rule(self.get_location("Chalice Reward 13"), lambda state: has_number_of_chalices(self, 13, state))

    # Ravenhooves the Archer
    set_rule(self.get_location("Chalice Reward 14"), lambda state: has_number_of_chalices(self, 14, state))

    # Megwynne Stormbinder
    set_rule(self.get_location("Chalice Reward 15"), lambda state: has_number_of_chalices(self, 15, state))

    # Ravenhooves the Archer
    set_rule(self.get_location("Chalice Reward 16"), lambda state: has_number_of_chalices(self, 16, state))

    # Imanzi Shongama
    set_rule(self.get_location("Chalice Reward 17"), lambda state: has_number_of_chalices(self, 17, state))

    # Karl Sturngard
    set_rule(self.get_location("Chalice Reward 18"), lambda state: has_number_of_chalices(self, 18, state))

    # Dirk Steadfast
    set_rule(self.get_location("Chalice Reward 19"), lambda state: has_number_of_chalices(self, 19, state))    

def set_locked_items_locations(self):
    set_rule(self.get_entrance("Dan's Crypt -> Locked Items DC"), lambda state: has_weapon_required(self, "Club", state) or has_weapon_required(self, "Hammer", state) or has_daring_dash(self, state))
    set_rule(self.get_entrance("Cemetery Hill -> Locked Items CH"), lambda state: has_weapon_required(self, "Club", state) or has_weapon_required(self, "Hammer", state))
    set_rule(self.get_entrance("The Hilltop Mausoleum -> Locked Items HM"), lambda state: has_keyitems_required(self, ["Sheet Music"], state))
    set_rule(self.get_entrance("Scarecrow Fields -> Locked Items SF"), lambda state: has_keyitems_required(self, ["Harvester Parts"], state))            