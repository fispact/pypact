from pypact.tests.testerbase import Tester
from pypact.material.element import Element
from pypact.material.isotope import Isotope
from pypact.material.knownelements import knownelements
from pypact.tests.material.isotopetest import IsoptopeAssertor


class ElementUnitTest(Tester):

    def test_createlithium(self):
        element = Element("Lithium", 'Li', 3, 6.941000)

        self.assertEqual(element.name, "Lithium")
        self.assertEqual(element.symbol, "Li")
        self.assertEqual(element.z, 3)
        self.assertEqual(element.aeff, 6.941000)

    def test_createlithiumfromknownelements(self):
        element = knownelements['Li']

        self.assertEqual(element.name, "Lithium")
        self.assertEqual(element.symbol, "Li")
        self.assertEqual(element.z, 3)
        self.assertEqual(element.aeff, 6.941000)

    def test_addisotope(self):

        isotopeassert = IsoptopeAssertor()

        element = Element("Lithium", 'Li', 3, 6.941000)

        element.addisotope(Isotope("Lithium 6", 3, 6), 0.9)
        self.assertEqual(element.isotopes[0][1], 0.9)
        isotopeassert.assertIsotope(element.isotopes[0][0], Isotope("Lithium 6", 3, 6))

        element.addisotope(Isotope("Lithium 7", 3, 7), 0.1)
        self.assertEqual(element.isotopes[1][1], 0.1)
        isotopeassert.assertIsotope(element.isotopes[1][0], Isotope("Lithium 7", 3, 7))
