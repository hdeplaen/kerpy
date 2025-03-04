import unittest
import torch
import kerch

from kerch.transform.TransformTree import ProjectionTree
from kerch.utils.errors import BijectionError

kerch.set_log_level(40)  # only print errors
unittest.TestCase.__str__ = lambda x: ""
all_projections = ProjectionTree.all_projections.keys()

class TestProjections(unittest.TestCase):
    r"""
    Tests the various transform
    """

    def __init__(self, *args, **kwargs):
        super(TestProjections, self).__init__(*args, **kwargs)

        self.num_sample = 5
        self.num_oos = 4
        self.dim = 3

        scale = torch.randn((1, self.dim))
        self.sample = torch.randn((self.num_sample, self.dim)) * scale
        self.oos = torch.randn((self.num_oos, self.dim)) * scale


    def test_sphere(self):
        """Verifies the consistency of the transform onto the unit sphere."""
        TT = ProjectionTree(sample=self.sample, default_projections=["unit_sphere_normalization"], explicit=True)
        t_sample = TT.projected_sample
        t_oos = TT.apply(self.oos)
        self.assertAlmostEqual(torch.sum(torch.norm(t_sample, dim=1)).numpy(), self.num_sample, places=5)
        self.assertAlmostEqual(torch.sum(torch.norm(t_oos, dim=1)).numpy(), self.num_oos, places=5)
        self.assertRaises(BijectionError, TT.revert, t_oos)


    def test_mean_centering(self):
        """Verifies the consistency of the centering with the mean/average value of each feature across all sample
        points."""
        TT = ProjectionTree(sample=self.sample, default_projections=["mean_centering"], explicit=True)
        t_sample = TT.projected_sample
        t_oos = TT.apply(self.sample)
        self.assertAlmostEqual(torch.norm(torch.sum(t_sample, dim=0)).numpy(), 0, places=5)
        self.assertAlmostEqual(torch.norm(torch.sum(t_oos, dim=0)).numpy(), 0, places=5)
        t_orig = TT.revert(t_oos)
        self.assertAlmostEqual(torch.sum(torch.norm(t_orig - self.sample)).numpy(), 0, places=5)

    def test_minimum_centering(self):
        """Verifies the consistency of the centering with the minimum value of each feature across all sample points."""
        TT = ProjectionTree(sample=self.sample, default_projections=["minimum_centering"], explicit=True)
        t_sample = TT.projected_sample
        t_oos = TT.apply(self.sample)
        self.assertAlmostEqual(torch.norm(torch.min(t_sample, dim=0).values).numpy(), 0, places=5)
        self.assertAlmostEqual(torch.norm(torch.min(t_oos, dim=0).values).numpy(), 0, places=5)

        t_orig = TT.revert(t_oos)
        self.assertAlmostEqual(torch.sum(torch.norm(t_orig - self.sample)).numpy(), 0, places=5)


    def test_unit_variance_normalization(self):
        """Verifies the consistency of the normalization of each feature to unit variance, across all sample points."""
        TT = ProjectionTree(sample=self.sample, default_projections=["unit_variance_normalization"], explicit=True)
        t_sample = TT.projected_sample
        t_oos = TT.apply(self.sample)
        self.assertAlmostEqual(torch.sum(torch.std(t_sample, dim=0)).numpy(), self.dim, places=5)
        self.assertAlmostEqual(torch.sum(torch.std(t_oos, dim=0)).numpy(), self.dim, places=5)

        t_orig = TT.revert(t_oos)
        self.assertAlmostEqual(torch.sum(torch.norm(t_orig - self.sample)).numpy(), 0, places=5)

    def test_minmax_normalization(self):
        """Verifies the consistency of the the minimum maximum rescaling."""
        TT = ProjectionTree(sample=self.sample, default_projections=["minmax_normalization"], explicit=True)
        t_sample = TT.projected_sample
        t_oos = TT.apply(self.sample)
        self.assertAlmostEqual(torch.sum(torch.max(t_sample, dim=0).values -
                                          torch.min(t_sample, dim=0).values).numpy(), self.dim, places=5)
        self.assertAlmostEqual(torch.sum(torch.max(t_oos, dim=0).values -
                                          torch.min(t_oos, dim=0).values).numpy(), self.dim, places=5)

        t_orig = TT.revert(t_oos)
        self.assertAlmostEqual(torch.sum(torch.norm(t_orig - self.sample)).numpy(), 0, places=5)


    def test_minmax_rescaling(self):
        """Verifies the consistency of the affine of each feature rescaling to [0, 1], across all sample points."""
        TT = ProjectionTree(sample=self.sample, default_projections=["minmax_rescaling"], explicit=True)
        t_sample = TT.projected_sample
        t_oos = TT.apply(self.sample)
        self.assertAlmostEqual(torch.norm(torch.min(t_sample, dim=0).values).numpy(), 0, places=5)
        self.assertAlmostEqual(torch.sum(torch.max(t_sample, dim=0).values).numpy(), self.dim, places=5)
        self.assertAlmostEqual(torch.norm(torch.min(t_oos, dim=0).values).numpy(), 0, places=5)
        self.assertAlmostEqual(torch.sum(torch.max(t_oos, dim=0).values).numpy(), self.dim, places=5)

        t_orig = TT.revert(t_oos)
        self.assertAlmostEqual(torch.sum(torch.norm(t_orig - self.sample)).numpy(), 0, places=5)


    def test_standardize(self):
        """Verifies the consistency of the standardization of each feature rescaling (0 mean, 1 std),
        across all sample points."""
        TT = ProjectionTree(sample=self.sample, default_projections=["standardize"], explicit=True)
        t_sample = TT.projected_sample
        t_oos = TT.apply(self.sample)
        self.assertAlmostEqual(torch.norm(torch.sum(t_sample, dim=0)).numpy(), 0, places=5)
        self.assertAlmostEqual(torch.norm(torch.sum(t_oos, dim=0)).numpy(), 0, places=5)
        self.assertAlmostEqual(torch.sum(torch.std(t_sample, dim=0)).numpy(), self.dim, places=5)
        self.assertAlmostEqual(torch.sum(torch.std(t_oos, dim=0)).numpy(), self.dim, places=5)

        t_orig = TT.revert(t_oos)
        self.assertAlmostEqual(torch.sum(torch.norm(t_orig - self.sample)).numpy(), 0, places=5)