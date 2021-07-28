
from .fragments import pos as fmtpos

def fi_link(form):
    return "{{l|fi|" + form + "}}"

def link(form, entry):
    base = fi_link(form)
    footer = " "
    if "main" in entry:
        footer += "→ " + ", ".join(fi_link(x) for x in entry["main"])
    elif "pos" in entry:
        footer += "– " + fmtpos.partsOfSpeechSimple(entry["pos"], fmtpos.longerNames)
    return (base + footer).strip()

always_subdivide = False
