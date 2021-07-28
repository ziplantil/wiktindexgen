
from .helpers import to_wikitext as formatter
from pywikibot import Site, Page

simulate = False

def format(infile, args, kwargs):
    if len(args) < 1:
        raise ValueError("missing prefix")
    prefix = args[0]
    summary = kwargs.get("summary", "wiktindexgen format_enwikt_pwb")
    site = Site("en", fam="wiktionary")
    site.login()

    lang, date, pages = formatter.format(infile, lambda lang, snippet: prefix + "".join("/" + c for c in snippet), args, kwargs)

    maxlines = 0
    for snippet, text in pages:
        title = prefix + "".join("/" + c for c in snippet)
        page = Page(site, title)
        try:
            if page.text.strip() == text.strip():
                continue
        except:
            pass
        page.text = text
        if simulate:
            print(title)
            print(text)
        else:
            page.save(summary, minor = False)
