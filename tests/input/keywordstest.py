import math
import pypact as pp

from tests.testerbase import Tester


class KeywordsUnitTest(Tester):
    def test_control_keywords(self):
        self.assertTrue(len(pp.control_keywords) == 32)
        
        self.assertTrue('CNVTYPE' in pp.control_keywords)
        self.assertFalse('CMVTYPE' in pp.control_keywords)
        
        self.assertTrue('SPEK' in pp.control_keywords)
        self.assertFalse('SPEKK' in pp.control_keywords)
    
    def test_init_keywords(self):
        self.assertTrue(len(pp.init_keywords) == 64)
        
        self.assertTrue('ATOMS' in pp.init_keywords)
        self.assertFalse('ATOM' in pp.init_keywords)
        
        self.assertTrue('BREMSSTRAHLUNG' in pp.init_keywords)
        self.assertFalse('BREMSTRAHLUNG' in pp.init_keywords)
        
        self.assertTrue('TAB1' in pp.init_keywords)
        self.assertTrue('TAB2' in pp.init_keywords)
        self.assertTrue('TAB3' in pp.init_keywords)
        self.assertTrue('TAB4' in pp.init_keywords)
        self.assertFalse('TAB' in pp.init_keywords)
        self.assertFalse('TAB0' in pp.init_keywords)
        self.assertFalse('TAB5' in pp.init_keywords)

    def test_inventory_keywords(self):
        self.assertTrue(len(pp.inventory_keywords) == 41)
        
        self.assertTrue('ATOMS' in pp.inventory_keywords)
        self.assertFalse('ATOM' in pp.inventory_keywords)
        
        self.assertFalse('BREMSSTRAHLUNG' in pp.inventory_keywords)
        self.assertFalse('BREMSTRAHLUNG' in pp.inventory_keywords)

        self.assertTrue('TAB1' in pp.inventory_keywords)
        self.assertTrue('TAB2' in pp.inventory_keywords)
        self.assertTrue('TAB3' in pp.inventory_keywords)
        self.assertTrue('TAB4' in pp.inventory_keywords)
        self.assertFalse('TAB' in pp.inventory_keywords)
        self.assertFalse('TAB0' in pp.inventory_keywords)
        self.assertFalse('TAB5' in pp.inventory_keywords)
