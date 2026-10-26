"""
The WorldModel engine: Epistemic scaffolding for autonomous cognitive agents.
Maintains beliefs, updates under observer uncertainty, detects conflicts,
and applies rigid deductive inference rules with proof provenance.
"""

from typing import List, Dict, Optional, Any, Set, Tuple
from mlc.types import Belief, Modality
from mlc.rules import InferenceRule, get_default_rules
from mlc.converter import ModalConverter


class WorldModel:
    """
    An agent's internal world model.
    Combines:
      - Discrete relational beliefs
      - Modal logic qualification (necessity, possibility, etc.)
      - Observer uncertainty (probabilistic credences, e.g. 95%)
      - Rigid deductive inference rules (transitivity, symmetry, subsumption)
      - Explicit proof traces and conflict detection
    """

    def __init__(self, rules: Optional[List[InferenceRule]] = None):
        self.beliefs: Dict[int, Belief] = {}
        self._next_id: int = 1
        self.rules: List[InferenceRule] = rules if rules is not None else get_default_rules()
        self.converter = ModalConverter()

    def observe(
        self,
        subject: str,
        predicate: str,
        object: str,
        modality: Modality = Modality.FACTUAL,
        confidence: float = 0.95,
        context: Optional[str] = None,
        justification: Optional[str] = None,
        inferred_from: Optional[List[int]] = None,
    ) -> Belief:
        """
        Record a direct observation or hypothesis into the world model.
        Handles conflict detection and confidence updates.
        """
        inferred_from = inferred_from or []

        # Check for exact duplicate
        for b in self.beliefs.values():
            if (
                b.subject.lower() == subject.lower() and
                b.predicate.lower() == predicate.lower() and
                b.object.lower() == object.lower()
            ):
                # Update confidence if higher
                if confidence > b.confidence:
                    b.confidence = confidence
                    b.modality = modality
                return b

        # Check for contradictory / conflicting beliefs (e.g. same S and P, different O)
        is_conflict = False
        for b in self.beliefs.values():
            if (
                b.subject.lower() == subject.lower() and
                b.predicate.lower() == predicate.lower() and
                b.object.lower() != object.lower()
            ):
                # Exclusive conflict flag
                b.is_conflicting = True
                is_conflict = True

        belief = Belief(
            id=self._next_id,
            subject=subject,
            predicate=predicate,
            object=object,
            modality=modality,
            confidence=confidence,
            justification=justification or ("Direct Observation" if not inferred_from else "Inferred"),
            inferred_from=inferred_from,
            is_conflicting=is_conflict,
            context=context,
        )
        self.beliefs[self._next_id] = belief
        self._next_id += 1
        return belief

    def observe_text(self, sentence: str) -> Optional[Belief]:
        """Convert a natural statement into a modal belief via converter heuristics."""
        parsed = self.converter.parse_statement(sentence)
        if parsed:
            return self.observe(
                subject=parsed["subject"],
                predicate=parsed["predicate"],
                object=parsed["object"],
                modality=parsed["modality"],
                confidence=parsed["confidence"],
                context=parsed["context"],
            )
        return None

    def add_rule(self, rule: InferenceRule) -> None:
        """Extend the rigid structural scaffolding with a new inference rule."""
        self.rules.append(rule)

    def infer(self, max_iterations: int = 5) -> List[Belief]:
        """
        Run forward-chaining inference loop until fixpoint or max_iterations.
        Deduces new beliefs while tracking dependencies and compounding confidence.
        """
        new_inferred_total: List[Belief] = []

        for iteration in range(max_iterations):
            current_beliefs = list(self.beliefs.values())
            iteration_added = 0

            for rule in self.rules:
                candidates = rule.apply(current_beliefs)
                for cand in candidates:
                    # Check if candidate already exists
                    existing = self.find(cand["subject"], cand["predicate"], cand["object"])
                    if existing is None:
                        new_b = self.observe(
                            subject=cand["subject"],
                            predicate=cand["predicate"],
                            object=cand["object"],
                            modality=cand["modality"],
                            confidence=cand["confidence"],
                            justification=cand["justification"],
                            inferred_from=cand["inferred_from"],
                            context=cand.get("context"),
                        )
                        new_inferred_total.append(new_b)
                        iteration_added += 1

            if iteration_added == 0:
                break  # Reached logical fixpoint

        return new_inferred_total

    def find(self, subject: str, predicate: str, object: str) -> Optional[Belief]:
        """Find a belief matching the exact subject, predicate, object."""
        s, p, o = subject.lower(), predicate.lower(), object.lower()
        for b in self.beliefs.values():
            if b.subject.lower() == s and b.predicate.lower() == p and b.object.lower() == o:
                return b
        return None

    def query(
        self,
        subject: Optional[str] = None,
        predicate: Optional[str] = None,
        object: Optional[str] = None,
        min_confidence: float = 0.0,
        exclude_conflicts: bool = False,
    ) -> List[Belief]:
        """Query beliefs matching pattern with optional confidence filter."""
        results = []
        for b in self.beliefs.values():
            if exclude_conflicts and b.is_conflicting:
                continue
            if b.confidence < min_confidence:
                continue
            if subject and b.subject.lower() != subject.lower():
                continue
            if predicate and b.predicate.lower() != predicate.lower():
                continue
            if object and b.object.lower() != object.lower():
                continue
            results.append(b)
        return results

    def get_proof_trace(self, belief_id: int, depth: int = 0) -> Dict[str, Any]:
        """
        Recursively construct an explanation / proof trace for a belief.
        Mirrors the Curry-Howard proof term: shows why a belief is justified.
        """
        belief = self.beliefs.get(belief_id)
        if not belief:
            return {"error": f"Belief #{belief_id} not found."}

        trace = {
            "id": belief.id,
            "statement": f"({belief.subject}, {belief.predicate}, {belief.object})",
            "modality": belief.modality.value if isinstance(belief.modality, Modality) else str(belief.modality),
            "confidence": f"{belief.confidence:.1%}",
            "justification": belief.justification,
            "premises": [self.get_proof_trace(pid, depth + 1) for pid in belief.inferred_from],
        }
        return trace

    def print_proof_trace(self, belief_id: int, indent: int = 0) -> None:
        """Pretty-print the proof derivation tree to stdout."""
        belief = self.beliefs.get(belief_id)
        if not belief:
            print(f"Belief #{belief_id} not found.")
            return

        prefix = "  " * indent
        symbol = "└── " if indent > 0 else ""
        mod = f"[{belief.modality.value}]"
        conf = f"({belief.confidence:.1%})"
        just = f"- by {belief.justification}" if belief.justification else ""
        print(f"{prefix}{symbol}Belief #{belief.id}: ({belief.subject}, {belief.predicate}, {belief.object}) {mod} {conf} {just}")

        for pid in belief.inferred_from:
            self.print_proof_trace(pid, indent + 1)

    def summary(self) -> Dict[str, Any]:
        """Generate high-level health and size metrics for the internal world model."""
        return {
            "total_beliefs": len(self.beliefs),
            "direct_observations": len([b for b in self.beliefs.values() if not b.inferred_from]),
            "inferred_beliefs": len([b for b in self.beliefs.values() if b.inferred_from]),
            "conflicts": len([b for b in self.beliefs.values() if b.is_conflicting]),
            "average_confidence": round(sum(b.confidence for b in self.beliefs.values()) / max(1, len(self.beliefs)), 3),
        }
