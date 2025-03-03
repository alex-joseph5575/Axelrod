from itertools import cycle
from typing import List

from axelrod_evo.action import Action
from axelrod_evo.player import Player

C, D = Action.C, Action.D


class MockPlayer(Player):
    """Creates a mock player that plays a given sequence of actions. If
    no actions are given, plays like Cooperator. Used for testing.
    """

    name = "Mock Player"

    def __init__(self, actions: List[Action] = None) -> None:
        super().__init__()
        if not actions:
            actions = []
        self.actions = cycle(actions)

    def strategy(self, opponent: Player) -> Action:
        # Return the next saved action, if present.
        try:
            action = self.actions.__next__()
            return action
        except StopIteration:
            return C
