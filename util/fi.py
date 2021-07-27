
from . import unicodeutils as unic

def xfrm(x, sort = False):
    x = x.upper()
    x = x.replace("-", "")
    x = x.replace(" ", "")
    x = x.replace("Æ", "Ä")
    x = x.replace("Ø", "Ö")
    x = x.replace("Ü", "Y")
    x = x.replace("ẞ", "SS")
    x = x.replace("ß", "SS")
    x = x.replace("Œ", "OE")
    x = x.replace("W", "V")
    x = unic.remove_diacritics(x, exceptions = set("ÅÄÖ"))
    if sort:
        x = x.replace("Þ", "¿") # Þ before Ä
        x = x.replace("Å", "À") # Å before Ä but after Þ
    return x

def compare(a, b):
    a, b = xfrm(a, True), xfrm(b, True)
    if a > b:
        return 1
    elif a < b:
        return -1
    else:
        return 0

def decompose(x, _):
    if not x:
        return []
    xx = xfrm(x)
    if not xx:
        return []
    if xx and xx[0] not in "-ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ":
        return []
    return list(c for c in xfrm(x) if c in "ABCDEFGHIJKLMNOPQRSTUVXYZÅÄÖ")

def snippet_compare(a, b):
    return compare("".join(a), "".join(b))
