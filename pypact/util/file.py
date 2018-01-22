import os.path


# Returns the content of the file as a string
def content_as_str(filename):
    with open(filename, 'r') as file:
        data = file.readlines()

    return data


# Returns the content of the file as a string, and removes new lines.
def content_as_str_noreturn(filename):
    with open(filename, 'r') as file:
        data = file.read().replace('\n', '')

    return data


# checks if file exists
def file_exists(filename):
    return os.path.isfile(filename)


def get_filename_ext(filename):
    return os.path.basename(os.path.splitext(filename)[-1])


def str_in_file(filename, str):
    if file_exists(filename) and str in open(filename).read():
        return True
    else:
        return False


# note that regardless of the flag 'ignore_empty_lines' value, the last line is always ignored
def nr_of_lines(filename, ignore_empty_lines=False):
    if ignore_empty_lines:
        return len([i for i in open(filename) if i[:-1]])
    else:
        return len([i for i in open(filename)])
