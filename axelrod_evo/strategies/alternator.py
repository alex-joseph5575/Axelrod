from axelrod_evo.action import Action
from axelrod_evo.player import Player

C, D = Action.C, Action.D


class Alternator(Player):
    """
    A player who alternates between cooperating and defecting.

    Names

    - Alternator: [Axelrod1984]_
    - Periodic player CD: [Mittal2009]_
    """

    name = "Alternator"
    classifier = {
        "memory_depth": 1,
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: Player) -> Action:
        """Actual strategy definition that determines player's action."""
        if len(self.history) == 0:
            return C
        if self.history[-1] == C:
            return D
        return C
