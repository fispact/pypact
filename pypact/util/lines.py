from typing import List, Tuple, Optional
from pypact.util.numerical import is_float, get_float


def line_indices(lines: List[str], tag: str) -> List[int]:
    """

    :param lines: Must be a list of strings representing each line
    :param tag: is the tag to find in the list of lines
    :return: the indices of the lines with that tag

    """
    return [l for l in range(len(lines)) if tag in lines[l]]


def strings_from_line(line: str, linetag: str, ignoretags: Optional[List[str]] = None, endtag: str = '') -> List[str]:
    """

    :param line: The string representing a line
    :param linetag: The tag to find in the line
    :param ignoretags: The list of strings to ignore
    :param endtag: The tag of which to stop the string
    :return: A list of strings, without spaces or carriage returns, of string after the linetag

    """
    if ignoretags is None:
        ignoretags = []
    
    startindex = line.find(linetag)
    if startindex < 0:
        return []

    endindex = len(line)
    if endtag:
        endindex = line.find(endtag)
        if endindex < 0:
            endindex = len(line)

    strings = (line[startindex + len(linetag):endindex]).split()

    # trim
    for tag in ignoretags:
        if tag in strings:
            strings.remove(tag)

    return strings


def join_strings_from_line(line: str, linetag: str, ignoretags: Optional[List[str]] = None, endtag: str = '') -> str:
    """

    :param line: The string representing a line
    :param linetag: The tag to find in the line
    :param ignoretags: The list of strings to ignore
    :param endtag: The tag of which to stop the string
    :return: A single string joining all strings from the list

    """
    strings = strings_from_line(line, linetag, ignoretags, endtag)

    return ' '.join(strings)


def first_value_from_line(line: str, linetag: str, ignoretags: Optional[List[str]] = None) -> float:
    """

    :param line: The string representing a line
    :param linetag: The tag to find in the line
    :param ignoretags: The list of strings to ignore
    :return: The first value, float, after the tag. Returns NaN if no value found.

    """
    strings = strings_from_line(line, linetag, ignoretags)

    nan = 0.0
    if not strings:
        return nan

    for s in strings:
        # strip off any common tags around numbers
        s = s.replace(',', '').replace('*', '')
        if is_float(s):
            return get_float(s)

    return nan


def first_occurrence(lines: List[str], tag: str) -> Tuple[int, str]:
    """

    :param lines: A list of strings representing each line
    :param tag: is the tag to find in the list of lines
    :return: A tuple of the index and the line

    """
    return next_occurrence(lines, tag, 0)


def last_occurrence(lines: List[str], tag: str) -> Tuple[int, str]:
    """

    :param lines: A list of strings representing each line
    :param tag: is the tag to find in the list of lines
    :return: A tuple of the index and the line

    """
    lineindices = line_indices(lines, tag)
    if len(lineindices) > 0:
        index = lineindices[-1]
        line = lines[index]
        return index, line.strip()
    else:
        return -1, ''


def next_occurrence(lines: List[str], tag: str, startindex: int = 0) -> Tuple[int, str]:
    """

    :param lines: A list of strings representing each line
    :param tag: is the tag to find in the list of lines
    :return: A tuple of the index and the line

    """
    lineindices = line_indices(lines[startindex:], tag)
    if len(lineindices) > 0:
        index = lineindices[0]+startindex
        line = lines[index]
        return index, line.strip()
    else:
        return -1, ''

