
import util.xmlutils as xml
import util.definitions as defn
import wikitextlib

l2 = "Finnish"

templateToHeadTable = {
    "fi-adj": "adjective",
    "fi-adv": "adverb",
    "fi-adv-pos": "adverb",
    "fi-con": "conjunction",
    "fi-contr": "contraction",
    "fi-prefix": "prefix",
    "fi-suffix": "suffix",
    "fi-int": "interjection",
    "fi-noun": "noun",
    "fi-num": "numeral",
    "fi-phrase": "phrase",
    "fi-postp": "postposition",
    "fi-pron": "pronoun",
    "fi-proper noun": "proper noun",
    "fi-verb": "verb"
}
nonlemmas = ["infinitive", "participle", "comparative", "superlative", "form"]
validHeads = set(templateToHeadTable.values())
def templateToHead(temp_name):
    return templateToHeadTable.get(temp_name, None)

def parse(title, text, kwargs):
    entries = []
    new_entry = []
    nonlemma = False
    titled = False
    for item in wikitextlib.parse_wikitext(text):
        if type(item) is wikitextlib.Heading:
            if item.level == 3 and "Etymology" in item.text:
                if new_entry:
                    assert titled
                    entries.append(new_entry)
                new_entry = []
                titled = False
        elif type(item) is wikitextlib.Template:
            head = None
            if item.name in templateToHeadTable:
                head = templateToHeadTable[item.name]
                if item.name == "fi-noun" and "proper" in item.args:
                    head = "proper noun"
            elif item.name == "head" and item.args.get(1, None) == "fi":
                head = item.args[2]
            if head is not None:
                nonlemma = any(nl in head for nl in nonlemmas)
            if not nonlemma:
                if head and head.endswith("s") and head[:-1] in validHeads:
                    head = head[:-1]
                if head and not titled:
                    new_entry.append(("k", title))
                    titled = True
                if head in defn.parts_of_speech_reverse:
                    new_entry.append(("pos", defn.parts_of_speech_reverse[head]))
                if (item.name in ["alt form", "alt form of", "alternative form",
                                "alternative form of", "alternative case form of",
                                "alt case form of", "alt case"] and
                        item.args.get(1, None) == "fi"):
                    new_entry.append(("main", item.args[2]))
    if new_entry:
        assert titled
        entries.append(new_entry)
    # split if multiple <main>s
    old_entries = entries
    entries = []
    for e in old_entries:
        if sum(1 for q in e if q[0] == "main") > 1:
            base = [q for q in e if q[0] != "main"]
            mains = [q[1] for q in e if q[0] == "main"]
            for m in mains:
                e1 = base[:] + [("main", m)]
                entries.append(e1)
        else:
            entries.append(e)
    return [xml.make_xml(e) for e in entries]
