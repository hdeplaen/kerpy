# coding=utf-8
from ..Transform import Transform
from .MinimumCentering import MinimumCentering
from kerch.utils.type import EPS

import torch


class MinMaxNormalization(Transform):
    def __init__(self, explicit: bool, default_path: bool = False, **kwargs):
        super(MinMaxNormalization, self).__init__(explicit=explicit,
                                                  name="Min Max Normalization", default_path=default_path, **kwargs)

    def _explicit_statistics(self, sample):
        max_sample = torch.max(sample, dim=0).values
        if type(self.parent) is MinimumCentering:
            return max_sample  # new min is 0
        else:
            min_sample = torch.min(sample, dim=0).values
            return max_sample - min_sample

    def _explicit_sample(self):
        sample = self.parent.sample
        norm = self.statistics_sample(sample)
        return sample / torch.clamp(norm, min=EPS)

    def _explicit_statistics_oos(self, x=None, oos=None):
        return self.statistics_sample()

    def _explicit_oos(self, x=None):
        return self.parent.oos(x=x) / torch.clamp(self.statistics_oos(x=x), min=EPS)

    def _revert_explicit(self, oos):
        return oos * torch.clamp(self.statistics_sample(), min=EPS)