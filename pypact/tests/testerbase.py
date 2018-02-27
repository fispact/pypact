import unittest
import math
import os

REFERENCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', '..', 'reference')

class Tester(unittest.TestCase):

    def assertValueAndType(self, obj, objtype, parameter, parametertype, value, rel_tol=0.0):
        self.assertEqual(True, isinstance(obj, objtype))
        if rel_tol == 0.0:
            self.assertEqual(getattr(obj, parameter), value)
        else:
            self.assertIsClose(getattr(obj, parameter), value, rel_tol)
        self.assertEqual(True, isinstance(getattr(obj, parameter), parametertype))

    def assertIsClose(self, a, b, rel_tol):
        if math.isnan(a):
            self.assertEquals(b, 0.0)
            return
        if math.isnan(b):
            self.assertEquals(a, 0.0)
            return

        # for when it is not close failure message is not useful
        # hence why we do the actual assert equals if not within tolerance
        # this shows the two values
        if math.isclose(a, b, rel_tol=rel_tol, abs_tol=0.0):
            self.assertTrue(math.isclose(a, b, rel_tol=rel_tol, abs_tol=0.0))
        else:
            self.assertEquals(a, b)

    @staticmethod
    def _isnotfound(value):
        return value == 0.0
