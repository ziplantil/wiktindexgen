
def invert(d):
    return {v: k for k, v in d.items()}

def filter_keys(d, keys):
    r = type(d)()
    for k, v in d.items():
        if k in keys:
            r[k] = v
    return r

def extend_lists(d1, d2):
    for k, v in d1.items():
        if k in d2:
            d1[k] += d2[k]
    return d1

def list_unique(l):
    s = set()
    r = []
    for x in l:
        if x not in s:
            s.add(x)
            r.append(x)
    return r

def extend_lists_unique(d1, d2):
    for k, v in d1.items():
        if k in d2:
            d1[k] = list_unique(d1[k] + d2[k])
    return d1
