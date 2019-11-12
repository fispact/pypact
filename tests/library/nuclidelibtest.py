import unittest

from pypact.library.nuclidelib import NUCLIDE_DICTIONARY, STATE_MAPPINGS, \
    find_z, find_isotopes, find_element, \
    get_zai, get_name, get_zai_props


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

    def test_getzai(self):
        self.assertEqual(10010, get_zai("H1"), "Assert zai for H1")
        self.assertEqual(10021, get_zai("H2m"), "Assert zai for H2m")
        self.assertEqual(922383, get_zai("U238o"), "Assert zai for U238o")
        self.assertEqual(270660, get_zai("Co66"), "Assert zai for Co66")
        self.assertEqual(1182139, get_zai("Og213u"), "Assert zai for Og233u")

    def test_getzaiprops(self):
        self.assertEqual((1, 1, 0), get_zai_props(10010), "Assert zai for H1")
        self.assertEqual((1, 2, 1), get_zai_props(10021), "Assert zai for H2m")
        self.assertEqual((92, 238, 3), get_zai_props(922383), "Assert zai for U238o")
        self.assertEqual((27, 66, 0), get_zai_props(270660), "Assert zai for Co66")
        self.assertEqual((118, 213, 9), get_zai_props(1182139), "Assert zai for Og233u")

    def test_getname(self):
        self.assertEqual("Cr87m", get_name(240871), "Assert zai for Cr87m")
        self.assertEqual("La145", get_name(571450), "Assert zai for La145")
        self.assertEqual("Ar198o", get_name(181983), "Assert zai for Ar198o")
        self.assertEqual("Ar198p", get_name(181984), "Assert zai for Ar198p")
        self.assertEqual("Og233u", get_name(1182339), "Assert zai for Og233u")
        self.assertEqual("Og233", get_name(1182330), "Assert zai for Og233")

    def test_getnamezai(self):
        for element in NUCLIDE_DICTIONARY:
            for A in element['isotopes']:
                for i, s in STATE_MAPPINGS.items():
                    zai = element['Z']*10000 + A*10 + i
                    name = "{}{}{}".format(element['element'], A, s)
                    self.assertEqual(zai, get_zai(get_name(zai)), "Assert zai for {}".format(zai))
                    self.assertEqual(name, get_name(get_zai(name)), "Assert name for {}".format(name))