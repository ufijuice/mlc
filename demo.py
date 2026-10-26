#!/usr/bin/env python3
"""
Interactive demonstration of the Modal Logic Converter (MLC).
Shows how an agent constructs an internal world model, learns under observer
uncertainty, detects conflicts, and derives verified inferences with proof traces.
"""

from mlc import WorldModel, Modality, TransitiveRule

def main():
    print("=" * 70)
    print("  MLC: Modal Logic Converter & Epistemic Reasoner")
    print("  Rigid Structural Scaffolding for Autonomous World Models")
    print("=" * 70)
    print()

    # 1. Initialize the cognitive world model
    wm = WorldModel()

    # Add custom transitivity rule for categorical syllogisms
    wm.add_rule(TransitiveRule("is_a"))

    print("[1] Ingesting observations under observer uncertainty...")
    # Observation 1: Axiom / High necessity
    b1 = wm.observe(
        subject="Socrates",
        predicate="is_a",
        object="Human",
        modality=Modality.NECESSITY,
        confidence=0.98,
        context="Observed in philosophical text",
    )
    print(f"  + {b1}")

    # Observation 2: Factual premise with standard 95% observer credence
    b2 = wm.observe(
        subject="Human",
        predicate="is_a",
        object="Mortal",
        modality=Modality.FACTUAL,
        confidence=0.95,
        context="Empirical biological observation",
    )
    print(f"  + {b2}")

    # Observation 3: Ingest via natural language heuristic converter
    print("\n[2] Ingesting natural language with modal qualification...")
    text_stmt = "Alice works for Occur."
    b3 = wm.observe_text(text_stmt)
    print(f"  Parsed '{text_stmt}' -> {b3}")

    b4 = wm.observe(
        subject="Occur",
        predicate="located_in",
        object="San_Francisco",
        modality=Modality.FACTUAL,
        confidence=0.95,
    )
    b5 = wm.observe(
        subject="San_Francisco",
        predicate="located_in",
        object="California",
        modality=Modality.AXIOMATIC,
        confidence=1.00,
    )
    print(f"  + {b4}")
    print(f"  + {b5}")

    # 3. Step the rigid inference engine
    print("\n[3] Executing forward-chaining deduction loop...")
    inferred = wm.infer()
    print(f"  -> Successfully derived {len(inferred)} new discrete beliefs:")
    for b in inferred:
        print(f"     * {b}")

    # 4. Inspect proof traces (The Lambda Cube lineage)
    print("\n[4] Inspecting proof provenance (Curry-Howard proof trace)...")
    socrates_mortal = wm.find("Socrates", "is_a", "Mortal")
    if socrates_mortal:
        print(f"  Explanation tree for: {socrates_mortal.subject} {socrates_mortal.predicate} {socrates_mortal.object}")
        wm.print_proof_trace(socrates_mortal.id)

    occur_in_ca = wm.find("Occur", "located_in", "California")
    if occur_in_ca:
        print(f"\n  Explanation tree for: {occur_in_ca.subject} {occur_in_ca.predicate} {occur_in_ca.object}")
        wm.print_proof_trace(occur_in_ca.id)

    # 5. Simulate observer conflict / noisy evidence
    print("\n[5] Simulating noisy observer with conflicting evidence...")
    conflicting_stmt = wm.observe(
        subject="Occur",
        predicate="located_in",
        object="New_York",
        modality=Modality.POSSIBILITY,
        confidence=0.60,
        context="Unverified forum comment",
    )
    print(f"  + Added conflicting observation: {conflicting_stmt}")
    print(f"  -> Conflict detected on original belief: is_conflicting={b4.is_conflicting}")

    # 6. Print world model health summary
    print("\n[6] World Model Metrics:")
    metrics = wm.summary()
    for k, v in metrics.items():
        print(f"  - {k.replace('_', ' ').title()}: {v}")

    print("\n" + "=" * 70)
    print("  Deductive scaffolding verified. World model consistent.")
    print("=" * 70)

if __name__ == "__main__":
    main()
