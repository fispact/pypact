import pypact as pp

from tests.testerbase import Tester


class ProjectilesUnitTest(Tester):

    def test_get_projectile_name(self):
        self.assertEqual('neutron', pp.get_projectile_name(pp.PROJECTILE_NEUTRON), "Assert neutron name")
        self.assertEqual('proton', pp.get_projectile_name(pp.PROJECTILE_PROTON), "Assert proton name")
        self.assertEqual('deuteron', pp.get_projectile_name(pp.PROJECTILE_DEUTERON), "Assert deuteron name")
        self.assertEqual('alpha', pp.get_projectile_name(pp.PROJECTILE_ALPHA), "Assert alpha name")
        self.assertEqual('gamma', pp.get_projectile_name(pp.PROJECTILE_GAMMA), "Assert gamma name")

    def test_get_projectile_symbol(self):
        self.assertEqual('n', pp.get_projectile_symbol(pp.PROJECTILE_NEUTRON), "Assert neutron symbol")
        self.assertEqual('p', pp.get_projectile_symbol(pp.PROJECTILE_PROTON), "Assert proton symbol")
        self.assertEqual('d', pp.get_projectile_symbol(pp.PROJECTILE_DEUTERON), "Assert deuteron symbol")
        self.assertEqual('a', pp.get_projectile_symbol(pp.PROJECTILE_ALPHA), "Assert alpha symbol")
        self.assertEqual('g', pp.get_projectile_symbol(pp.PROJECTILE_GAMMA), "Assert gamma symbol")

    def test_get_projectile_value(self):
        self.assertEqual(pp.PROJECTILE_NEUTRON, pp.get_projectile_value('neutron'), "Assert neutron value")
        self.assertEqual(pp.PROJECTILE_PROTON, pp.get_projectile_value('proton'), "Assert proton value")
        self.assertEqual(pp.PROJECTILE_DEUTERON, pp.get_projectile_value('deuteron'), "Assert deuteron value")
        self.assertEqual(pp.PROJECTILE_ALPHA, pp.get_projectile_value('alpha'), "Assert alpha value")
        self.assertEqual(pp.PROJECTILE_GAMMA, pp.get_projectile_value('gamma'), "Assert gamma value")
