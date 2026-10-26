import unittest
from mlc import (
    WorldModel,
    Modality,
    TransitiveRule,
    SymmetricRule,
    SubsumptionRule,
    InverseRule,
)
from mlc.modal_map import compose_modalities


class TestWorldModel(unittest.TestCase):

    def setUp(self):
        self.wm = WorldModel()

    def test_transitive_inference_and_confidence(self):
        # A located_in B (0.90) and B located_in C (0.90)
        self.wm.observe("Paris", "located_in", "France", confidence=0.90)
        self.wm.observe("France", "located_in", "Europe", confidence=0.90)

        inferred = self.wm.infer()
        derived = self.wm.find("Paris", "located_in", "Europe")

        self.assertIsNotNone(derived)
        self.assertAlmostEqual(derived.confidence, 0.81, places=3)
        self.assertEqual(len(derived.inferred_from), 2)
        self.assertEqual(derived.justification, "Transitivity of 'located_in'")

    def test_modal_composition(self):
        self.assertEqual(compose_modalities(Modality.NECESSITY, Modality.NECESSITY), Modality.NECESSITY)
        self.assertEqual(compose_modalities(Modality.NECESSITY, Modality.POSSIBILITY), Modality.POSSIBILITY)
        self.assertEqual(compose_modalities(Modality.AXIOMATIC, Modality.AXIOMATIC), Modality.AXIOMATIC)

    def test_symmetric_inference(self):
        self.wm.observe("Alice", "married_to", "Bob")
        self.wm.infer()
        bob_married = self.wm.find("Bob", "married_to", "Alice")
        self.assertIsNotNone(bob_married)
        self.assertEqual(bob_married.justification, "Symmetry of 'married_to'")

    def test_subsumption_inference(self):
        self.wm.observe("Alice", "works_for", "AcmeCorp")
        self.wm.infer()
        employed = self.wm.find("Alice", "employed_by", "AcmeCorp")
        self.assertIsNotNone(employed)

    def test_inverse_inference(self):
        self.wm.observe("ProfessorX", "teaches", "Wolverine")
        self.wm.infer()
        student = self.wm.find("Wolverine", "learned_from", "ProfessorX")
        self.assertIsNotNone(student)

    def test_conflict_detection(self):
        b1 = self.wm.observe("Occur", "located_in", "SF", confidence=0.95)
        self.assertFalse(b1.is_conflicting)

        # Conflicting location
        b2 = self.wm.observe("Occur", "located_in", "NYC", confidence=0.70)
        self.assertTrue(b1.is_conflicting)
        self.assertTrue(b2.is_conflicting)

    def test_proof_trace(self):
        self.wm.observe("A", "ancestor_of", "B")
        self.wm.observe("B", "ancestor_of", "C")
        self.wm.infer()
        c_ancestor = self.wm.find("A", "ancestor_of", "C")
        self.assertIsNotNone(c_ancestor)

        trace = self.wm.get_proof_trace(c_ancestor.id)
        self.assertEqual(trace["statement"], "(A, ancestor_of, C)")
        self.assertEqual(len(trace["premises"]), 2)

    def test_text_converter(self):
        b = self.wm.observe_text("Aristotle must be a philosopher.")
        self.assertIsNotNone(b)
        self.assertEqual(b.modality, Modality.DEDUCTION)
        self.assertEqual(b.subject, "Aristotle")

        b2 = self.wm.observe_text("Agents must obey safety rules.")
        self.assertIsNotNone(b2)
        self.assertEqual(b2.modality, Modality.NECESSITY)


if __name__ == "__main__":
    unittest.main()
