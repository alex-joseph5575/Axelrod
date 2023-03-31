import subprocess
import sys

modules = [
    "run_strategy_indexer.py",
    "axelrod_evo/action.py",
    "axelrod_evo/deterministic_cache.py",
    "axelrod_evo/ecosystem.py",
    "axelrod_evo/evolvable_player.py",
    "axelrod_evo/fingerprint.py",
    "axelrod_evo/game.py",
    "axelrod_evo/load_data_.py",
    "axelrod_evo/mock_player.py",
    "axelrod_evo/moran.py",
    "axelrod_evo/plot.py",
    "axelrod_evo/random_.py",
    "axelrod_evo/tournament.py",
    "axelrod_evo/strategies/adaptive.py",
    "axelrod_evo/strategies/alternator.py",
    "axelrod_evo/strategies/ann.py",
    "axelrod_evo/strategies/apavlov.py",
    "axelrod_evo/strategies/appeaser.py",
    "axelrod_evo/strategies/averagecopier.py",
    "axelrod_evo/strategies/axelrod_evo_first.py",
    "axelrod_evo/strategies/axelrod_evo_second.py",
    "axelrod_evo/strategies/backstabber.py",
    "axelrod_evo/strategies/better_and_better.py",
    "axelrod_evo/strategies/calculator.py",
    "axelrod_evo/strategies/cooperator.py",
    "axelrod_evo/strategies/cycler.py",
    "axelrod_evo/strategies/darwin.py",
    "axelrod_evo/strategies/defector.py",
    "axelrod_evo/strategies/forgiver.py",
    "axelrod_evo/strategies/gradualkiller.py",
    "axelrod_evo/strategies/grudger.py",
    "axelrod_evo/strategies/grumpy.py",
    "axelrod_evo/strategies/handshake.py",
    "axelrod_evo/strategies/hunter.py",
    "axelrod_evo/strategies/inverse.py",
    "axelrod_evo/strategies/mathematicalconstants.py",
    "axelrod_evo/strategies/memoryone.py",
    "axelrod_evo/strategies/memorytwo.py",
    "axelrod_evo/strategies/mutual.py",
    "axelrod_evo/strategies/negation.py",
    "axelrod_evo/strategies/oncebitten.py",
    "axelrod_evo/strategies/prober.py",
    "axelrod_evo/strategies/punisher.py",
    "axelrod_evo/strategies/qlearner.py",
    "axelrod_evo/strategies/rand.py",
    "axelrod_evo/strategies/titfortat.py",
    "axelrod_evo/strategies/hmm.py",
    "axelrod_evo/strategies/human.py",
    "axelrod_evo/strategies/finite_state_machines.py",
    "axelrod_evo/strategies/worse_and_worse.py",
]

exit_codes = []
for module in modules:
    rc = subprocess.call(
        ["mypy", "--ignore-missing-imports", "--follow-imports", "skip", module]
    )
    exit_codes.append(rc)
sys.exit(max(exit_codes))
