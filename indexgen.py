
import sys, traceback, importlib

class UsageError(ValueError):
    pass

def parse_rest(rest):
    flags = True
    p, kw = [], {}
    nextname = None
    for a in rest:
        if a == "--":
            if nextname:
                kw[nextname] = True
            flags = False
            nextname = None
        elif flags and a.startswith("-") and len(a) > 1:
            n = a[1:]
            if n[0] == "-":
                n = n[1:]
            if nextname:
                kw[nextname] = True
            nextname = n
        elif nextname:
            kw[nextname] = a
            nextname = None
        else:
            p.append(a)
    return p, kw

def do_extract(args):
    import util.xmlutils as xml
    try:
        site, lang, method, outxml, *rest = args
    except ValueError:
        raise UsageError("not enough parameters: " +
                         "<site> <lang> <method> <out-xml>")
    pargs, kwargs = parse_rest(rest)
    url = None
    if len(site) >= 6 and site.endswith("wikt"):
        url = "https://{}.{}.org/".format(site[:-4], "wiktionary")
    findname = "find_" + site + "_" + method
    parsename = "parse_" + site + "_" + lang
    findmodule = importlib.import_module("extract.find." + findname)
    parsemodule = importlib.import_module("extract.parse." + parsename)
    finder = findmodule.Finder(pargs, kwargs)
    total = 0
    with open(outxml, "w", encoding = "utf-8") as f:
        print("<index lang=\"{}\" date=\"{}\">".format(xml.escape_xml_attr(lang), xml.escape_xml_attr(finder.get_date())), file = f)
        print("  <meta>", file = f)
        if url:
            print("    <site>{}</site>".format(url), file = f)
        print("  </meta>", file = f)
        entries = []
        for title, text in finder.get_pages(parsemodule.l2):
            for entry in parsemodule.parse(title, text, kwargs):
                if entry:
                    print("  <e>{}</e>".format(entry), file = f)
                    total += 1
        print("</index>", file = f)
    print(total)

def do_format(args):
    try:
        inxml, formatter, *rest = args
    except ValueError:
        raise UsageError("not enough parameters: " +
                         "<formatter> <in-xml>")
    pargs, kwargs = parse_rest(rest)
    fmtmodule = importlib.import_module("format.format_" + formatter)
    fmtmodule.format(inxml, pargs, kwargs)

def main(*argv):
    try:
        if len(argv) <= 1:
            raise UsageError("allowed modes: extract, format")
        elif argv[1] == "extract":
            do_extract(argv[2:])
        elif argv[1] == "format":
            do_format(argv[2:])
        else:
            raise UsageError("unknown script")
        return 0
    except:
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main(*sys.argv))
