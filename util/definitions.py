from . import dictutils

parts_of_speech = {
    "n": "noun",
    "v": "verb",
    "a": "adjective",
    "adv": "adverb",
    "p": "pronoun",
    "pn": "proper noun",
    "num": "numeral",
    "part": "particle",
    "prep": "preposition",
    "postp": "postposition",
    "conj": "conjunction",
    "det": "determiner",
    "int": "interjection",
    "pref": "prefix",
    "suff": "suffix",
    "infix": "infix",
    "interfix": "interfix",
    "clitic": "clitic",
    "ideophone": "ideophone",
    "phrase": "phrase",
    "proverb": "proverb",
    "letter": "letter",
    "symbol": "symbol",
    "root": "root"
}
parts_of_speech_reverse = dictutils.invert(parts_of_speech)

genders = {
    "m": "masculine",
    "f": "feminine",
    "n": "neuter",
    "c": "common",
    "an": "animate",
    "in": "inanimate",
    "anml": "animal",
    "pr": "personal",
    "np": "nonpersonal"
}
genders_reverse = dictutils.invert(genders)

numbers = {
    "s": "singular",
    "d": "dual",
    "p": "plural"
}
numbers_reverse = dictutils.invert(numbers)

aspects = {
    "impf": "imperfective",
    "pf": "perfective"
}
aspects_reverse = dictutils.invert(aspects)