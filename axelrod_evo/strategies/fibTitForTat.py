from axelrod.action import Action, actions_to_str
from axelrod.player import Player
from axelrod.strategy_transformers import (
    FinalTransformer,
    TrackHistoryTransformer,
)
from misc_functions import (
    fib, getRandom
)

C, D = Action.C, Action.D
turnCount = 0

class fibTitForTat(Player):
    """
    A player starts by cooperating and then mimics the previous action of the
    opponent.
    This strategy was referred to as the *'simplest'* strategy submitted to
    Axelrod's first tournament. It came first.
    Note that the code for this strategy is written in a fairly verbose
    way. This is done so that it can serve as an example strategy for
    those who might be new to Python.
    Names:
    - Rapoport's strategy: [Axelrod1980]_
    - TitForTat: [Axelrod1980]_
    """

    # These are various properties for the strategy
    name = "fibTitForTat"
    classifier = {
        "memory_depth": 1,  # Four-Vector = (1.,0.,1.,0.)
        "stochastic": False,
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def strategy(self, opponent: Player) -> Action:
        turnCount += 1
        """This is the actual strategy"""
        # First move
        if not self.history:
            return C
        
        # Each turn, fibTitForTat has a chance of defecting outright
        # as determined by a one-in-fib(turnCount) chance
        fibChance = fib(turnCount)
        if getRandom(fibChance) == True:
            return D

        # React to the opponent's last move
        if opponent.history[-1] == D:
            return D
        return C
    
    def clone(self):
        return self