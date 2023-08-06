from mosfit.modules.module import Module

CLASS_NAME = 'Transform'


class Transform(Module):
    """Parent class for transforms.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def process(self, **kwargs):
        return {}

    def set_times_lums(self, **kwargs):
        self._times = kwargs['resttimes']
        self._rest_t_explosion = kwargs['resttexplosion']
        if 'densetimes' in kwargs:
            self._dense_times = kwargs['densetimes']
            self._dense_luminosities = kwargs['luminosities']
        elif min(self._times) > self._rest_t_explosion:
            self._dense_times = [self._rest_t_explosion] + self._times
            self._dense_luminosities = [0.0] + kwargs['luminosities']
        self._times_since_exp = [(x - self._rest_t_explosion)
                                 for x in self._times]
        self._dense_times_since_exp = [(x - self._rest_t_explosion)
                                       for x in self._dense_times]
