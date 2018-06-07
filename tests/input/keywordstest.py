import math
import pypact as pp

from tests.testerbase import Tester


class KeywordsUnitTest(Tester):
    def test_control_keywords(self):
        self.assertTrue(len(pp.CONTROL_KEYWORDS) == 32)
        
        self.assertTrue('CNVTYPE' in pp.CONTROL_KEYWORDS)
        self.assertFalse('CMVTYPE' in pp.CONTROL_KEYWORDS)
        
        self.assertTrue('SPEK' in pp.CONTROL_KEYWORDS)
        self.assertFalse('SPEKK' in pp.CONTROL_KEYWORDS)
    
    def test_init_keywords(self):
        self.assertTrue(len(pp.INIT_KEYWORDS) == 64)
        
        self.assertTrue('ATOMS' in pp.INIT_KEYWORDS)
        self.assertFalse('ATOM' in pp.INIT_KEYWORDS)
        
        self.assertTrue('BREMSSTRAHLUNG' in pp.INIT_KEYWORDS)
        self.assertFalse('BREMSTRAHLUNG' in pp.INIT_KEYWORDS)
        
        self.assertTrue('TAB1' in pp.INIT_KEYWORDS)
        self.assertTrue('TAB2' in pp.INIT_KEYWORDS)
        self.assertTrue('TAB3' in pp.INIT_KEYWORDS)
        self.assertTrue('TAB4' in pp.INIT_KEYWORDS)
        self.assertFalse('TAB' in pp.INIT_KEYWORDS)
        self.assertFalse('TAB0' in pp.INIT_KEYWORDS)
        self.assertFalse('TAB5' in pp.INIT_KEYWORDS)

    def test_inventory_keywords(self):
        self.assertTrue(len(pp.INVENTORY_KEYWORDS) == 41)
        
        self.assertTrue('ATOMS' in pp.INVENTORY_KEYWORDS)
        self.assertFalse('ATOM' in pp.INVENTORY_KEYWORDS)
        
        self.assertFalse('BREMSSTRAHLUNG' in pp.INVENTORY_KEYWORDS)
        self.assertFalse('BREMSTRAHLUNG' in pp.INVENTORY_KEYWORDS)

        self.assertTrue('TAB1' in pp.INVENTORY_KEYWORDS)
        self.assertTrue('TAB2' in pp.INVENTORY_KEYWORDS)
        self.assertTrue('TAB3' in pp.INVENTORY_KEYWORDS)
        self.assertTrue('TAB4' in pp.INVENTORY_KEYWORDS)
        self.assertFalse('TAB' in pp.INVENTORY_KEYWORDS)
        self.assertFalse('TAB0' in pp.INVENTORY_KEYWORDS)
        self.assertFalse('TAB5' in pp.INVENTORY_KEYWORDS)
