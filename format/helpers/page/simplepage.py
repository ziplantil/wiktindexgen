
import wikitextlib

def make_topbar(jumpto, keys):
    return """{{-}}<onlyinclude>
----
{{center top}}'''""" + " • ".join("[[{}|{}]]".format(jumpto(k), "".join(k)) for k in keys) + """'''{{center bottom}}
----
{{tocright}}</onlyinclude>"""

def make_page(make_link, key, sections, data):
    lines = []
    if key:
        lines.append("<<<upref>>>")
        lines.append("==" + "".join(key) + "==")
    else:
        lines.append("<<<header>>>")
        lines.append("<<<downref>>>\n")
        lines.append("==Symbols==")
    for s, v in sections.items():
        if s:
            lines.append("\n===" + "".join(s) + "===")
        for x in v:
            lines.append("# " + make_link(x, data[x]))
    if key:            
        lines.append("\n<<<downref>>>")
    return "\n".join(lines)
