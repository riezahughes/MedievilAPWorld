"""Regression tests for base-game key-item dependencies, applied in every mode."""

from . import MedievilTestBase
from ..Options import ProgressionOptions


class KeyItemDependencyTest(MedievilTestBase):
    options = {
        "progression_option": ProgressionOptions.OPEN,
    }

    def test_shadow_artefact_requires_crucifix(self) -> None:
        self.assertFalse(self.can_reach_location("Key Item: Shadow Artefact - SV"))
        self.collect_by_name("Key Item: Crucifix")
        self.assertTrue(self.can_reach_location("Key Item: Shadow Artefact - SV"))
