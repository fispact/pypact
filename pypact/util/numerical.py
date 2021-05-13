nan = float("NaN")


def are_values_the_same(value1, value2, rel_tol, abs_tol=0.0):
    """
    Use math.isclose algorithm, it is better than numpy.isclose method.
    See https://github.com/numpy/numpy/issues/10161 for more on the discussion
    Since some python version don't come with math.isclose we implement it here directly
    """
    return abs(value1 - value2) <= max(rel_tol * max(abs(value1), abs(value2)), abs_tol)


def get_float(value):
    """
    Gets the floating point value from a string
    Will allow for fortran style floats, i.e -2.34321-308
    If it is neither then it will return "nan"
    """
    if _istradiationalfloat(value):
        return float(value)

    return _getfortranfloat(value)


def _istradiationalfloat(value):
    """
    Checks if the string can be converted to a floating point value
    Does not allow for fortran style floats, i.e -2.34321-308
    only standard floats.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_float(value):
    """
    Checks if the string can be converted to a floating point value
    Will allow for fortran style floats, i.e -2.34321-308
    If it is neither then it will return False
    """
    if isinstance(value, (int, float, str)):
        return _istradiationalfloat(value) or _isfortranfloat(value)
    return False


def _isfortranfloat(value):
    passfunc = lambda sign, esign, parts: True
    failfunc = lambda: False

    return _fortranfloat(value, passfunc, failfunc)


def _getfortranfloat(value):
    passfunc = lambda sign, esign, parts: float(
        sign + parts[0] + "E" + esign + parts[1]
    )
    failfunc = lambda: "nan"

    return _fortranfloat(value, passfunc, failfunc)


def _fortranfloat(value, passfunc, failfunc):
    # could be 2.3
    #          2.3e+10
    #          -2.3e+10
    #          -2.3+10
    #          -2.3-10
    #          2.3-10
    #          +2.3-10
    #          +2.3+10
    #          -2.3+10

    signs = ["-", "+"]

    valueasstring = str(value)
    sign = ""
    if valueasstring:
        # check for sign at the front
        if valueasstring[0] in signs:
            sign = valueasstring[0]
            valueasstring = valueasstring[1:]

        # cannot have both separators in the value for a valid float
        if not all(s in valueasstring for s in signs):
            # check the values in both parts recursively
            for sn in signs:
                if sn in valueasstring:
                    parts = valueasstring.split(sn, 1)
                    if (
                        _istradiationalfloat(parts[0])
                        and _istradiationalfloat(parts[1])
                        and "." in parts[0]
                        and not "." in parts[1]
                    ):
                        return passfunc(sign, sn, parts)
    return failfunc()
