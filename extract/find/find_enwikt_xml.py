
import datetime
import wikitextlib
import re

def validate_date(dt):
    try:
        y, m, d = dt.split("-")
        y, m, d = int(y), int(m), int(d)
        assert y > 1970
        ly = int(not y % 4) - (int(not y % 100) - int(not y % 400))
        assert m in range(1, 13)
        assert d in range(1, 1 + [31, 28 + ly, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    except:
        raise ValueError("invalid date!")

class Finder():
    def __init__(self, args, kwargs):
        if len(args) < 1:
            raise ValueError("input XML file required")
        self.xml_in = args[0]
        if len(args) > 1:
            self.xml_date = args[1]
            validate_date(self.xml_date)
        else:
            try:
                m = re.match(r".+-(\d{8,})-pages-articles\.xml", self.xml_in)
                d = m.group(1)
                self.xml_date = d[:-4] + "-" + d[-4:-2] + "-" + d[-2:]
                validate_date(self.xml_date)
            except:
                raise ValueError("cannot extract date from file name. please specify it as an extra parameter in the format YYYY-MM-DD")

    def get_date(self):
        return self.xml_date

    def get_pages(self, l2):
        for page in wikitextlib.iterate_pages_in_xml(self.xml_in):
            if wikitextlib.contains_l2(page.text, l2):
                yield (page.title, wikitextlib.get_section_text(page.text, 2, l2))
