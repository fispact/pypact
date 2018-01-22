
nan = float('NaN')


def getfloat(value):
    defaultreturn = lambda value: float(value)

    def func(parts, sign):
        if isfortranfloat(value):
            return float(parts[0] + 'E' + sign + parts[1])

        return defaultreturn(value)

    return _fortranfloat(value, func, defaultreturn)


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        # Fortran floats are a special case,
        # it allows floats of the form 2.65773-317
        # python doesn't recognise this as a float however
        # we must allow for this
        return isfortranfloat(value)


def isfortranfloat(value):
    defaultreturn = lambda value: False

    def func(parts, sign):
        # the decimal point must be in the first part
        # i.e. to the left of the decimal point
        if isfloat(parts[0]) \
                and isfloat(parts[1]) \
                and '.' in parts[0] \
                and '.' not in parts[1]:
            return True
        else:
            return defaultreturn(value)

    return _fortranfloat(value, func, defaultreturn)


def _fortranfloat(value, func, defaultreturn):
    # Fortran allows floats of the form 2.65773-317
    # as opposed to 2.65773E-317
    # python doesn't recognise this as a float however
    # we must allow for this
    separators = ['-', '+']

    # cannot have both separators in the value for a valid float
    if not all(s in value for s in separators):
        # check the values in both parts recursively
        for s in separators:
            if s in value:
                parts = value.split(s, 1)
                return func(parts, s)

    return defaultreturn(value)

