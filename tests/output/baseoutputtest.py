import os
import pypact as pp

from tests.testerbase import Tester, REFERENCE_DIR


class BaseOutputUnitTest(Tester):
    def setUp(self):
        self.base_dir = os.path.join(REFERENCE_DIR)
        self.filename_test91out = os.path.join(self.base_dir, "test91.out")
        self.filename_test91json = os.path.join(self.base_dir, "test91.json")
        self.filerecord91 = pp.FileRecord(self.filename_test91out)
        self.jsonoutput91 = pp.Output()
        self.jsonoutput91.json_deserialize(open(self.filename_test91json).read())
        
        self.filename_test31out = os.path.join(self.base_dir, "test31.out")
        self.filename_test31json = os.path.join(self.base_dir, "test31.json")
        self.filerecord31 = pp.FileRecord(self.filename_test31out)
        self.jsonoutput31 = pp.Output()
        self.jsonoutput31.json_deserialize(open(self.filename_test31json).read())
