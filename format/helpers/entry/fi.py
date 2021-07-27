
import util.dictutils as dictu

def make(entry):
    k = dictu.filter_keys(entry, {"pos", "main"})
    if "main" in k:
        k["main"] = [k["main"]]
    return k

def merge(entry1, entry2):
    return dictu.extend_lists_unique(entry1, entry2)
