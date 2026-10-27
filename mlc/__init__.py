"""
MLC: Modal Logic Converter & Epistemic Reasoner
Rigid structural scaffolding for learning, experimenting, and building
internal world models under observer uncertainty.
"""

from mlc.types import Belief, Modality, RelationCategory
from mlc.rules import (
    InferenceRule,
    TransitiveRule,
    SymmetricRule,
    SubsumptionRule,
    InverseRule,
    get_default_rules,
)
from mlc.converter import ModalConverter
from mlc.engine import WorldModel
from mlc.simulation import SocietySimulation, Citizen, Archetype

__version__ = "0.2.0"
__all__ = [
    "WorldModel",
    "Belief",
    "Modality",
    "RelationCategory",
    "ModalConverter",
    "InferenceRule",
    "TransitiveRule",
    "SymmetricRule",
    "SubsumptionRule",
    "InverseRule",
    "get_default_rules",
    "SocietySimulation",
    "Citizen",
    "Archetype",
]
