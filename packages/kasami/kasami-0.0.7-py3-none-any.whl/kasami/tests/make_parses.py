import pickle
import sys

# from bllipparser import RerankingParser
from spacy.en import English

'''
bllip_rrp = RerankingParser.fetch_and_load('WSJ-PTB3')


def bllip_parse(s):
    print("bllip_parse-ing {0}".format(repr(s)))
    return bllip_rrp.parse(s)[0].ptb_parse
'''
spacy_parse = English()

sentence_trees = [
    ("I'm a little teapot.", spacy_parse("I'm a little teapot.")),
    ("", spacy_parse("")),
    ("{| foo | bar", spacy_parse("{| foo | bar"))
]

'''
    ("I'm a little teapot.", bllip_parse("I'm a little teapot.")),
    ("", bllip_parse("")),
    ("{| foo | bar", bllip_parse("{| foo | bar")),
'''

pickle.dump(sentence_trees, sys.stdout.buffer)

parse = English()
doc = parse("I'm a little teapot")
pickled_doc = pickle.loads(pickle.dumps(doc))
doc
pickled_doc
doc == pickled_doc
pickled_doc == parse("")
