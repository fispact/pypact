import unittest

from pypact.library.projectiles import *
from pypact.library.reactionlib import *


class ReactionLibUnitTest(unittest.TestCase):

    def test_getreaction(self):
        self.assertEqual(getreaction(204), '(n,Xd   )', 
            "Assert mt=204")
        self.assertEqual(getreaction(1, proj=PROJECTILE_NEUTRON), '(n,total)', 
            "Assert mt=1")
        self.assertEqual(getreaction(199, proj=PROJECTILE_ALPHA), '(a,3n2pa)', 
            "Assert mt=199")
        self.assertEqual(getreaction(102, proj=PROJECTILE_DEUTERON), '(d,g    )', 
            "Assert mt=102")
        self.assertEqual(getreaction(102, proj=PROJECTILE_GAMMA), '(g,g    )', 
            "Assert mt=102")
        self.assertEqual(getreaction(3, proj=PROJECTILE_GAMMA), '(g,nonel)', 
            "Assert mt=3")
        self.assertEqual(getreaction(446, proj=PROJECTILE_GAMMA), '(g,Dinel)', 
            "Assert mt=446")
        self.assertEqual(getreaction(301, proj=PROJECTILE_PROTON), '(p,Ktot )', 
            "Assert mt=301")

    def test_getmtreaction(self):
        for k, v in REACTION_DICTIONARY.items():
            self.assertEqual(k, getmt(getreaction(k), fullstring=True), 
                "Asset MT={}".format(k))

    def test_getreactionmt(self):
        for proj in VALID_PROJECTILES:
            for k, v in REACTION_DICTIONARY.items():
                self.assertEqual("({},{:5})".format(get_projectile_symbol(proj), v), 
                    getreaction(getmt(v.strip(), fullstring=False), proj=proj), 
                    "Asset MT={}".format(k))