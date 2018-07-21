class PypactException(Exception):
    pass

class PypactFrozenException(PypactException):
    pass

class PypactOutOfRangeException(PypactException):
    pass

class PypactSerializeException(PypactException):
    pass

class PypactDeserializeException(PypactException):
    pass

