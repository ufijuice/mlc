# MLC: Modal Logic Converter & Epistemic World Model

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

> *"A clear mind that has some rigid structure for learning and experimenting, therefore building the internal world model or behavioring systems."*

**MLC** (Modal Logic Converter / Modal Logic Core) is a lightweight, neuro-symbolic cognitive engine designed to give autonomous agents a **rigid structural scaffolding** for learning and reasoning about reality.

---

## The Philosophy: Bridging Lean and the Real World

Modern AI faces two extremes:
1. **Unconstrained LLMs**: Fluid and associative, but prone to hallucination, lacking internal world models, and incapable of certifying *why* a conclusion follows from premises.
2. **Interactive Theorem Provers (like Lean)**: Perfectly sound, but operate with rigid 100% binary truth ($1$ or $0$). They cannot handle noisy observations, empirical contradictions, or the inherent uncertainty of an observer.

In reality, **an intelligent agent is an observer operating under uncertainty.** When an agent reads text or observes the physical world:
* Facts have **credences / confidence scores** (e.g., $95\%$ statistical confidence).
* Facts are qualified by **modal attitudes** (*necessity*, *possibility*, *obligation*, *contingency*).
* Conflicting observations happen and must be tracked without crashing the system via the logical principle of explosion (*ex falso quodlibet*).
* Inferences must retain an unbroken **proof trace** (the Lambda Cube / Curry-Howard lineage: tracking *which* premises and rules justified the belief).

**MLC provides this middle ground:** a rigid deductive scaffolding (transitivity, symmetry, subsumption, modal composition) acting upon probabilistic, modal-qualified empirical observations.

---

## Architecture & Epistemic Pipeline

```text
  [ Raw Text / Sensory Data ]
               │
               ▼
   ┌───────────────────────┐
   │ Modal Logic Converter │  <-- Extracts (Subject, Predicate, Object)
   │  & Lexical Heuristics │  <-- Tags Modality (Necessity, Possibility, etc.)
   └───────────┬───────────┘
               │
               ▼
   ┌───────────────────────┐
   │  Internal World Model │  <-- Evaluates Observer Confidence (e.g., 95%)
   │  (Belief Repository)  │  <-- Detects & Flags Contradictions
   └───────────┬───────────┘
               │
               ▼
   ┌───────────────────────┐
   │ Rigid Inference Rules │  <-- Forward Chaining: Transitivity, Symmetry, Subsumption
   │ (Structural Invariants)│  <-- Compounds Confidence & Composes Modalities
   └───────────┬───────────┘
               │
               ▼
   [ Verified Beliefs with Proof Lineage (Curry-Howard Traces) ]
```

---

## Features

* **Modal Logic Converter**: Heuristically translates natural language statements and auxiliary verbs into formal modal categories (`necessity`, `possibility`, `axiomatic`, `obligation`, `probability`).
* **Observer Uncertainty**: Every belief carries a statistical confidence score ($0.0 \dots 1.0$, default $0.95$). Confidences compound logically along deduction paths ($c_1 \times c_2$).
* **Conflict Detection**: Automatically flags contradictory observations (e.g., conflicting functional locations or incompatible modalities) without system collapse.
* **Rigid Structural Scaffolding**: Plug-and-play deductive rules (Transitive, Symmetric, Subsumptive, Inverse) that guarantee valid relational derivations.
* **Proof Lineage (Curry-Howard)**: Recursively reconstructs the full derivation tree (`inferred_from` and `justification`) for any belief in the model.
* **Zero Heavy Dependencies**: Pure Python standard library core.

---

## Quickstart

### 1. Installation

Clone and install locally:
```bash
git clone https://github.com/ufijuice/mlc.git
cd mlc
pip install -e .
```

### 2. Run the Demo

Run the interactive demonstration:
```bash
python demo.py
```

### 3. Basic Usage

```python
from mlc import WorldModel, Modality, TransitiveRule

# 1. Initialize the internal world model
wm = WorldModel()
wm.add_rule(TransitiveRule("is_a"))

# 2. Ingest observations under observer uncertainty
wm.observe(
    subject="Socrates",
    predicate="is_a",
    object="Human",
    modality=Modality.NECESSITY,
    confidence=0.98
)

wm.observe(
    subject="Human",
    predicate="is_a",
    object="Mortal",
    modality=Modality.FACTUAL,
    confidence=0.95
)

# 3. Ingest natural language with modal qualification
wm.observe_text("Alice works for Occur.")

# 4. Step the rigid inference engine
inferred = wm.infer()
for b in inferred:
    print(b)
# Output:
# Belief#4: (Alice, employed_by, Occur) (95%) <- [3]
# Belief#5: (Socrates, is_a, Mortal) [deduction] (93.1%) <- [1, 2]

# 5. Inspect the proof trace (why does the agent believe this?)
wm.print_proof_trace(5)
# Output:
# Belief #5: (Socrates, is_a, Mortal) [deduction] (93.1%) - by Transitivity of 'is_a'
#   └── Belief #1: (Socrates, is_a, Human) [necessity] (98.0%) - by Direct Observation
#   └── Belief #2: (Human, is_a, Mortal) [factual] (95.0%) - by Direct Observation
```

---

## Running Tests

Run the full unit test suite:
```bash
python -m unittest discover tests
```

---

## Roadmap

- [ ] Kripke Frame semantics for possible-world graph transitions.
- [ ] Active Inference / Action-selection policies based on world-model state.
- [ ] D3 / Graphviz visualizer export for real-time cognitive state rendering.
- [ ] Integration with local LLMs (e.g. Ollama) for neuro-symbolic groundings.

---

## License

MIT License. Developed by Pavel Chekmaryov ([@ufijuice](https://github.com/ufijuice)).
