from mot.cl_routines.optimizing.base import AbstractOptimizer

__author__ = 'Robbert Harms'
__date__ = "2016-11-22"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class Randomizer(object):

    pass


class RandomRestartOptimizer(AbstractOptimizer):

    def __init__(self, optimizer, randomizer, **kwargs):
        """A meta optimization routine that allows multiple random restarts.

        This meta optimizer runs the given optimizer multiple times using different starting positions for each run.
        The starting positions are obtained using the ``randomizer`` which returns new starting points
        given the initial starting points.

        The returned results contain per problem instance the parameter that resulted in the lowest function value.

        Args:
            optimizer (AbstractOptimizer): the optimization routines to run one after another.
            randomizer (Randomizer): the randomizer instance we use to randomize the starting point
        """
        super(RandomRestartOptimizer, self).__init__(**kwargs)
        self._optimizer = optimizer
        self._randomizer = randomizer

    def minimize(self, model, init_params=None, full_output=False):
        pass
