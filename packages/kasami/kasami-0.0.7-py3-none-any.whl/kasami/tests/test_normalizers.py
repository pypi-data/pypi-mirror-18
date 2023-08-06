import os
import pickle

from nose.tools import eq_

from .. import normalizers

sentence_trees = pickle.load(
    open(os.path.join(os.path.dirname(__file__), "parses.pickle"), "rb"))
spacy_teapot, spacy_empty, spacy_junk = sentence_trees


def test_spacy():
    print(spacy_teapot)
    eq_(str(normalizers.spacy(spacy_teapot[1])),
        "(EMPTY 'EMPTY')")
    print(spacy_empty)
    eq_(str(normalizers.spacy(spacy_empty[1])),
        "foobar2")
    print(spacy_junk)
    eq_(str(normalizers.spacy(spacy_junk[1])),
        "foobar3")
