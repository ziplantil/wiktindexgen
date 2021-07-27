
def escape_xml(x):
    return x.replace("&", "&amp;").replace("\"", "&quot;").replace("'", "&apos;").replace("<", "&lt;").replace(">", "&gt;")

def escape_xml_tag(x):
    return escape_xml(x)

def escape_xml_attr(x):
    return x.replace("&", "&amp;").replace("\"", "&quot;").replace("'", "&apos;").replace("<", "&lt;")

def escape_xml_text(x):
    return x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def make_xml_pair(pair):
    name, value = pair
    return "<" + escape_xml_tag(name) + ">" + escape_xml_text(value) + "</" + escape_xml_tag(name) + ">"

def make_xml(pairs):
    return "".join(make_xml_pair(pair) for pair in pairs)
