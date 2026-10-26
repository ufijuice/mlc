"""
Inference rules for the rigid structural scaffolding of the world model.
Provides deterministic, verified deduction over relational beliefs.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Dict
from mlc.types import Belief, Modality
from mlc.modal_map import compose_modalities


class InferenceRule(ABC):
    """Abstract base class for discrete inference rules."""
    name: str
    description: str

    @abstractmethod
    def apply(self, beliefs: List[Belief]) -> List[Dict]:
        """
        Evaluate the rule over the current set of beliefs.
        Returns a list of candidate inferred beliefs as dicts.
        """
        pass


class TransitiveRule(InferenceRule):
    """
    Transitivity: If (A, P, B) and (B, P, C), infer (A, P, C).
    Confidence compounds: c(A, C) = c(A, B) * c(B, C).
    """
    def __init__(self, predicate: str, inferred_predicate: Optional[str] = None):
        self.predicate = predicate
        self.inferred_predicate = inferred_predicate or predicate
        self.name = f"Transitivity of '{predicate}'"
        self.description = f"If A {predicate} B and B {predicate} C, then A {self.inferred_predicate} C."

    def apply(self, beliefs: List[Belief]) -> List[Dict]:
        candidates = []
        matching = [b for b in beliefs if b.predicate.lower() == self.predicate.lower() and not b.is_conflicting]

        for b1 in matching:
            for b2 in matching:
                # Chain condition: object of b1 matches subject of b2
                if b1.object.lower() == b2.subject.lower() and b1.subject.lower() != b2.object.lower():
                    compounded_confidence = b1.confidence * b2.confidence
                    derived_modality = compose_modalities(b1.modality, b2.modality)

                    candidates.append({
                        "subject": b1.subject,
                        "predicate": self.inferred_predicate,
                        "object": b2.object,
                        "modality": derived_modality,
                        "confidence": compounded_confidence,
                        "justification": self.name,
                        "inferred_from": [b1.id, b2.id],
                        "context": b1.context or b2.context,
                    })
        return candidates


class SymmetricRule(InferenceRule):
    """
    Symmetry: If (A, P, B), infer (B, P, A).
    """
    def __init__(self, predicate: str, inferred_predicate: Optional[str] = None):
        self.predicate = predicate
        self.inferred_predicate = inferred_predicate or predicate
        self.name = f"Symmetry of '{predicate}'"
        self.description = f"If A {predicate} B, then B {self.inferred_predicate} A."

    def apply(self, beliefs: List[Belief]) -> List[Dict]:
        candidates = []
        matching = [b for b in beliefs if b.predicate.lower() == self.predicate.lower() and not b.is_conflicting]

        for b in matching:
            if b.subject.lower() != b.object.lower():
                candidates.append({
                    "subject": b.object,
                    "predicate": self.inferred_predicate,
                    "object": b.subject,
                    "modality": b.modality,
                    "confidence": b.confidence,
                    "justification": self.name,
                    "inferred_from": [b.id],
                    "context": b.context,
                })
        return candidates


class SubsumptionRule(InferenceRule):
    """
    Subsumption: If (A, specific_P, B), infer (A, general_P, B).
    E.g., (A, works_for, B) -> (A, employed_by, B).
    """
    def __init__(self, specific_predicate: str, general_predicate: str, confidence_discount: float = 1.0):
        self.specific_predicate = specific_predicate
        self.general_predicate = general_predicate
        self.confidence_discount = confidence_discount
        self.name = f"Subsumption: '{specific_predicate}' -> '{general_predicate}'"
        self.description = f"If A {specific_predicate} B, then A {general_predicate} B."

    def apply(self, beliefs: List[Belief]) -> List[Dict]:
        candidates = []
        matching = [b for b in beliefs if b.predicate.lower() == self.specific_predicate.lower() and not b.is_conflicting]

        for b in matching:
            candidates.append({
                "subject": b.subject,
                "predicate": self.general_predicate,
                "object": b.object,
                "modality": b.modality,
                "confidence": b.confidence * self.confidence_discount,
                "justification": self.name,
                "inferred_from": [b.id],
                "context": b.context,
            })
        return candidates


class InverseRule(InferenceRule):
    """
    Inverse Relation: If (A, P, B), infer (B, inv_P, A).
    E.g., (A, teaches, B) -> (B, student_of, A), or (A, parent_of, B) -> (B, child_of, A).
    """
    def __init__(self, predicate: str, inverse_predicate: str):
        self.predicate = predicate
        self.inverse_predicate = inverse_predicate
        self.name = f"Inverse: '{predicate}' <-> '{inverse_predicate}'"
        self.description = f"If A {predicate} B, then B {inverse_predicate} A."

    def apply(self, beliefs: List[Belief]) -> List[Dict]:
        candidates = []
        matching = [b for b in beliefs if b.predicate.lower() == self.predicate.lower() and not b.is_conflicting]

        for b in matching:
            candidates.append({
                "subject": b.object,
                "predicate": self.inverse_predicate,
                "object": b.subject,
                "modality": b.modality,
                "confidence": b.confidence,
                "justification": self.name,
                "inferred_from": [b.id],
                "context": b.context,
            })
        return candidates


def get_default_rules() -> List[InferenceRule]:
    """Default baseline reasoning scaffolding."""
    return [
        TransitiveRule("ancestor_of"),
        TransitiveRule("part_of"),
        TransitiveRule("subset_of"),
        TransitiveRule("causes"),
        TransitiveRule("located_in"),
        SymmetricRule("married_to"),
        SymmetricRule("adjacent_to"),
        SymmetricRule("equals"),
        SymmetricRule("sibling_of"),
        SubsumptionRule("works_for", "employed_by"),
        SubsumptionRule("founded", "associated_with"),
        InverseRule("teaches", "learned_from"),
        InverseRule("parent_of", "child_of"),
        InverseRule("contains", "inside_of"),
    ]
