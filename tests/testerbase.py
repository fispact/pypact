import unittest
import math
import os

from pypact.util.numerical import are_values_the_same

REFERENCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', 'reference')

class Tester(unittest.TestCase):

    def assertValueAndType(self, obj, objtype, parameter, parametertype, value, rel_tol=0.0):
        self.assertEqual(True, isinstance(obj, objtype))
        if rel_tol == 0.0:
            self.assertEqual(getattr(obj, parameter), value)
        else:
            self.assertIsClose(getattr(obj, parameter), value, rel_tol)
        self.assertEqual(True, isinstance(getattr(obj, parameter), parametertype))

    def assertIsClose(self, a, b, rel_tol):
        self.assertTrue(are_values_the_same(a, b, rel_tol=rel_tol, abs_tol=0.0))

    @staticmethod
    def _isnotfound(value):
        return value == 0.0
