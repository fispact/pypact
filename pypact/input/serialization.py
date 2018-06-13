
def serialize(obj, filename):
    """
        Serialize data to test file (files file)
        
        obj: must have serialize method
        filename: the name of the file to write
    """
    with open(filename, 'w') as f:
        obj._serialize(f)


def deserialize(obj, filename):
    """
        Deserialize data from file
        
        obj: must have deserialize and nullify methods
        filename: the name of the file to read
    """
    obj.nullify()
    with open(filename, 'r') as f:
        obj._deserialize(f)
