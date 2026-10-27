"""
Society & Behavioral Models Simulator:
Simulates multi-agent socio-economic dynamics, ideological echo-chambers,
and perceived meritocracy using MLC (Modal Logic Converter) as the cognitive core.
"""

import random
from enum import Enum
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass, field
from mlc.engine import WorldModel
from mlc.types import Modality, Belief
from mlc.rules import TransitiveRule, SubsumptionRule, get_default_rules


class Archetype(str, Enum):
    """
    Behavioral models that compete in society.
    """
    MERIT_SEEKER = "merit_seeker"              # Rigorous modal logic, requires proof provenance & high confidence
    SHORT_TERM_OPTIMIZER = "short_term_opt"     # Chases immediate profit, low modal rigor, high risk
    SIMULACRUM_FOLLOWER = "simulacrum_follower" # Accepts echo-chamber consensus, rejects counter-evidence


@dataclass
class MarketTask:
    """
    A real-world economic problem requiring grounded knowledge to solve.
    E.g., solving requires knowing that (technology, enables, automation).
    """
    title: str
    required_subject: str
    required_predicate: str
    required_object: str
    reward: float = 20.0
    failure_cost: float = 5.0


@dataclass
class InformationSignal:
    """
    A piece of information or social media content circulating in society.
    """
    subject: str
    predicate: str
    object: str
    modality: Modality
    is_grounded_truth: bool
    sensationalism: float  # High sensationalism = boosted by engagement algorithms
    source_archetype: Archetype


class Citizen:
    """
    An agent in the society whose internal worldview is powered by MLC.
    """
    def __init__(self, agent_id: int, archetype: Archetype, initial_wealth: float = 100.0):
        self.id = agent_id
        self.archetype = archetype
        self.wealth = initial_wealth
        self.brain = WorldModel(rules=get_default_rules())
        self.reputation: float = 1.0
        self.productive_successes: int = 0
        self.failures: int = 0

    def ingest_information(self, signal: InformationSignal, algorithm_bias: float = 0.5) -> bool:
        """
        Process incoming information according to the agent's behavioral model.
        Returns True if the signal was incorporated into the internal world model.
        """
        # Echo-Chamber / Simulacrum bias: rejects out-group or dissonant signals
        if self.archetype == Archetype.SIMULACRUM_FOLLOWER:
            # If sensational or matches existing object polarity, accept uncritically
            if signal.sensationalism > 0.6 or not signal.is_grounded_truth:
                self.brain.observe(
                    subject=signal.subject,
                    predicate=signal.predicate,
                    object=signal.object,
                    modality=signal.modality,
                    confidence=0.90,
                    context="Social Media Feed",
                )
                return True
            # Suppress grounded truth that causes cognitive dissonance
            if random.random() < algorithm_bias:
                return False

        elif self.archetype == Archetype.SHORT_TERM_OPTIMIZER:
            # Adopts beliefs that seem popular or immediately profitable
            confidence = 0.75 if signal.sensationalism > 0.5 else 0.85
            self.brain.observe(
                subject=signal.subject,
                predicate=signal.predicate,
                object=signal.object,
                modality=signal.modality,
                confidence=confidence,
                context="Market Signal",
            )
            return True

        elif self.archetype == Archetype.MERIT_SEEKER:
            # Rigorous: requires axiomatic/high necessity or discounts sensationalism
            confidence = 0.95 if signal.is_grounded_truth else 0.35
            if confidence >= 0.70:
                self.brain.observe(
                    subject=signal.subject,
                    predicate=signal.predicate,
                    object=signal.object,
                    modality=signal.modality,
                    confidence=confidence,
                    context="Verified Source",
                )
                return True

        return False

    def think(self) -> int:
        """
        Step the MLC internal reasoning engine to derive new beliefs.
        Returns the number of newly inferred beliefs.
        """
        new_inferred = self.brain.infer()
        return len(new_inferred)

    def attempt_task(self, task: MarketTask) -> bool:
        """
        Test whether the agent's internal world model can solve a real-world task.
        Requires having the necessary grounded belief with sufficient confidence.
        """
        belief = self.brain.find(task.required_subject, task.required_predicate, task.required_object)

        # Grounded success: agent has verified belief and it is not conflicting
        if belief and belief.confidence >= 0.75 and not belief.is_conflicting:
            self.wealth += task.reward
            self.productive_successes += 1
            self.reputation += 0.1
            return True
        else:
            # Bluff / Failure
            penalty = task.failure_cost
            if self.archetype == Archetype.SHORT_TERM_OPTIMIZER and random.random() < 0.35:
                # Short-term optimizer bluffs through survivorship bias occasionally
                self.wealth += task.reward * 0.7
                self.productive_successes += 1
                return True
            else:
                self.wealth = max(0.0, self.wealth - penalty)
                self.failures += 1
                self.reputation = max(0.1, self.reputation - 0.05)
                return False


class SocietySimulation:
    """
    Macro-level socio-economic simulation.
    Tests how algorithmic recommendation feeds alter the shared reality,
    meritocracy, and wealth distribution across behavioral models.
    """

    def __init__(
        self,
        num_merit_seekers: int = 20,
        num_short_term_opt: int = 20,
        num_simulacrum: int = 20,
        algorithm_bias: float = 0.5,
    ):
        self.algorithm_bias = algorithm_bias
        self.population: List[Citizen] = []
        agent_id = 1

        for _ in range(num_merit_seekers):
            self.population.append(Citizen(agent_id, Archetype.MERIT_SEEKER))
            agent_id += 1
        for _ in range(num_short_term_opt):
            self.population.append(Citizen(agent_id, Archetype.SHORT_TERM_OPTIMIZER))
            agent_id += 1
        for _ in range(num_simulacrum):
            self.population.append(Citizen(agent_id, Archetype.SIMULACRUM_FOLLOWER))
            agent_id += 1

        self.knowledge_base_truth: List[InformationSignal] = [
            InformationSignal("Skill", "causes", "Productivity", Modality.AXIOMATIC, True, 0.2, Archetype.MERIT_SEEKER),
            InformationSignal("Productivity", "causes", "Wealth", Modality.NECESSITY, True, 0.2, Archetype.MERIT_SEEKER),
            InformationSignal("Rigorous_Study", "causes", "Skill", Modality.NECESSITY, True, 0.1, Archetype.MERIT_SEEKER),
            InformationSignal("Integrity", "causes", "Trust", Modality.AXIOMATIC, True, 0.1, Archetype.MERIT_SEEKER),
            InformationSignal("Trust", "causes", "Collaboration", Modality.NECESSITY, True, 0.2, Archetype.MERIT_SEEKER),
        ]

        self.knowledge_base_simulacrum: List[InformationSignal] = [
            InformationSignal("Hype", "causes", "Instant_Wealth", Modality.POSSIBILITY, False, 0.95, Archetype.SIMULACRUM_FOLLOWER),
            InformationSignal("Deception", "causes", "Status", Modality.POSSIBILITY, False, 0.85, Archetype.SHORT_TERM_OPTIMIZER),
            InformationSignal("Outgroup", "causes", "Scarcity", Modality.POSSIBILITY, False, 0.90, Archetype.SIMULACRUM_FOLLOWER),
            InformationSignal("Real_Effort", "causes", "Exhaustion", Modality.FACTUAL, False, 0.80, Archetype.SIMULACRUM_FOLLOWER),
        ]

        self.market_tasks: List[MarketTask] = [
            MarketTask("Automate Workflow", "Skill", "causes", "Productivity", reward=30.0, failure_cost=8.0),
            MarketTask("Scale Enterprise", "Productivity", "causes", "Wealth", reward=50.0, failure_cost=15.0),
            MarketTask("Build Industry Consortium", "Trust", "causes", "Collaboration", reward=40.0, failure_cost=10.0),
        ]

        self.history: List[Dict] = []

    def step(self, generation: int) -> Dict:
        """Execute one generational cycle of communication, deduction, and economic tests."""

        # 1. Information Broadcast (Social Media / Information Feed)
        for agent in self.population:
            # Algorithmic feed selection: bias promotes sensational content
            if random.random() < self.algorithm_bias:
                signal = random.choice(self.knowledge_base_simulacrum)
            else:
                signal = random.choice(self.knowledge_base_truth)
            agent.ingest_information(signal, self.algorithm_bias)

        # 2. Epistemic Deduction: Agents step their MLC WorldModel
        for agent in self.population:
            agent.think()

        # 3. Economic Labor Market & Task Testing
        for agent in self.population:
            task = random.choice(self.market_tasks)
            agent.attempt_task(task)

        # 4. Measure Metrics
        metrics = self.calculate_metrics(generation)
        self.history.append(metrics)
        return metrics

    def calculate_metrics(self, generation: int) -> Dict:
        """
        Calculate macro-societal metrics:
        - Shared Reality Index (overlap of true grounded beliefs)
        - Average Wealth by Archetype
        - Gini Inequality Coefficient
        """
        # Grounded truth keys
        ground_keys = {
            ("skill", "causes", "productivity"),
            ("productivity", "causes", "wealth"),
            ("trust", "causes", "collaboration"),
            ("skill", "causes", "wealth"),  # Transitive deduction
        }

        agent_grounded_counts = []
        for a in self.population:
            matched = 0
            for k in ground_keys:
                b = a.brain.find(k[0], k[1], k[2])
                if b and not b.is_conflicting and b.confidence >= 0.70:
                    matched += 1
            agent_grounded_counts.append(matched / len(ground_keys))

        shared_reality_index = sum(agent_grounded_counts) / len(agent_grounded_counts)

        # Wealth by archetype
        wealth_by_arch = {}
        for arch in Archetype:
            agents = [a for a in self.population if a.archetype == arch]
            avg_w = sum(a.wealth for a in agents) / max(1, len(agents))
            wealth_by_arch[arch.value] = round(avg_w, 2)

        # Gini Coefficient
        wealths = sorted([a.wealth for a in self.population])
        n = len(wealths)
        total_wealth = sum(wealths)
        if total_wealth == 0:
            gini = 0.0
        else:
            diff_sum = sum(abs(i - j) for i in wealths for j in wealths)
            gini = diff_sum / (2 * n * total_wealth)

        return {
            "generation": generation,
            "shared_reality_index": round(shared_reality_index, 3),
            "gini_coefficient": round(gini, 3),
            "wealth_by_archetype": wealth_by_arch,
        }

    def run(self, generations: int = 30) -> List[Dict]:
        """Run simulation over multiple generations."""
        for g in range(1, generations + 1):
            self.step(g)
        return self.history
