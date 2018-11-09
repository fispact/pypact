import math
import pypact as pp

from tests.testerbase import Tester


class FilesFileUnitTest(Tester):
    
    def test_default(self):
        ff = pp.FilesFile()
        self._assertDefaults(ff)

    def test_todict(self):
        ff = pp.FilesFile()
        self._assertDefaults(ff)
        
        # change default flux
        ff.fluxes = "flux1"
        
        # set some other paths
        ff.ind_nuc = "/path/to/ind_nuc"
        ff.enbins = "/path/to/enbins"
        
        d = ff.to_dict()
        # 4 defaults + 2 set above
        self.assertEqual(6, len(d), "Assert size of set paths")
        
        self.assertTrue('fluxes' in d, "Assert fluxes is set")
        self.assertTrue('xs_endf' not in d, "Assert xs_endf is not set")
        self.assertEqual("flux1", d['fluxes'], "Assert fluxes")
        self.assertEqual("flux1", ff.fluxes, "Assert fluxes")
        self.assertEqual("/path/to/ind_nuc", d['ind_nuc'], "Assert /path/to/ind_nuc")
        self.assertEqual("/path/to/ind_nuc", ff.ind_nuc, "Assert ind_nuc")
        self.assertEqual("/path/to/enbins", d['enbins'], "Assert /path/to/enbins")
        self.assertEqual("/path/to/enbins", ff.enbins, "Assert enbins")

    def test_reset(self):
        ff = pp.FilesFile()
        self._assertDefaults(ff)
        
        # change default flux
        ff.fluxes = "flux1"
        
        # set some other paths
        ff.ind_nuc = "/path/to/ind_nuc"
        ff.enbins = "/path/to/enbins"
        
        d = ff.to_dict()
        # 4 defaults + 2 set above
        self.assertEqual(6, len(d), "Assert size of set paths")
        
        self.assertTrue('fluxes' in d, "Assert fluxes is set")
        self.assertTrue('xs_endf' not in d, "Assert xs_endf is not set")
        self.assertEqual("flux1", d['fluxes'], "Assert fluxes")
        self.assertEqual("flux1", ff.fluxes, "Assert fluxes")
        self.assertEqual("/path/to/ind_nuc", d['ind_nuc'], "Assert /path/to/ind_nuc")
        self.assertEqual("/path/to/ind_nuc", ff.ind_nuc, "Assert ind_nuc")
        self.assertEqual("/path/to/enbins", d['enbins'], "Assert /path/to/enbins")
        self.assertEqual("/path/to/enbins", ff.enbins, "Assert enbins")
    
        ff.reset()
        d = ff.to_dict()
        self.assertEqual(0, len(d), "Assert size of set paths")
        self.assertEqual("null", ff.fluxes, "Assert fluxes")
        self.assertEqual("null", ff.collapxi, "Assert collapxi")
        self.assertEqual("null", ff.collapxo, "Assert collapxo")
        self.assertEqual("null", ff.arrayx, "Assert arrayx")
        self.assertEqual("null", ff.ind_nuc, "Assert ind_nuc")
        self.assertEqual("null", ff.xs_endf, "Assert xs_endf")
        self.assertEqual("null", ff.ggbins, "Assert ggbins")
    
    def test_writeread(self):
        ff = pp.FilesFile()
        self._assertDefaults(ff)
        
        # change default flux
        ff.fluxes = "flux1"
        
        # set some other paths
        ff.ind_nuc = "/path/to/ind_nuc"
        ff.enbins = "/path/to/enbins"
        
        d = ff.to_dict()
        # 4 defaults + 2 set above
        self.assertEqual(6, len(d), "Assert size of set paths")
        
        self.assertTrue('fluxes' in d, "Assert fluxes is set")
        self.assertTrue('xs_endf' not in d, "Assert xs_endf is not set")
        self.assertEqual("flux1", d['fluxes'], "Assert fluxes")
        self.assertEqual("flux1", ff.fluxes, "Assert fluxes")
        self.assertEqual("/path/to/ind_nuc", d['ind_nuc'], "Assert /path/to/ind_nuc")
        self.assertEqual("/path/to/ind_nuc", ff.ind_nuc, "Assert ind_nuc")
        self.assertEqual("/path/to/enbins", d['enbins'], "Assert /path/to/enbins")
        self.assertEqual("/path/to/enbins", ff.enbins, "Assert enbins")

        # write to file
        filename = '_PYPACT_TEST_writeread_files'
        pp.to_file(ff, filename)
        
        # reset
        ff.reset()
        d = ff.to_dict()
        self.assertEqual(0, len(d), "Assert size of set paths")
        self.assertEqual("null", ff.fluxes, "Assert fluxes")
        self.assertEqual("null", ff.collapxi, "Assert collapxi")
        self.assertEqual("null", ff.collapxo, "Assert collapxo")
        self.assertEqual("null", ff.arrayx, "Assert arrayx")
        self.assertEqual("null", ff.ind_nuc, "Assert ind_nuc")
        self.assertEqual("null", ff.xs_endf, "Assert xs_endf")
        self.assertEqual("null", ff.ggbins, "Assert ggbins")
        
        # read from file
        filename = '_PYPACT_TEST_writeread_files'
        pp.from_file(ff, filename)
        
        d = ff.to_dict()
        # 4 defaults + 2 set above
        self.assertEqual(6, len(d), "Assert size of set paths")
        
        self.assertTrue('fluxes' in d, "Assert fluxes is set")
        self.assertTrue('xs_endf' not in d, "Assert xs_endf is not set")
        self.assertEqual("flux1", d['fluxes'], "Assert fluxes")
        self.assertEqual("flux1", ff.fluxes, "Assert fluxes")
        self.assertEqual("/path/to/ind_nuc", d['ind_nuc'], "Assert /path/to/ind_nuc")
        self.assertEqual("/path/to/ind_nuc", ff.ind_nuc, "Assert ind_nuc")
        self.assertEqual("/path/to/enbins", d['enbins'], "Assert /path/to/enbins")
        self.assertEqual("/path/to/enbins", ff.enbins, "Assert enbins")

    def _assertDefaults(self, ff):
        # defaults
        self.assertEqual("fluxes", ff.fluxes, "Assert fluxes")
        self.assertEqual("COLLAPX", ff.collapxi, "Assert collapxi")
        self.assertEqual("COLLAPX", ff.collapxo, "Assert collapxo")
        self.assertEqual("ARRAYX", ff.arrayx, "Assert arrayx")
        self.assertEqual("null", ff.ind_nuc, "Assert ind_nuc")
        self.assertEqual("null", ff.xs_endf, "Assert xs_endf")
        self.assertEqual("null", ff.ggbins, "Assert ggbins")

