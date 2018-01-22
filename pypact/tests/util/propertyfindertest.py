import os
from pypact.tests.testerbase import Tester
import pypact.util.propertyfinder as pf
from pypact.util.file import content_as_str


class PropertyFinderUnitTest(Tester):
    def setUp(self):
        self.base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../reference')
        self.filename_test91out = os.path.join(self.base_dir, "test91.out")
        self.file_as_string = content_as_str(self.filename_test91out)

        # DO NOT CHANGE THIS TEXT. IT IS USED FOR TESTING
        self.teststr = """This is a line.

        This is another line after a    space
        Here are some values 3.4, 88.93e7 and -0.83324e-5 with some text.  (738.9)


            Here are some \tmore values \t783.4 ** * 3248.93e7  !and -10.83324e+3 with some text.  (0.598e+6)

        blah blah 6 4 dajsl 2.3

         HEADER

         you see it here

         and here 4.615 * & 5.02e-4 tag 0.472e-8 ^55 fdjl

         HEADER

         you see it here

         and here 14.65 * & 5.032e-4 tag 0.4342e-3 ^545 fdjddl

         HEADER2

         you seedhfsdjkl it here

         and here 44.65 * & 52.02e-4 tag 0.342e-4 ^55 fdjl fds
        """.splitlines()

    def test_first(self):
        self.assertEqual(pf.first(self.teststr, 'This', '', asstring=True), 'This is a line.')
        self.assertTrue(self._isnotfound(pf.first(self.teststr, 'This', '', asstring=False)))
        self.assertEqual(pf.first(self.teststr, 'This', 'This', asstring=True), 'is a line.')
        self.assertTrue(self._isnotfound(pf.first(self.teststr, 'This', 'This', asstring=False)))
        self.assertEqual(pf.first(self.teststr, 'This', 'This is ', asstring=True), 'a line.')
        self.assertTrue(self._isnotfound(pf.first(self.teststr, 'This', 'This is ', asstring=False)))

        self.assertEqual(pf.first(self.teststr, 'This', 'Here', asstring=True),
                         'are some values 3.4, 88.93e7 and -0.83324e-5 with some text. (738.9)')
        self.assertEqual(pf.first(self.teststr, 'This', 'Here', asstring=False), 3.4)
        self.assertEqual(pf.first(self.teststr, 'This', 'Here', ignores=['3.4,'], asstring=False), 88.93e7)

    def test_from_file(self):
        # test some values from the output file
        self.assertEqual(pf.first(datadump=self.file_as_string,
                                  headertag='THIS RUN',
                                  starttag='timestamp:',
                                  endtag='',
                                  ignores=['\n', '|'],
                                  asstring=True), '12:35:22 13 January 2018')
        self.assertEqual(pf.last(datadump=self.file_as_string,
                                 headertag='THIS RUN',
                                 starttag='timestamp:',
                                 endtag='',
                                 ignores=['\n', '|'],
                                 asstring=True), '12:35:22 13 January 2018')

        self.assertEqual(pf.first(datadump=self.file_as_string,
                                  headertag='INITIAL CROSS SECTION DATA',
                                  starttag='FLUX file label:',
                                  endtag='',
                                  ignores=['\n', '|'],
                                  asstring=True), 'FBR-Na End of Cycle heavy fuel s')
        self.assertEqual(pf.last(datadump=self.file_as_string,
                                 headertag='INITIAL CROSS SECTION DATA',
                                 starttag='FLUX file label:',
                                 endtag='',
                                 ignores=['\n', '|'],
                                 asstring=True), 'FBR-Na End of Cycle heavy fuel s')

        self.assertEqual(pf.first(datadump=self.file_as_string,
                                  headertag='* * * TIME INTERVAL',
                                  starttag='TOTAL ACTIVITY EXCLUDING TRITIUM',
                                  endtag='',
                                  ignores=['\n', '|'],
                                  asstring=True), '1.45396E+07 Bq')
        self.assertEqual(pf.first(datadump=self.file_as_string,
                                  headertag='* * * TIME INTERVAL',
                                  starttag='TOTAL ACTIVITY EXCLUDING TRITIUM',
                                  endtag='Bq',
                                  ignores=['\n', '|'],
                                  asstring=True), '1.45396E+07')
        self.assertEqual(pf.first(datadump=self.file_as_string,
                                  headertag='* * * TIME INTERVAL',
                                  starttag='TOTAL ACTIVITY EXCLUDING TRITIUM',
                                  endtag='',
                                  ignores=['\n', '|'],
                                  asstring=False), 1.45396E+07)
        self.assertEqual(pf.first(datadump=self.file_as_string,
                                  headertag='* * * TIME INTERVAL',
                                  starttag='TOTAL ACTIVITY EXCLUDING TRITIUM',
                                  endtag='Bq',
                                  ignores=['\n', '|'],
                                  asstring=False), 1.45396E+07)

        self.assertEqual(pf.last(datadump=self.file_as_string,
                                 headertag='* * * TIME INTERVAL',
                                 starttag='TOTAL ACTIVITY EXCLUDING TRITIUM',
                                 endtag='',
                                 ignores=['\n', '|'],
                                 asstring=True), '4.11578E+07 Bq')
        self.assertEqual(pf.last(datadump=self.file_as_string,
                                 headertag='* * * TIME INTERVAL',
                                 starttag='TOTAL ACTIVITY EXCLUDING TRITIUM',
                                 endtag='Bq',
                                 ignores=['\n', '|'],
                                 asstring=True), '4.11578E+07')
        self.assertEqual(pf.last(datadump=self.file_as_string,
                                 headertag='* * * TIME INTERVAL',
                                 starttag='TOTAL ACTIVITY EXCLUDING TRITIUM',
                                 endtag='',
                                 ignores=['\n', '|'],
                                 asstring=False), 4.11578E+07)
        self.assertEqual(pf.last(datadump=self.file_as_string,
                                 headertag='* * * TIME INTERVAL',
                                 starttag='TOTAL ACTIVITY EXCLUDING TRITIUM',
                                 endtag='Bq',
                                 ignores=['\n', '|'],
                                 asstring=False), 4.11578E+07)

        self.assertEqual(pf.first(datadump=self.file_as_string,
                                  headertag='DOSE RATE (',
                                  starttag='IS',
                                  endtag='',
                                  ignores=[],
                                  asstring=True), '2.94608E-05 Sieverts/hour ( 2.94608E-03 Rems/hour)')
        self.assertEqual(pf.first(datadump=self.file_as_string,
                                  headertag='DOSE RATE (',
                                  starttag='IS',
                                  endtag='Sieverts/hour',
                                  ignores=[],
                                  asstring=True), '2.94608E-05')
        self.assertEqual(pf.first(datadump=self.file_as_string,
                                  headertag='DOSE RATE (',
                                  starttag='IS',
                                  endtag='Sieverts/hour',
                                  ignores=[],
                                  asstring=False), 2.94608E-05)
        self.assertEqual(pf.first(datadump=self.file_as_string,
                                  headertag='DOSE RATE (',
                                  starttag='IS',
                                  endtag='',
                                  ignores=[],
                                  asstring=False), 2.94608E-05)
        self.assertEqual(pf.first(datadump=self.file_as_string,
                                  headertag='DOSE RATE (',
                                  starttag='DOSE RATE (',
                                  endtag='',
                                  ignores=[],
                                  asstring=False), 2.94608E-05)
        self.assertEqual(pf.first(datadump=self.file_as_string,
                                  headertag='DOSE RATE (',
                                  starttag='DOSE RATE (',
                                  endtag='',
                                  ignores=['2.94608E-05'],
                                  asstring=False), 2.94608E-03)
