
def escape_html_quote(x):
    return x.replace("&", "&amp;").replace("\"", "&quot;").replace("'", "&apos;").replace("<", "&lt;").replace(">", "&gt;")

def escape_html(x):
    return x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
