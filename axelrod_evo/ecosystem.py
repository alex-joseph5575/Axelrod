"""Tools for simulating population dynamics of immutable players.

An ecosystem runs in the context of a previous tournament, and takes the
results as input. That means no matches are run by the ecosystem, and a
tournament needs to happen before it is created. For example:

players = [axelrod_evo.Cooperator(), axlerod.Defector()]
tournament = axelrod_evo.Tournament(players=players)
results = tournament.play()
ecosystem = axelrod_evo.Ecosystem(results)
ecosystem.reproduce(100)
"""

import random
from typing import Callable, List

from axelrod_evo.result_set import ResultSet


class Ecosystem(object):
    """An ecosystem based on the payoff matrix from a tournament.

    Attributes
    ----------
    num_players: int
        The number of players
    """

    def __init__(
        self,
        results: ResultSet,
        fitness: Callable[[float], float] = None,
        population: List[int] = None,
    ) -> None:
        """Create a new ecosystem.

        Parameters
        ----------
        results: ResultSet
            The results of the tournament run beforehand to use.
        fitness: List of callables
            The reproduction rate at which populations reproduce.
        population: List of ints.
            The initial populations of the players, corresponding to the
            payoff matrix in results.
        """

        self.results = results
        self.num_players = self.results.num_players
        self.payoff_matrix = self.results.payoff_matrix
        self.payoff_stddevs = self.results.payoff_stddevs

        # Population sizes will be recorded in this nested list, with each
        # internal list containing strategy populations for a given turn. The
        # first list, representing the starting populations, will by default
        # have all equal values, and all population lists will be normalized to
        # one. An initial population vector can also be passed. This will be
        # normalised, but must be of the correct size and have all non-negative
        # values.
        if population:
            if min(population) < 0:
                raise TypeError(
                    "Minimum value of population vector must be non-negative"
                )
            elif len(population) != self.num_players:
                raise TypeError(
                    "Population vector must be same size as number of players"
                )
            else:
                norm = sum(population)
                self.population_sizes = [[p / norm for p in population]]
        else:
            self.population_sizes = [
                [1 / self.num_players for _ in range(self.num_players)]
            ]

        # This function is quite arbitrary and probably only influences the
        # kinetics for the current code.
        if fitness:
            self.fitness = fitness
        else:
            self.fitness = lambda p: p

    def reproduce(self, turns: int):
        """Reproduce populations according to the payoff matrix.

        Parameters
        ----------
        turns: int
            The number of turns to run.
        """
        for iturn in range(turns):
            plist = list(range(self.num_players))
            pops = self.population_sizes[-1]

            # The unit payoff for each player in this turn is the sum of the
            # payoffs obtained from playing with all other players, scaled by
            # the size of the opponent's population. Note that we sample the
            # normal distribution based on the payoff matrix and its standard
            # deviations obtained from the iterated PD tournament run
            # previously.
            payoffs = [0.0 for ip in plist]
            for ip in plist:
                for jp in plist:
                    avg = self.payoff_matrix[ip][jp]
                    dev = self.payoff_stddevs[ip][jp]
                    p = random.normalvariate(avg, dev)
                    payoffs[ip] += p * pops[jp]

            # The fitness should determine how well a strategy reproduces. The
            # new populations should be multiplied by something that is
            # proportional to the fitness, but we are normalizing anyway so
            # just multiply times fitness.
            fitness = [self.fitness(p) for p in payoffs]
            newpops = [p * f for p, f in zip(pops, fitness)]

            # Make sure the new populations are normalized to one.
            norm = sum(newpops)
            newpops = [p / norm for p in newpops]

            self.population_sizes.append(newpops)
