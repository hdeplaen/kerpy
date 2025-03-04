# coding=utf-8
"""
File containing the indicator kernel class.

@author: HENRI DE PLAEN
@copyright: KU LEUVEN
@license: MIT
@date: May 2022
"""
from typing import Iterator
from ... import utils
from ..implicit import Implicit, Kernel

import torch



@utils.extend_docstring(Kernel)
class Indicator(Implicit):
    r"""
    Indicator kernel.

    .. math::
        k(x,y) = \left\{
        \begin{array}
        g\gamma & \text{ if } |x-y|=0, \\
        1 & \text{ if } 0 < |x-y| \leq p, \\
        0 & \text{ otherwise.}
        \end{array}
        \right.

    .. note ::
        If the default value for :math:`\gamma` is used and the :math:`p` is to be trained, their two values will be
        linked.

    .. warning::
        Depending on the choice of :math:`\gamma`, the kernel may not be positive semi-definite. The default value
        however ensures it, as long as the inputs are integers. If they are not, this may get more complicated.

    .. warning::
        For this name of kernel, the input dimension of the datapoints `dim_input` must be 1.

    :param lag: Lag parameter :math:`p`., defaults to 1.
    :param gamma: Identity value :math:`\gamma` of the kernel. If `None`, the value will be :math:`\gamma = 2p+1` to
        ensure positive semi-definiteness., defaults to `None`
    :param lag_trainable: `True` if the gradient of the lag :math:`p` is to be computed. If so, a graph is computed
        and the lag can be updated. `False` just leads to a static computation., defaults to `False`
    :param gamma_trainable: `True` if the gradient of the :math:`\gamma` is to be computed. If so, a graph is computed
        and the :math:`\gamma` can be updated. `False` just leads to a static computation., this value will be tied to the
        evolution of the lag :math:`p`., defaults to `False`
    :type lag: double, optional
    :type gamma: double, optional
    :type lag_trainable: bool, optional
    :type gamma_trainable: bool, optional
    """

    def __init__(self, *args, **kwargs):
        """
        :param lag: bandwidth of the kernel (default 1)
        :param gamma: value on the diagonal (default 2 * lag + 1, which ensures PSD in most cases)
        """
        self._lag = kwargs.pop('lag', 1)
        super(Indicator, self).__init__(*args, **kwargs)
        assert self._dim_input == 1, "The indicator kernel is only defined for 1-dimensional entries."

        self._lag_trainable = kwargs.pop('lag_trainable', False)
        self._lag = torch.nn.Parameter(
            torch.tensor(self._lag, dtype=utils.FTYPE), requires_grad=self._lag_trainable)

        self._gamma_trainable = kwargs.pop('gamma_trainable', False)
        gamma = kwargs.pop('gamma', None)
        if gamma is None:
            self._link_training = True
            self._gamma = torch.nn.Parameter(2 * self._lag.data + 1, requires_grad=False)
        else:
            self._link_training = False
            self._gamma = torch.nn.Parameter(
                torch.tensor(gamma, dtype=utils.FTYPE), requires_grad=self._gamma_trainable)

    def __str__(self):
        return f"Indicator kernel (lag: {self.lag})"

    @property
    def hparams_variable(self):
        return {'Kernel lag': self.lag,
                'Kernel gamma': self.gamma}

    @property
    def lag(self):
        r"""
        Lah :math:`p` of the kernel.
        """
        if isinstance(self._lag, torch.nn.Parameter):
            return self._lag.data.cpu().numpy()
        return self._lag

    @lag.setter
    def lag(self, val):
        self._reset_cache(reset_persisting=False)
        self._lag.data = utils.castf(val, tensor=False, dev=self._lag.device)

    @property
    def lag_trainable(self) -> bool:
        r"""
        Boolean indicating if the lag :math:`p` is trainable.
        """
        return self._lag_trainable

    @lag_trainable.setter
    def lag_trainable(self, val: bool):
        self._lag_trainable = val
        self._lag.requires_grad = self._lag_trainable

    @property
    def hparams_fixed(self):
        return {"Kernel": "Indicator", **super(Indicator, self).hparams_fixed}

    @property
    def gamma(self):
        return self._gamma.data.cpu().numpy()

    @gamma.setter
    def gamma(self, val):
        self._reset_cache(reset_persisting=False)
        self._gamma.data = utils.castf(val, tensor=False, dev=self._gamma.device)

    def _implicit(self, x, y):
        if self._link_training and self.lag_trainable:
            self._gamma.data = 2 * self.lag + 1

        x = x[:, :, None]
        y = y.T[:, None, :]

        diff = (x - y).squeeze()
        assert len(diff.shape) == 2, 'Indicator kernel is only defined for 1-dimensional entries.'

        output = (torch.abs(diff).le(self._lag)).type(dtype=utils.FTYPE)
        output[diff == 0] = self._gamma

        return output

    def _slow_parameters(self, recurse=True) -> Iterator[torch.nn.Parameter]:
        yield self._lag
        yield self._gamma
        yield from super(Indicator, self)._slow_parameters(recurse)
