
import unicodedata

def remove_diacritics_char(c, exceptions = None):
    if exceptions and c in exceptions:
        return c
    return unicodedata.normalize("NFKC", "".join(q for q in unicodedata.normalize("NFKD", c) if not unicodedata.combining(q)))

def remove_diacritics(text, exceptions = None):
    return "".join(remove_diacritics_char(c, exceptions) for c in unicodedata.normalize("NFKC", text))
