from pypact.util.lines import *


def get(datadump, headertag, starttag, endtag='', findfirst=True, ignores=[], asstring=True):
    """
    Get the first occurrence of the linetag within the first headertag.

    Parameters
    ----------
    datadump : str
        Full output string dump
    headertag : str
        The string tag to indicate the property is below this header tag
    starttag : str
        The string tag to indicate the property is after this tag on the line
    endtag : str
        The string tag to indicate the property is before this tag on the line (optional)
    findfirst : bool
        The flag to indicate if the first or last occurrence should be used
    ignores : list[str]
        List of strings to ignore when performing the join (optional)
    asstring : bool
        True if return as a string, False if you require the first value -
            float or int from that line after the tag (optional)
    """
    # find the first or last occurrence of the header tag in the output dump
    i, line = (first_occurrence(datadump, headertag) if findfirst
               else last_occurrence(datadump, headertag))

    # if it cannot find anything then return an empty string
    if i == -1:
        return ('' if asstring else 0.0)

    # get the first line occurrence after the header
    i, line = first_occurrence(datadump[i:], starttag)

    return (join_strings_from_line(line, starttag, ignores, endtag) if asstring
            else first_value_from_line(line, starttag, ignores))
    

def first(datadump, headertag, starttag, endtag='', ignores=[], asstring=True):
    """
    Get the first occurrence of the linetag within the first headertag.

    Parameters
    ----------
    datadump : str
        Full output string dump
    headertag : str
        The string tag to indicate the property is below this header tag
    starttag : str
        The string tag to indicate the property is after this tag on the line
    endtag : str
        The string tag to indicate the property is before this tag on the line (optional)
    ignores : list[str]
        List of strings to ignore when performing the join (optional)
    asstring : bool
        True if return as a string, False if you require the first value -
            float or int from that line after the tag (optional)
    """
    return get(datadump=datadump,
               headertag=headertag,
               starttag=starttag,
               endtag=endtag,
               findfirst=True,
               ignores=ignores,
               asstring=asstring)


def last(datadump, headertag, starttag, endtag='', ignores=[], asstring=True):
    """
    Get the last occurrence of the linetag within the last headertag.

    Parameters
    ----------
    datadump : str
        Full output string dump
    headertag : str
        The string tag to indicate the property is below this header tag
    starttag : str
        The string tag to indicate the property is after this tag on the line
    endtag : str
        The string tag to indicate the property is before this tag on the line (optional)
    ignores : list[str]
        List of strings to ignore when performing the join (optional)
    asstring : bool
        True if return as a string, False if you require the first value -
            float or int from that line after the tag (optional)
    """
    return get(datadump=datadump,
               headertag=headertag,
               starttag=starttag,
               endtag=endtag,
               findfirst=False,
               ignores=ignores,
               asstring=asstring)
