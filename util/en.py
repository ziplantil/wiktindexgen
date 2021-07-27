
def xfrm(x):
    x = x.upper()
    x = x.replace("-", "")
    x = x.replace(" ", "")
    return x

def compare(a, b):
    a, b = xfrm(a), xfrm(b)
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
    if xx and xx[0] not in "-ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return []
    return list(c for c in xx if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def snippet_compare(a, b):
    return compare("".join(a), "".join(b))
