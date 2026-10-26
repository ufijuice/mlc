"""
Lexical and ontological mappings for modal and relational heuristics.
Translates unstructured observer statements into structured modal categories.
"""

from mlc.types import Modality, RelationCategory

MODAL_LEXICON = {
    # Necessity & Obligation
    "must": Modality.NECESSITY,
    "shall": Modality.OBLIGATION,
    "need": Modality.NECESSITY,
    "needs to": Modality.NECESSITY,
    "have to": Modality.NECESSITY,
    "has to": Modality.NECESSITY,
    "ought to": Modality.NECESSITY,
    "required": Modality.NECESSITY,
    "necessary": Modality.NECESSITY,

    # Recommendation
    "should": Modality.PROBABILITY,
    "advised to": Modality.PROBABILITY,

    # Possibility & Probability
    "can": Modality.POSSIBILITY,
    "could": Modality.POSSIBILITY,
    "might": Modality.POSSIBILITY,
    "may": Modality.POSSIBILITY,
    "able to": Modality.CAPABILITY,
    "capable of": Modality.CAPABILITY,
    "likely": Modality.PROBABILITY,
    "probable": Modality.PROBABILITY,
    "almost surely": Modality.PROBABILITY,
    "possible": Modality.POSSIBILITY,

    # Permission
    "allowed to": Modality.PERMISSION,
    "permitted to": Modality.PERMISSION,
    "free to": Modality.PERMISSION,

    # Hypothetical / Conditional
    "would": Modality.HYPOTHETICAL,
    "if possible": Modality.HYPOTHETICAL,
    "assuming": Modality.HYPOTHETICAL,

    # Future / Determinism
    "will": Modality.FUTURE,
    "going to": Modality.FUTURE,
    "certain to": Modality.FUTURE,
    "destined to": Modality.FUTURE,

    # Deduction
    "must be": Modality.DEDUCTION,
    "appears to be": Modality.DEDUCTION,
    "seems to be": Modality.DEDUCTION,

    # Prohibition / Impossibility
    "cannot": Modality.PROHIBITION,
    "must not": Modality.PROHIBITION,
    "impossible": Modality.PROHIBITION,
    "forbidden to": Modality.PROHIBITION,

    # Axiomatic / Foundational
    "axiom": Modality.AXIOMATIC,
    "postulate": Modality.AXIOMATIC,
    "assume": Modality.AXIOMATIC,
    "given": Modality.AXIOMATIC,
}

RELATION_LEXICON = {
    # Classification / Taxonomy
    "is a": RelationCategory.CLASSIFICATION,
    "is an": RelationCategory.CLASSIFICATION,
    "is an example of": RelationCategory.CLASSIFICATION,
    "is a type of": RelationCategory.CLASSIFICATION,
    "belongs to": RelationCategory.CLASSIFICATION,
    "instance of": RelationCategory.CLASSIFICATION,

    # Part-Whole (Mereology)
    "contains": RelationCategory.PART_WHOLE,
    "includes": RelationCategory.PART_WHOLE,
    "is part of": RelationCategory.PART_WHOLE,
    "is component of": RelationCategory.PART_WHOLE,
    "composed of": RelationCategory.PART_WHOLE,

    # Spatial
    "located in": RelationCategory.SPATIAL,
    "inside": RelationCategory.SPATIAL,
    "adjacent to": RelationCategory.SPATIAL,
    "near": RelationCategory.SPATIAL,

    # Temporal
    "happened before": RelationCategory.TEMPORAL,
    "before": RelationCategory.TEMPORAL,
    "after": RelationCategory.TEMPORAL,
    "occurs after": RelationCategory.TEMPORAL,
    "during": RelationCategory.TEMPORAL,

    # Equivalence
    "equals": RelationCategory.EQUIVALENCE,
    "equivalent to": RelationCategory.EQUIVALENCE,
    "synonymous with": RelationCategory.EQUIVALENCE,
    "identical to": RelationCategory.EQUIVALENCE,

    # Causal
    "causes": RelationCategory.CAUSAL,
    "leads to": RelationCategory.CAUSAL,
    "results in": RelationCategory.CAUSAL,
    "produces": RelationCategory.CAUSAL,

    # Ownership / Attribution
    "owns": RelationCategory.OWNERSHIP,
    "property of": RelationCategory.OWNERSHIP,
    "attribute of": RelationCategory.OWNERSHIP,

    # Functional
    "used for": RelationCategory.FUNCTIONAL,
    "serves as": RelationCategory.FUNCTIONAL,
    "functions as": RelationCategory.FUNCTIONAL,
    "works for": RelationCategory.FUNCTIONAL,
    "teaches": RelationCategory.FUNCTIONAL,

    # Hierarchical
    "subset of": RelationCategory.HIERARCHICAL,
    "superset of": RelationCategory.HIERARCHICAL,
    "greater than": RelationCategory.HIERARCHICAL,
    "less than": RelationCategory.HIERARCHICAL,
}


def compose_modalities(m1: Modality, m2: Modality) -> Modality:
    """
    Modal logic algebra for inference composition.
    E.g., Necessity combined with Necessity yields Necessity.
    Possibility combined with anything yields Possibility (weakest link rule).
    """
    if m1 == Modality.AXIOMATIC and m2 == Modality.AXIOMATIC:
        return Modality.AXIOMATIC
    if m1 == Modality.NECESSITY and m2 == Modality.NECESSITY:
        return Modality.NECESSITY
    if m1 == Modality.POSSIBILITY or m2 == Modality.POSSIBILITY:
        return Modality.POSSIBILITY
    if m1 == Modality.PROBABILITY or m2 == Modality.PROBABILITY:
        return Modality.PROBABILITY
    if m1 == Modality.HYPOTHETICAL or m2 == Modality.HYPOTHETICAL:
        return Modality.HYPOTHETICAL
    return Modality.DEDUCTION
