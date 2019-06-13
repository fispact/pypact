class PypactException(Exception):
    pass

class PypactFrozenException(PypactException):
    pass

class PypactInvalidOptionException(PypactException):
    pass

class PypactIncompatibleOptionException(PypactException):
    pass

class PypactOutOfRangeException(PypactException):
    pass

class PypactSerializeException(PypactException):
    pass

class PypactDeserializeException(PypactException):
    pass

class PypactFispactExecutableNotFoundException(PypactException):
    pass

class PypactTypeException(PypactException):
    pass

class PypactUnphysicalValueException(PypactException):
    pass

class PypactNotPrintLib5FileException(PypactException):
    pass