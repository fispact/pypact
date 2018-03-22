import unittest

from pypact.library.nuclidelib import findZ, findisotopes, findelement


class NuclideLibUnitTest(unittest.TestCase):
    def setUp(self):
        self.testz = [('H', 1),
                      ('He', 2),
                      ('Fe', 26),
                      ('Co', 27),
                      ('Pd', 46),
                      ('U', 92),
                      ('Pa', 91),
                      ('Ds', 110)
                      ]

        self.testisotopes = [('H', list(range(1,8,1))),
                             ('He', list(range(3,11,1))),
                             ('Fe', list(range(45,75,1))),
                             ('Co', list(range(47,77,1))),
                             ('Pd', list(range(91,129,1))),
                             ('U', list(range(217,244,1))),
                             ('Pa', list(range(212,242,1))),
                             ('Ds', list(range(267,282,1)))
                              ]

    def test_findZ(self):
        for e, z in self.testz:
            self.assertEqual(findZ(e), z, "Assert {0} has Z={1}".format(e, z))

    def test_findElement(self):
        for e, z in self.testz:
            self.assertEqual(findelement(z), e, "Assert {0} has Z={1}".format(e, z))

    def test_findZElementCombined(self):
        """
            Test that inversefunction(x).function(x) = x 
        """
        for e, z in self.testz:
            self.assertEqual(findZ(findelement(z)), z, "Assert {0} has Z={1}".format(e, z))
            self.assertEqual(findelement(findZ(e)), e, "Assert {0} has Z={1}".format(e, z))

    def test_findisotopes(self):
        for e, isotopes in self.testisotopes:
            self.assertEqual(findisotopes(e), isotopes,
                             "Assert {0} has isotopes={1}".format(e, isotopes))
