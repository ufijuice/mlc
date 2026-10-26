from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional, Dict, Any


class Modality(str, Enum):
    """
    Modal categories describing the epistemic and alethic status of a belief.
    """
    NECESSITY = "necessity"          # Must, have to, required
    POSSIBILITY = "possibility"      # May, can, could, might
    PROBABILITY = "probability"      # Likely, probable, almost surely
    OBLIGATION = "obligation"        # Must, shall
    PERMISSION = "permission"        # Allowed to, permitted to
    HYPOTHETICAL = "hypothetical"    # Would, if possible
    FUTURE = "future"                # Will, destined to
    DEDUCTION = "deduction"          # Must be, inferred
    CAPABILITY = "capability"        # Able to, capable of
    PROHIBITION = "prohibition"      # Cannot, forbidden, must not
    AXIOMATIC = "axiomatic"          # Given, postulate, foundational axiom
    FACTUAL = "factual"              # Default factual assertion


class RelationCategory(str, Enum):
    """
    Ontological categorization of binary relations.
    """
    CLASSIFICATION = "classification"  # is a, belongs to
    PART_WHOLE = "part_whole"          # contains, part of
    SPATIAL = "spatial"                # located in, adjacent to
    TEMPORAL = "temporal"              # before, after, during
    EQUIVALENCE = "equivalence"        # equal to, synonymous with
    CAUSAL = "causal"                  # causes, leads to
    OWNERSHIP = "ownership"            # owns, belongs to
    FUNCTIONAL = "functional"          # used for, serves as
    HIERARCHICAL = "hierarchical"      # subset of, greater than
    GENERIC = "generic"


@dataclass
class Belief:
    """
    A single discrete belief in the agent's world model.
    Represents an observer's structured hypothesis (Subject, Predicate, Object)
    qualified by modality, confidence, and derivation provenance.
    """
    id: int
    subject: str
    predicate: str
    object: str
    modality: Modality = Modality.FACTUAL
    confidence: float = 0.95
    justification: Optional[str] = None
    inferred_from: List[int] = field(default_factory=list)
    is_conflicting: bool = False
    context: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def key(self) -> tuple:
        """Normalized key for identity checking."""
        return (self.subject.strip().lower(), self.predicate.strip().lower(), self.object.strip().lower())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "subject": self.subject,
            "predicate": self.predicate,
            "object": self.object,
            "modality": self.modality.value if isinstance(self.modality, Modality) else str(self.modality),
            "confidence": round(self.confidence, 4),
            "justification": self.justification,
            "inferred_from": self.inferred_from,
            "is_conflicting": self.is_conflicting,
            "context": self.context,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self) -> str:
        mod_str = f" [{self.modality.value}]" if self.modality != Modality.FACTUAL else ""
        conf_str = f" ({self.confidence:.0%})"
        inf_str = f" <- {self.inferred_from}" if self.inferred_from else ""
        return f"Belief#{self.id}: ({self.subject}, {self.predicate}, {self.object}){mod_str}{conf_str}{inf_str}"
