
from .helpers import to_wikitext as formatter
import os.path

def format(infile, args, kwargs):
    if len(args) < 1:
        raise ValueError("missing output folder")
    folder = args[0]

    lang, date, pages = formatter.format(infile, lambda lang, snippet: lang + "_" + "".join(snippet), args, kwargs)

    for snippet, text in pages:
        fn = lang + "_" + "".join(snippet) + ".txt"
        with open(os.path.join(folder, fn), "w", encoding = "utf-8") as f:
            f.write(text)
