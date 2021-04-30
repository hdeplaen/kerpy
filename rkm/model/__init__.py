"""
Source code for the RKM toolbox.

@author: HENRI DE PLAEN
@copyright: KU LEUVEN
@license: MIT
@date: March 2021
"""

class DualError(Exception):
    def __init__(self):
        self.message = "Dual representation not available."


class PrimalError(Exception):
    def __init__(self):
        self.message = "Primal representation not available. \
        The explicit representation lies in an infinite dimensional Hilbert space."


class RepresentationError(Exception):
    def __init__(self):
        self.message = "Unrecognized or unspecified representation (must be primal or dual)."

from .kernel import KernelFactory