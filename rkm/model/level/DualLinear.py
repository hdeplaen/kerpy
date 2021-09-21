"""
Dual linear class for a RKM level.

@author: HENRI DE PLAEN
@copyright: KU LEUVEN
@license: MIT
@date: March 2021
"""

import torch

import rkm
import rkm.model.level.Linear as Linear


class DualLinear(Linear.Linear):
    def __init__(self, **kwargs):
        super(DualLinear, self).__init__(**kwargs)
        self._alpha = torch.nn.Parameter(
            torch.nn.init.orthogonal_(torch.empty((kwargs["size_out"], kwargs["init_kernels"]),
                                                  dtype=rkm.ftype)),
            requires_grad=self._soft)
        self._bias = torch.nn.Parameter(torch.zeros([kwargs["size_out"]], dtype=rkm.ftype),
                                        requires_grad=self._soft and self._requires_bias)
        self._classifier = kwargs["classifier"]
        self._y = torch.nn.Parameter(torch.ones((kwargs["init_kernels"], kwargs["size_out"]), dtype=rkm.ftype),
                                     requires_grad=False)

    @property
    def alpha(self):
        if self._classifier:
            return torch.abs(self._alpha.t())
        else:
            return self._alpha.t()

    @property
    def bias(self):
        return self._bias

    def set(self, a, b=None):
        self.alpha.data = a.data.t()
        if b is not None: self.bias.data = b.data

    def forward(self, x, idx_sv):
        if self._classifier:
            x_tilde = x @ (self._y[idx_sv] * self.alpha[idx_sv]) + \
                      self.bias.expand([x.shape[0], self.bias.shape[0]])
        else:
            x_tilde = x @ self.alpha[idx_sv] + self.bias.expand([x.shape[0],self.bias.shape[0]])
        return x_tilde.squeeze()

    def project(self):
        if self._classifier:
            self.alpha.data -= self._y.data * torch.mean(self.alpha.data)
        else:
            self.alpha.data -= torch.mean(self.alpha.data)

    def init_y(self, y, idxs):
        self._y[idxs] = y.data.unsqueeze(dim=1)

    def merge(self, idxs):
        if self._classifier: raise NotImplemented
        self.alpha[idxs[:, 0]] += self.alpha[idxs[:, 1]]
        self.alpha.gather(dim=0, index=idxs[:, 1], out=self._alpha)

    def reduce(self, idxs):
        if self._classifier: raise NotImplemented
        self.alpha.gather(dim=0, index=idxs, out=self._alpha)

    def reduce_idxs(self, **kwargs):
        if self._classifier: raise NotImplemented
        return torch.nonzero(torch.abs(self.alpha) < kwargs["rtol"], as_tuple=True)
