from .Rules import has_number_of_chalices

def defeat_zarok_victory(self, max_chalices, state):
    return state.can_reach_location("Cleared: Zaroks Lair", self.player)

def get_chalices_victory(self, max_chalices, state):
    return has_number_of_chalices(self, max_chalices, state)

def defeat_zarok_and_get_chalices_victory(self, max_chalice_count, state):
    return state.can_reach_location("Cleared: Zaroks Lair", self.player) and has_number_of_chalices(self, max_chalice_count, state)