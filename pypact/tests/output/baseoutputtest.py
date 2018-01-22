import os
from pypact.reader.filerecord import FileRecord
from pypact.tests.testerbase import Tester


class BaseOutputUnitTest(Tester):
    def setUp(self):
        self.base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../reference')
        self.filename_test91out = os.path.join(self.base_dir, "test91.out")
        self.filerecord91 = FileRecord(self.filename_test91out)
        self.filename_test31out = os.path.join(self.base_dir, "test31.out")
        self.filerecord31 = FileRecord(self.filename_test31out)
