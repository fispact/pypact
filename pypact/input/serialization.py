from io import StringIO


def to_string(obj):
    stream = StringIO()
    obj._serialize(stream)
    s = stream.getvalue()
    stream.close()
    return s


def to_file(obj, filename):
    """
    Serialize data to test file (files file)

    obj: must have serialize method
    filename: the name of the file to write
    """
    with open(filename, "w") as f:
        obj._serialize(f)


def from_file(obj, filename):
    """
    Deserialize data from file

    obj: must have deserialize and reset methods
    filename: the name of the file to read
    """
    obj.reset()
    with open(filename, "r") as f:
        obj._deserialize(f)
