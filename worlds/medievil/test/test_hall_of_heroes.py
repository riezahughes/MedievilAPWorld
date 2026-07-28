from . import MedievilTestBase
from ..Options import ProgressionOptions


class HallOfHeroesOpenTest(MedievilTestBase):
    options = {
        "progression_option": ProgressionOptions.OPEN,
    }

    def _reward_reachable(self, count: int) -> bool:
        return self.can_reach_location(f"Chalice Reward {count}")

    def test_nine_chalices_are_reachable_with_no_items_in_open_mode(self) -> None:
        """
        In open mode, with default options (ant hill + chalices both enabled), 9 of the
        20 tracked chalice pickups sit in regions with no access rule at all: The
        Graveyard, Enchanted Earth, The Lake, The Crystal Caves, Inside the Asylum,
        Pumpkin Gorge, Ghost Ship, The Entrance Hall, and The Time Device.
        """
        self.assertTrue(self.can_reach_entrance("Map -> Hall of Heroes"))
        for i in range(1, 10):
            with self.subTest(reward=i):
                self.assertTrue(self._reward_reachable(i))
        self.assertFalse(self._reward_reachable(10))

    def test_reward_locations_unlock_progressively_as_chalice_count_rises(self) -> None:
        self.collect_by_name("Key Item: Witches Talisman")  # Pumpkin Serpent + Ant Hill chalices: 9 -> 11
        self.assertTrue(self._reward_reachable(11))
        self.assertFalse(self._reward_reachable(12))

        self.collect_by_name("Equipment: Club")  # Cemetery Hill: 11 -> 12
        self.assertTrue(self._reward_reachable(12))
        self.assertFalse(self._reward_reachable(13))

        self.collect_by_name("Key Item: Sheet Music")  # Hilltop Mausoleum: 12 -> 13
        self.assertTrue(self._reward_reachable(13))
        self.assertFalse(self._reward_reachable(14))

        self.collect_by_name("Key Item: Skull Key")  # Return to the Graveyard: 13 -> 14
        self.assertTrue(self._reward_reachable(14))
        self.assertFalse(self._reward_reachable(15))

        self.collect_by_name("Key Item: Harvester Parts")  # Scarecrow Fields: 14 -> 15
        self.assertTrue(self._reward_reachable(15))
        self.assertFalse(self._reward_reachable(16))

        self.collect_by_name("Key Item: Crucifix")  # Sleeping Village (Asylum needs 2 more): 15 -> 16
        self.assertTrue(self._reward_reachable(16))
        self.assertFalse(self._reward_reachable(17))

        self.collect_by_name("Equipment: Dragon Armour")  # The Gallows Gauntlet: 16 -> 17
        self.assertTrue(self._reward_reachable(17))
        self.assertFalse(self._reward_reachable(18))

        self.collect_by_name(["Key Item: Crucifix Cast", "Key Item: Landlords Bust"])  # Asylum Grounds trio complete: 17 -> 18
        self.assertTrue(self._reward_reachable(18))
        self.assertFalse(self._reward_reachable(19))

        self.collect_by_name(["Key Item: Shadow Talisman", "Key Item: Shadow Artefact"])
        self.collect_by_name([f"Key Item: Soul Helmet {i}" for i in range(1, 9)])  # Pools of the Ancient Dead: 18 -> 19
        self.assertTrue(self._reward_reachable(19))
        self.assertFalse(self._reward_reachable(20))

        self.collect_by_name(["Key Item: King Peregrine's Crown", "Skill: Daring Dash"])  # The Haunted Ruins: 19 -> 20
        self.assertTrue(self._reward_reachable(20))


class HallOfHeroesChalicesDisabledTest(MedievilTestBase):
    options = {
        "include_chalices_in_checks": 0,
    }

    def test_hall_of_heroes_has_no_locations_and_is_trivially_reachable(self) -> None:
        region = self.world.get_region("Hall of Heroes")
        self.assertEqual(len(region.locations), 0)
        self.assertTrue(self.can_reach_entrance("Map -> Hall of Heroes"))
