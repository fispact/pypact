class PypactException(Exception):
    pass

class PypactFrozenException(PypactException):
    pass

class PypactInvalidOptionException(Exception):
    pass

class PypactOutOfRangeException(PypactException):
    pass

class PypactSerializeException(PypactException):
    pass

class PypactDeserializeException(PypactException):
    pass

class PypactFispactExecutableNotFoundException(PypactException):
    pass
