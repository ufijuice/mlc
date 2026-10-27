#!/usr/bin/env python3
"""
Society Simulation CLI Demo:
Tests the impact of algorithmic information bubbles and behavioral models on
macroeconomic health, shared reality, and meritocracy.
Based on Pavel Chekmaryov's 2021 Behavioral Models Research thesis.
"""

from mlc.simulation import SocietySimulation, Archetype

def print_separator(title: str):
    print("\n" + "=" * 78)
    print(f"  {title}")
    print("=" * 78)

def run_experiment(name: str, bias: float, generations: int = 25):
    print_separator(f"EXPERIMENT: {name} (Algorithm Bias: {bias:.0%})")
    sim = SocietySimulation(
        num_merit_seekers=20,
        num_short_term_opt=20,
        num_simulacrum=20,
        algorithm_bias=bias,
    )

    print(f"{'Gen':<5} | {'Shared Reality':<15} | {'Gini':<6} | {'Merit Seekers $':<16} | {'Short-Term $':<14} | {'Simulacrum $'}")
    print("-" * 78)

    results = sim.run(generations=generations)

    # Print snapshots
    for row in results:
        if row["generation"] in [1, 5, 10, 15, 20, 25]:
            gen = row["generation"]
            sri = f"{row['shared_reality_index']:.1%}"
            gini = f"{row['gini_coefficient']:.3f}"
            w_merit = f"${row['wealth_by_archetype']['merit_seeker']:.1f}"
            w_short = f"${row['wealth_by_archetype']['short_term_opt']:.1f}"
            w_simul = f"${row['wealth_by_archetype']['simulacrum_follower']:.1f}"
            print(f"{gen:<5} | {sri:<15} | {gini:<6} | {w_merit:<16} | {w_short:<14} | {w_simul}")

    final = results[-1]
    print("\n[Final Evaluation]:")
    print(f"  * Final Shared Reality Index : {final['shared_reality_index']:.1%}")
    print(f"  * Wealth Inequality (Gini)   : {final['gini_coefficient']:.3f}")
    print("  * Wealth Distribution by Archetype:")
    for arch, val in final["wealth_by_archetype"].items():
        print(f"      - {arch.replace('_', ' ').title():<22}: ${val}")

def main():
    print_separator("MLC BEHAVIORAL MODELS & SOCIETY SIMULATOR")
    print("  Simulating the evolution of behavioral models, epistemic bubbles,")
    print("  and the collapse vs preservation of shared reality.")

    # 1. Run Society with Heavy Algorithmic Bias (Echo-Chambers & Short-Term Maximization)
    run_experiment(
        name="Algorithmic Polarization & Simulacrum Trap",
        bias=0.85,
        generations=25,
    )

    # 2. Run Society with Transparent Information & Verifiable Standards
    run_experiment(
        name="Transparent Epistemic Environment (Healthy Meritocracy)",
        bias=0.15,
        generations=25,
    )

    print_separator("SIMULATION COMPLETE")
    print("  Conclusion: In a noisy information environment, agents with rigid modal")
    print("  logic (MLC) and proof provenance maintain productivity, while echo-chambers")
    print("  destroy shared reality and destabilize the social ladder.")
    print("=" * 78 + "\n")

if __name__ == "__main__":
    main()
