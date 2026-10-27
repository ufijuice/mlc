import unittest
from mlc.simulation import SocietySimulation, Citizen, Archetype, MarketTask, InformationSignal
from mlc.types import Modality


class TestSocietySimulation(unittest.TestCase):

    def test_simulation_initialization(self):
        sim = SocietySimulation(
            num_merit_seekers=5,
            num_short_term_opt=5,
            num_simulacrum=5,
            algorithm_bias=0.2,
        )
        self.assertEqual(len(sim.population), 15)

    def test_simulation_step(self):
        sim = SocietySimulation(
            num_merit_seekers=4,
            num_short_term_opt=4,
            num_simulacrum=4,
            algorithm_bias=0.5,
        )
        metrics = sim.step(1)
        self.assertEqual(metrics["generation"], 1)
        self.assertIn("shared_reality_index", metrics)
        self.assertIn("gini_coefficient", metrics)
        self.assertIn("wealth_by_archetype", metrics)

    def test_agent_task_solution(self):
        citizen = Citizen(agent_id=1, archetype=Archetype.MERIT_SEEKER)
        # Give citizen the required knowledge
        citizen.brain.observe("Skill", "causes", "Productivity", Modality.AXIOMATIC, confidence=0.95)

        task = MarketTask("Test Task", "Skill", "causes", "Productivity", reward=50.0, failure_cost=10.0)
        success = citizen.attempt_task(task)
        self.assertTrue(success)
        self.assertEqual(citizen.wealth, 150.0)


if __name__ == "__main__":
    unittest.main()
