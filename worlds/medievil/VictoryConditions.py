from rule_builder.rules import CanReachLocation, Rule

from .Rules import HasNumberOfChalices


def defeat_zarok_victory() -> Rule:
    return CanReachLocation("Cleared: Zaroks Lair")


def get_chalices_victory(max_chalices: int) -> Rule:
    return HasNumberOfChalices(max_chalices)


def defeat_zarok_and_get_chalices_victory(max_chalice_count: int) -> Rule:
    return CanReachLocation("Cleared: Zaroks Lair") & HasNumberOfChalices(max_chalice_count)
