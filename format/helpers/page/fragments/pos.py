
import util.definitions as defs
import util.htmlutils as html

aIsAdj = {"a": "adj"}
longerNames = {"a": "adj", "p": "pron", "pn": "proper"}

def partOfSpeechSimple(pos, forms = {}):
    return "''{}''".format(forms.get(pos, pos))

def partsOfSpeechSimple(psos, forms = {}):
    return ", ".join(partOfSpeechSimple(pos, forms) for pos in psos)

def partOfSpeechAbbr(pos, forms = {}):
    full = defs.parts_of_speech.get(pos, pos)
    if full != pos:
        return "''<abbr title=\"{}\">{}</abbr>''".format(html.escape_html_quote(full), forms.get(pos, pos))
    else:
        return "''{}''".format(forms.get(pos, pos))

def partsOfSpeechAbbr(psos, forms = {}):
    return ", ".join(partOfSpeechAbbr(pos, forms) for pos in psos)
