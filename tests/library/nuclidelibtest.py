import unittest

from pypact.library.nuclidelib import find_z, find_isotopes, find_element


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

    def test_find_z(self):
        for e, z in self.testz:
            self.assertEqual(find_z(e), z, "Assert {0} has Z={1}".format(e, z))

    def test_find_element(self):
        for e, z in self.testz:
            self.assertEqual(find_element(z), e, "Assert {0} has Z={1}".format(e, z))

    def test_find_z_element_combined(self):
        """
            Test that inversefunction(x).function(x) = x 
        """
        for e, z in self.testz:
            self.assertEqual(find_z(find_element(z)), z, "Assert {0} has Z={1}".format(e, z))
            self.assertEqual(find_element(find_z(e)), e, "Assert {0} has Z={1}".format(e, z))

    def test_find_isotopes(self):
        for e, isotopes in self.testisotopes:
            self.assertEqual(find_isotopes(e), isotopes,
                             "Assert {0} has isotopes={1}".format(e, isotopes))
