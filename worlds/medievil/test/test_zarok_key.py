"""
Tests for the Zarok's Lair level key (KeySanity): "Zaroks Lair Unlock" / "False Heroes Hope".
"""

from . import MedievilTestBase
from ..Options import ProgressionOptions, KeysanityOptions

ZAROK_KEYS = {
    KeysanityOptions.LEVEL_NAME: "Zaroks Lair Unlock",
    KeysanityOptions.UNIQUE_NAME: "False Heroes Hope",
}


class ZarokKeyTest(MedievilTestBase):
    options = {"progression_option": ProgressionOptions.OPEN, "keysanity": 1, "keysanity_starting_keys": 19}
    naming = KeysanityOptions.LEVEL_NAME

    def key_name(self) -> str:
        return ZAROK_KEYS[self.naming]

    def test_zarok_key_is_either_a_starting_key_or_in_the_pool(self) -> None:
        in_start = self.key_name() in self.world.starting_keys
        in_pool = len(self.get_items_by_name(self.key_name()))
        self.assertEqual(in_pool, 0 if in_start else 1)

    def test_entrance_needs_the_key(self) -> None:
        has_key = self.key_name() in self.world.starting_keys
        self.assertEqual(self.can_reach_entrance("Map -> Zaroks Lair"), has_key)
        self.collect_by_name(self.key_name())
        self.assertTrue(self.can_reach_entrance("Map -> Zaroks Lair"))


class ZarokKeyUniqueNameTest(ZarokKeyTest):
    options = {
        "progression_option": ProgressionOptions.OPEN,
        "keysanity": 1,
        "keysanity_starting_keys": 19,
        "keysanity_naming": KeysanityOptions.UNIQUE_NAME,
    }
    naming = KeysanityOptions.UNIQUE_NAME


class ZarokKeyOffTest(MedievilTestBase):
    options = {"progression_option": ProgressionOptions.OPEN, "keysanity": 0}

    def test_no_zarok_key_without_keysanity(self) -> None:
        self.assertEqual(self.get_items_by_name(list(ZAROK_KEYS.values())), [])
        self.assertTrue(self.can_reach_entrance("Map -> Zaroks Lair"))
