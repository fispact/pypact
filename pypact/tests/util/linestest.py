import os
from pypact.tests.testerbase import Tester, REFERENCE_DIR
import pypact.util.lines as lines
from pypact.util.file import content_as_str


class LinesUnitTest(Tester):
    def setUp(self):
        self.base_dir = os.path.join(REFERENCE_DIR)
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

    def test_line_indices(self):
        self.assertEqual(lines.line_indices(self.teststr, 'This'), [0, 2])
        self.assertEqual(lines.line_indices(self.teststr, 'another'), [2])
        self.assertEqual(lines.line_indices(self.teststr, 'This is a line'), [0])
        self.assertEqual(lines.line_indices(self.teststr, 'This is a lines'), [])
        self.assertEqual(lines.line_indices(self.teststr, 'This is another line after a space'), [])
        self.assertEqual(lines.line_indices(self.teststr, 'This is another line after a    space'), [2])
        self.assertEqual(lines.line_indices(self.teststr, 'blah'), [8])
        self.assertEqual(lines.line_indices(self.teststr, 'blah blah'), [8])
        self.assertEqual(lines.line_indices(self.teststr, '6'), [6, 8, 14, 20, 26])
        self.assertEqual(lines.line_indices(self.teststr, '3'), [3, 6, 8, 20, 26])
        self.assertEqual(lines.line_indices(self.teststr, '738.9'), [3])
        self.assertEqual(lines.line_indices(self.teststr, '(738.9)'), [3])
        self.assertEqual(lines.line_indices(self.teststr, ' (738.9)'), [3])
        self.assertEqual(lines.line_indices(self.teststr, ' (738.9)'), [3])
        self.assertEqual(lines.line_indices(self.teststr, ' (738.9) '), [])
        self.assertEqual(lines.line_indices(self.teststr, '!'), [6])
        self.assertEqual(lines.line_indices(self.teststr, ' !'), [6])
        self.assertEqual(lines.line_indices(self.teststr, ' !and'), [6])
        self.assertEqual(lines.line_indices(self.teststr, ' ! '), [])
        self.assertEqual(lines.line_indices(self.teststr, ' some text '), [])
        self.assertEqual(lines.line_indices(self.teststr, ' some text. '), [3, 6])
        self.assertEqual(lines.line_indices(self.teststr, 'HEADER'), [10, 16, 22])
        self.assertEqual(lines.line_indices(self.teststr, 'HEADER2'), [22])
        self.assertEqual(lines.line_indices(self.teststr, ' '), [0,2,3,6,8,10,12,14,16,18,20,22,24,26,27])
        self.assertEqual(lines.line_indices(self.teststr, '\n'), [])

    def test_string_from_line(self):
        self.assertEqual(
            lines.strings_from_line(self.teststr[0], 'This'), ['is', 'a', 'line.'])
        self.assertEqual(
            lines.strings_from_line(self.teststr[0], 'is'), ['is', 'a', 'line.'])
        self.assertEqual(
            lines.strings_from_line(self.teststr[0], 'a'), ['line.'])
        self.assertEqual(
            lines.strings_from_line(self.teststr[1], 'This'), [])
        self.assertEqual(
            lines.strings_from_line(self.teststr[2], 'This'), ['is', 'another', 'line', 'after', 'a', 'space'])
        self.assertEqual(
            lines.strings_from_line(self.teststr[3], 'This'), [])
        self.assertEqual(
            lines.strings_from_line(self.teststr[16], 'HEADER'), [])
        self.assertEqual(
            lines.strings_from_line(self.teststr[22], 'HEADER'), ['2'])
        self.assertEqual(
            lines.strings_from_line(self.teststr[22], 'HEADER2'), [])
        self.assertEqual(
            lines.strings_from_line(self.teststr[26], 'tag'), ['0.342e-4', '^55', 'fdjl', 'fds'])
        self.assertEqual(
            lines.strings_from_line(self.teststr[26], 'tag', ignoretags=['^']), ['0.342e-4', '^55', 'fdjl', 'fds'])
        self.assertEqual(
            lines.strings_from_line(self.teststr[26], 'tag', ignoretags=['^55']), ['0.342e-4', 'fdjl', 'fds'])
        self.assertEqual(
            lines.strings_from_line(self.teststr[26], 'tag', ignoretags=['^55', 'djl']), ['0.342e-4', 'fdjl', 'fds'])
        self.assertEqual(
            lines.strings_from_line(self.teststr[26], 'tag', ignoretags=['^55', 'fdjl']), ['0.342e-4', 'fds'])

        self.assertEqual(lines.strings_from_line(self.file_as_string[83], 'TOTAL ACTIVITY EXCLUDING TRITIUM'),
                         ['1.45396E+07', 'Bq'])

    def test_join_strings_from_line(self):
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[0], 'This'), 'is a line.')
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[0], 'is'), 'is a line.')
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[0], 'a'), 'line.')
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[1], 'This'), '')
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[2], 'This'), 'is another line after a space')
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[2], 'This', endtag='a space'), 'is another line after a space')
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[2], 'This', endtag='space'), 'is another line after a')
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[2], 'This', endtag='another'), 'is')
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[3], 'This'), '')
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[16], 'HEADER'), '')
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[22], 'HEADER'), '2')
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[22], 'HEADER2'), '')
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[26], 'tag'), '0.342e-4 ^55 fdjl fds')
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[26], 'tag', ignoretags=['^']), '0.342e-4 ^55 fdjl fds')
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[26], 'tag', ignoretags=['^55']), '0.342e-4 fdjl fds')
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[26], 'tag', ignoretags=['^55', 'djl']), '0.342e-4 fdjl fds')
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[26], 'tag', ignoretags=['^55', 'fdjl']), '0.342e-4 fds')
        self.assertEqual(
            lines.join_strings_from_line(self.teststr[26], 'tag', ignoretags=['^55', 'fdjl'], endtag='fds'), '0.342e-4')

    def test_first_value_from_line(self):
        self.assertTrue(
            self._isnotfound(lines.first_value_from_line(self.teststr[0], 'This')))
        self.assertTrue(
            self._isnotfound(lines.first_value_from_line(self.teststr[0], 'is')))
        self.assertTrue(
            self._isnotfound(lines.first_value_from_line(self.teststr[0], 'a')))
        self.assertTrue(
            self._isnotfound(lines.first_value_from_line(self.teststr[1], 'This')))
        self.assertTrue(
            self._isnotfound(lines.first_value_from_line(self.teststr[2], 'This')))
        self.assertTrue(
            self._isnotfound(lines.first_value_from_line(self.teststr[3], 'This')))
        self.assertEqual(
            lines.first_value_from_line(self.teststr[6], 'Here'), 783.4)
        self.assertEqual(
            lines.first_value_from_line(self.teststr[6], '**'), 3248.93e7)
        self.assertEqual(
            lines.first_value_from_line(self.teststr[6], '** *'), 3248.93e7)
        self.assertEqual(
            lines.first_value_from_line(self.teststr[6], '*'), 3248.93e7)
        self.assertEqual(
            lines.first_value_from_line(self.teststr[6], ' *'), 3248.93e7)
        self.assertEqual(
            lines.first_value_from_line(self.teststr[6], ' *', ignoretags=['3248.93e7']), -10.83324e+3)
        self.assertEqual(
            lines.first_value_from_line(self.teststr[6], '3248.93e7'), -10.83324e+3)
        self.assertEqual(
            lines.first_value_from_line(self.teststr[6], '!'), -10.83324e+3)
        self.assertEqual(
            lines.first_value_from_line(self.teststr[6], '!and'), -10.83324e+3)
        self.assertTrue(
            self._isnotfound(lines.first_value_from_line(self.teststr[16], 'HEADER')))
        self.assertTrue(
            self._isnotfound(lines.first_value_from_line(self.teststr[22], 'HEADER2')))
        self.assertEqual(
            lines.first_value_from_line(self.teststr[22], 'HEADER'), 2)
        self.assertEqual(
            lines.first_value_from_line(self.teststr[26], 'tag'), 0.342e-4)
        self.assertEqual(
            lines.first_value_from_line(self.teststr[26], 'tag', ignoretags=['^']), 0.342e-4)
        self.assertEqual(
            lines.first_value_from_line(self.teststr[26], 'tag', ignoretags=['^55']), 0.342e-4)
        self.assertTrue(
            self._isnotfound(lines.first_value_from_line(self.teststr[26], 'tag', ignoretags=['0.342e-4', '^55', 'djl'])))
        self.assertEqual(
            lines.first_value_from_line(self.teststr[26], 'tag', ignoretags=['^55', 'fdjl']), 0.342e-4)

    def test_first_occurrence(self):
        notfound = (-1, '')
        self.assertEqual(lines.first_occurrence(self.teststr, 'This'),
                         (0, 'This is a line.'))
        self.assertEqual(lines.first_occurrence(self.teststr, 'another'),
                         (2, 'This is another line after a    space'))
        self.assertEqual(lines.first_occurrence(self.teststr, 'This is a line'),
                         (0, 'This is a line.'))
        self.assertEqual(lines.first_occurrence(self.teststr, 'This is a lines'),
                         notfound)
        self.assertEqual(lines.first_occurrence(self.teststr, 'This is another line after a space'),
                         notfound)
        self.assertEqual(lines.first_occurrence(self.teststr, 'This is another line after a    space'),
                         (2, 'This is another line after a    space'))
        self.assertEqual(lines.first_occurrence(self.teststr, 'blah'),
                         (8, 'blah blah 6 4 dajsl 2.3'))
        self.assertEqual(lines.first_occurrence(self.teststr, 'blah blah'),
                         (8, 'blah blah 6 4 dajsl 2.3'))
        self.assertEqual(lines.first_occurrence(self.teststr, '6'),
                         (6, 'Here are some \tmore values \t783.4 ** * 3248.93e7  !and -10.83324e+3 with some text.  (0.598e+6)'))
        self.assertEqual(lines.first_occurrence(self.teststr, '3'),
                         (3, 'Here are some values 3.4, 88.93e7 and -0.83324e-5 with some text.  (738.9)'))
        self.assertEqual(lines.first_occurrence(self.teststr, '738.9'),
                         (3, 'Here are some values 3.4, 88.93e7 and -0.83324e-5 with some text.  (738.9)'))
        self.assertEqual(lines.first_occurrence(self.teststr, '(738.9)'),
                         (3, 'Here are some values 3.4, 88.93e7 and -0.83324e-5 with some text.  (738.9)'))
        self.assertEqual(lines.first_occurrence(self.teststr, ' (738.9)'),
                         (3, 'Here are some values 3.4, 88.93e7 and -0.83324e-5 with some text.  (738.9)'))
        self.assertEqual(lines.first_occurrence(self.teststr, ' (738.9)'),
                         (3, 'Here are some values 3.4, 88.93e7 and -0.83324e-5 with some text.  (738.9)'))
        self.assertEqual(lines.first_occurrence(self.teststr, ' (738.9) '),
                         notfound)
        self.assertEqual(lines.first_occurrence(self.teststr, '!'),
                         (6, 'Here are some \tmore values \t783.4 ** * 3248.93e7  !and -10.83324e+3 with some text.  (0.598e+6)'))
        self.assertEqual(lines.first_occurrence(self.teststr, ' !'),
                         (6, 'Here are some \tmore values \t783.4 ** * 3248.93e7  !and -10.83324e+3 with some text.  (0.598e+6)'))
        self.assertEqual(lines.first_occurrence(self.teststr, ' !and'),
                         (6,'Here are some \tmore values \t783.4 ** * 3248.93e7  !and -10.83324e+3 with some text.  (0.598e+6)'))
        self.assertEqual(lines.first_occurrence(self.teststr, ' ! '),
                         notfound)
        self.assertEqual(lines.first_occurrence(self.teststr, ' some text '),
                         notfound)
        self.assertEqual(lines.first_occurrence(self.teststr, ' some text. '),
                         (3, 'Here are some values 3.4, 88.93e7 and -0.83324e-5 with some text.  (738.9)'))
        self.assertEqual(lines.first_occurrence(self.teststr, 'HEADER'),
                         (10, 'HEADER'))
        self.assertEqual(lines.first_occurrence(self.teststr, 'HEADER2'),
                         (22, 'HEADER2'))
        self.assertEqual(lines.first_occurrence(self.teststr, ' '),
                         (0, 'This is a line.'))
        self.assertEqual(lines.first_occurrence(self.teststr, '\n'),
                         notfound)

        self.assertEqual(lines.first_occurrence(self.file_as_string, 'TOTAL ACTIVITY EXCLUDING TRITIUM'),
                         (83, 'TOTAL ACTIVITY EXCLUDING TRITIUM     1.45396E+07 Bq'))

    def test_last_occurrence(self):
        notfound = (-1, '')
        self.assertEqual(lines.last_occurrence(self.teststr, 'This'),
                         (2, 'This is another line after a    space'))
        self.assertEqual(lines.last_occurrence(self.teststr, 'another'),
                         (2, 'This is another line after a    space'))
        self.assertEqual(lines.last_occurrence(self.teststr, 'This is a line'),
                         (0, 'This is a line.'))
        self.assertEqual(lines.last_occurrence(self.teststr, 'This is a lines'),
                         notfound)
        self.assertEqual(lines.last_occurrence(self.teststr, 'This is another line after a space'),
                         notfound)
        self.assertEqual(lines.last_occurrence(self.teststr, 'This is another line after a    space'),
                         (2, 'This is another line after a    space'))
        self.assertEqual(lines.last_occurrence(self.teststr, 'blah'),
                         (8, 'blah blah 6 4 dajsl 2.3'))
        self.assertEqual(lines.last_occurrence(self.teststr, 'blah blah'),
                         (8, 'blah blah 6 4 dajsl 2.3'))
        self.assertEqual(lines.last_occurrence(self.teststr, '6'),
                         (26, 'and here 44.65 * & 52.02e-4 tag 0.342e-4 ^55 fdjl fds'))
        self.assertEqual(lines.last_occurrence(self.teststr, '3'),
                         (26, 'and here 44.65 * & 52.02e-4 tag 0.342e-4 ^55 fdjl fds'))
        self.assertEqual(lines.last_occurrence(self.teststr, '738.9'),
                         (3, 'Here are some values 3.4, 88.93e7 and -0.83324e-5 with some text.  (738.9)'))
        self.assertEqual(lines.last_occurrence(self.teststr, '(738.9)'),
                         (3, 'Here are some values 3.4, 88.93e7 and -0.83324e-5 with some text.  (738.9)'))
        self.assertEqual(lines.last_occurrence(self.teststr, ' (738.9)'),
                         (3, 'Here are some values 3.4, 88.93e7 and -0.83324e-5 with some text.  (738.9)'))
        self.assertEqual(lines.last_occurrence(self.teststr, ' (738.9)'),
                         (3, 'Here are some values 3.4, 88.93e7 and -0.83324e-5 with some text.  (738.9)'))
        self.assertEqual(lines.last_occurrence(self.teststr, ' (738.9) '),
                         notfound)
        self.assertEqual(lines.last_occurrence(self.teststr, '!'),
                         (6,
                          'Here are some \tmore values \t783.4 ** * 3248.93e7  !and -10.83324e+3 with some text.  (0.598e+6)'))
        self.assertEqual(lines.last_occurrence(self.teststr, ' !'),
                         (6,
                          'Here are some \tmore values \t783.4 ** * 3248.93e7  !and -10.83324e+3 with some text.  (0.598e+6)'))
        self.assertEqual(lines.last_occurrence(self.teststr, ' !and'),
                         (6,
                          'Here are some \tmore values \t783.4 ** * 3248.93e7  !and -10.83324e+3 with some text.  (0.598e+6)'))
        self.assertEqual(lines.last_occurrence(self.teststr, ' ! '),
                         notfound)
        self.assertEqual(lines.last_occurrence(self.teststr, ' some text '),
                         notfound)
        self.assertEqual(lines.last_occurrence(self.teststr, ' some text. '),
                         (6, 'Here are some \tmore values \t783.4 ** * 3248.93e7  !and -10.83324e+3 with some text.  (0.598e+6)'))
        self.assertEqual(lines.last_occurrence(self.teststr, 'HEADER'),
                         (22, 'HEADER2'))
        self.assertEqual(lines.last_occurrence(self.teststr, 'HEADER2'),
                         (22, 'HEADER2'))
        self.assertEqual(lines.last_occurrence(self.teststr, ' '),
                         (27, ''))
        self.assertEqual(lines.last_occurrence(self.teststr, '\n'),
                         notfound)

    def test_next_occurrence(self):
        notfound = (-1, '')
        self.assertEqual(lines.next_occurrence(self.teststr, 'HEADER', 10),
                         (10, 'HEADER'))
        self.assertEqual(lines.next_occurrence(self.teststr, 'HEADER', 11),
                         (16, 'HEADER'))
        self.assertEqual(lines.next_occurrence(self.teststr, 'HEADER', 16),
                         (16, 'HEADER'))
        self.assertEqual(lines.next_occurrence(self.teststr, 'HEADER', 17),
                         (22, 'HEADER2'))
        self.assertEqual(lines.next_occurrence(self.teststr, 'HEADER', 22),
                         (22, 'HEADER2'))
        self.assertEqual(lines.next_occurrence(self.teststr, 'HEADER2', 22),
                         (22, 'HEADER2'))
        self.assertEqual(lines.next_occurrence(self.teststr, 'HEADER2', 0),
                         (22, 'HEADER2'))
        self.assertEqual(lines.next_occurrence(self.teststr, 'HEADER2', 23),
                         notfound)
        self.assertEqual(lines.next_occurrence(self.teststr, '3'),
                         (3, 'Here are some values 3.4, 88.93e7 and -0.83324e-5 with some text.  (738.9)'))
        self.assertEqual(lines.next_occurrence(self.teststr, '3', 1),
                         (3, 'Here are some values 3.4, 88.93e7 and -0.83324e-5 with some text.  (738.9)'))
        self.assertEqual(lines.next_occurrence(self.teststr, '3', 3),
                         (3, 'Here are some values 3.4, 88.93e7 and -0.83324e-5 with some text.  (738.9)'))
        self.assertEqual(lines.next_occurrence(self.teststr, '3', 4),
                         (6, 'Here are some \tmore values \t783.4 ** * 3248.93e7  !and -10.83324e+3 with some text.  (0.598e+6)'))
