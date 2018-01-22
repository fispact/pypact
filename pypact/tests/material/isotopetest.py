from pypact.tests.testerbase import Tester
from pypact.material.isotope import Isotope


class IsoptopeAssertor(Tester):
    """
        Isotope unit test asserter
    """

    def assertIsotope(self, original, compare):
        self.assertEqual(True, isinstance(original, Isotope))
        self.assertEqual(True, isinstance(compare, Isotope))
        self.assertValueAndType(compare, Isotope, 'name', str, original.name)
        self.assertN(compare, original.n)
        self.assertZ(compare, original.z)
        self.assertEqual(original.a, compare.a)
        self.assertEqual(original.m, compare.m)

    def assertName(self, isotope, name):
        self.assertValueAndType(isotope, Isotope, 'name', str, name)

    def assertZ(self, isotope, z):
        self.assertValueAndType(isotope, Isotope, 'z', int, z)

    def assertN(self, isotope, n):
        self.assertValueAndType(isotope, Isotope, 'n', int, n)

    def assertA(self, isotope, a):
        self.assertValueAndType(isotope, Isotope, 'a', float, a)

    def assertM(self, isotope, m):
        self.assertValueAndType(isotope, Isotope, 'm', int, m)


class IsotopeUnitTest(IsoptopeAssertor):
    """
        Isotope unit tests
    """
    def test_createlithium6(self):
        isotope = Isotope("Lithium 6", 3, 6)

        self.assertName(isotope, "Lithium 6")
        self.assertN(isotope, 6)
        self.assertZ(isotope, 3)
        self.assertA(isotope, 0.0)
        self.assertM(isotope, 0)

    def test_createlithium6_withmass(self):
        isotope = Isotope("Lithium 6", 3, 6, 4.3)

        self.assertName(isotope, "Lithium 6")
        self.assertN(isotope, 6)
        self.assertZ(isotope, 3)
        self.assertA(isotope, 4.3)
        self.assertM(isotope, 0)

    def test_createlithium6_withmassandisomer(self):
        isotope = Isotope("Lithium 6", 3, 6, 4.3, 9)

        self.assertName(isotope, "Lithium 6")
        self.assertN(isotope, 6)
        self.assertZ(isotope, 3)
        self.assertA(isotope, 4.3)
        self.assertM(isotope, 9)
