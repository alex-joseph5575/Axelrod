from axelrod_evo.action import Action
from axelrod_evo.player import Player

C, D = Action.C, Action.D


class Appeaser(Player):
    """A player who tries to guess what the opponent wants.

    Switch the classifier every time the opponent plays D.
    Start with C, switch between C and D when opponent plays D.

    Names:

    - Appeaser: Original Name by Jochen Müller
    """

    name = "Appeaser"
    classifier = {
        "memory_depth": float("inf"),  # Depends on internal memory.
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        if not len(opponent.history):
            return C
        else:
            if opponent.history[-1] == D:
                if self.history[-1] == C:
                    return D
                else:
                    return C
        return self.history[-1]
