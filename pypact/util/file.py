import os.path
from typing import List


def content_as_str(filename: str) -> List[str]:
    """Returns the content of the file as a list of strings (one per line)."""
    with open(filename, 'r') as file:
        data = file.readlines()

    return data


def content_as_str_noreturn(filename: str) -> str:
    """Returns the content of the file as a string, and removes new lines."""
    with open(filename, 'r') as file:
        data = file.read().replace('\n', '')

    return data


def file_exists(filename: str) -> bool:
    """Checks if file exists."""
    return os.path.isfile(filename)


def dir_exists(filename: str) -> bool:
    """Checks if directory exists."""
    return os.path.isdir(filename)


def file_remove(filename: str) -> None:
    """Removes file if it exists."""
    if file_exists(filename):
        os.remove(filename)


def get_filename_ext(filename: str) -> str:
    """Gets the file extension from filename."""
    return os.path.basename(os.path.splitext(filename)[-1])


def str_in_file(filename: str, string: str) -> bool:
    """Checks if a string exists in the file."""
    if file_exists(filename):
        with open(filename) as file:
            return string in file.read()

    return False


def nr_of_lines(filename: str, ignore_empty_lines: bool = False) -> int:
    """
    Returns the number of lines in a file.
    
    Note that regardless of the flag 'ignore_empty_lines' value,
    the last line is always ignored.
    """
    with open(filename) as file:
        if ignore_empty_lines:
            return len([i for i in file if i[:-1]])

        return len([i for i in file])
