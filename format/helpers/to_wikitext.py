
import functools
import importlib
from collections import OrderedDict

# if more than this many per page, split page if possible
MAX_TERMS_PER_PAGE = 1000
# if more than this many per page, add subheadings
MAX_TERMS_PER_SECTION = 200
# probably don't need to split beyond five levels
MAX_LEVELS = 5

def strip_ns(tag):
    if "{" and "}" in tag:
        return tag[tag.find("}") + 1 :]
    return tag

def make_entry_default(form, entry):
    return "[[" + form + "]]"

def subdivide_default(key, pages, data):
    result = OrderedDict()
    level = len(key)
    for p in pages:
        target = tuple()
        decomp = data[p]["_"]
        if len(decomp) > level:
            target = key + (decomp[level],)
        if target not in result:
            result[target] = []
        result[target].append(p)
    return result

def clean_entry_default(entry):
    return {}

def merge_entry_default(entry1, entry2):
    return entry1

def format_page(langutil, fmtpage, make_link, key, pages, data):
    subheadings = len(key) < MAX_LEVELS and len(pages) >= MAX_TERMS_PER_SECTION
    try:
        subheadings = subheadings or fmtpage.always_subdivide
    except:
        pass
    try:
        subdivide = fmtpage.subdivide
    except:
        subdivide = subdivide_default
    try:
        make_page = fmtpage.make
    except:
        from .page.simplepage import make_page
    if subheadings:
        sections = subdivide(key, pages, data)
    else:
        sections = {tuple(): pages}
    sections_sorted = OrderedDict((k, sections[k]) for k in sorted(sections.keys(), key = functools.cmp_to_key(langutil.snippet_compare)))
    for k, v in sections_sorted.items():
        v.sort(key = functools.cmp_to_key(langutil.compare))
    return make_page(make_link, key, sections_sorted, data)

def format(infile, jumpto, args, kwargs):
    import xml.etree.ElementTree as etree
    # first check meta

    in_index = False
    in_meta = False
    lang, date = None, None
    meta = {}
    for event, elem in etree.iterparse(infile, events=("start", "end")):
        if event == "start":
            if strip_ns(elem.tag) == "index":
                in_index = True
                lang = elem.attrib["lang"]
                date = elem.attrib["date"]
            if strip_ns(elem.tag) == "meta":
                in_meta = True
        elif event == "end":
            if in_index and in_meta:
                meta[elem.tag] = elem.text
            if in_index and strip_ns(elem.tag) == "meta":
                break
            elem.clear()
    if not in_index:
        raise ValueError("no <index>, invalid index XML.")
    if not in_meta:
        raise ValueError("no <meta>, invalid index XML.")
    if lang is None or date is None:
        raise ValueError("no lang or date, invalid index XML.")

    util_override = kwargs.get("utillang", lang)
    page_override = kwargs.get("pagelang", lang)
    entry_override = kwargs.get("entrylang", lang)
    langutil = importlib.import_module("util." + util_override)
    try:
        fmtpage = importlib.import_module("format.helpers.page." + page_override)
    except:
        fmtpage = None
    try:
        entryutil = importlib.import_module("format.helpers.entry." + entry_override)
    except:
        entryutil = None
    try:
        make_entry = fmtpage.link
    except:
        make_entry = make_entry_default
    try:
        make_topbar = fmtpage.topbar
    except:
        from .page.simplepage import make_topbar
    try:
        clean_entry = entryutil.make
    except:
        clean_entry = clean_entry_default
    try:
        merge_entry = entryutil.merge
    except:
        merge_entry = merge_entry_default

    in_entry = False
    entries = {}
    for event, elem in etree.iterparse(infile, events=("start", "end")):
        if event == "start":
            if strip_ns(elem.tag) == "index":
                in_index = True
            if in_index and strip_ns(elem.tag) == "e":
                in_entry = True
                entry = {}
        elif event == "end":
            if in_index and strip_ns(elem.tag) == "e":
                newentry = clean_entry(entry)
                if entry["k"] in entries:
                    # merge
                    entries[entry["k"]] = merge_entry(entries[entry["k"]], newentry)
                else:
                    entries[entry["k"]] = newentry
                in_entry = False
            if in_entry:
                if elem.tag in ["k", "main"]:
                    entry[elem.tag] = elem.text
                else:
                    if elem.tag not in entry:
                        entry[elem.tag] = []
                    entry[elem.tag].append(elem.text)
            elem.clear()

    data = entries
    entries = list(entries.keys())
    # decomposition for all words
    for x in entries:
        data[x]["_"] = tuple(langutil.decompose(x, data[x].get("ph", x))[:MAX_LEVELS])

    header = "::''Created with wiktindexgen. {} entries, dumped {}''".format(len(entries), date)
    pages = {}
    pages[tuple()] = entries

    # split downwards until below max page limit or max levels reached
    visit = [tuple()]
    while visit:
        n, *visit = visit
        level = len(n)
        if level >= MAX_LEVELS:
            continue
        if len(pages[n]) > MAX_TERMS_PER_PAGE:
            backup = pages[n][:]
            pages[n] = []
            for e in backup:
                decomp = data[e]["_"]
                if level >= len(decomp):
                    target = n
                else:
                    target = n + (decomp[level],)
                if target not in pages:
                    pages[target] = []
                    visit.append(target)
                pages[target].append(e)

    formatpages = {}
    children = {}
    for key in pages:
        formatpages[key] = format_page(langutil, fmtpage, make_entry, key, pages[key], data)
        if key:
            up = key[:-1]
            if up not in children:
                children[up] = []
            children[up].append(key)

    for child in formatpages.keys():
        if child:
            parent = child[:-1]
            assert parent in children
            text = formatpages[child]
            ur = "{{" + jumpto(lang, parent) + "}}"
            if "<<<upref>>>" in text:
                text = text.replace("<<<upref>>>", ur)
            else:
                text = ur + "\n" + text
            formatpages[child] = text

    for parent in children.keys():
        text = formatpages[parent]
        dr = make_topbar(lambda x: jumpto(lang, x), list(sorted(children[parent], key = functools.cmp_to_key(langutil.snippet_compare))))
        if "<<<downref>>>" in text:
            text = text.replace("<<<downref>>>", dr)
        else:
            text = text + "\n" + dr
        formatpages[parent] = text

    for page in formatpages.keys():
        if "<<<header>>>" in formatpages[page]:
            formatpages[page] = formatpages[page].replace("<<<header>>>", header)
        if "<<<upref>>>" in formatpages[page]:
            formatpages[page] = formatpages[page].replace("<<<upref>>>", "")
        if "<<<downref>>>" in formatpages[page]:
            formatpages[page] = formatpages[page].replace("<<<downref>>>", "")

    return lang, date, [(k, v) for k, v in formatpages.items()]
