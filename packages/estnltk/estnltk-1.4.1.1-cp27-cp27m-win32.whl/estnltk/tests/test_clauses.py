# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import unittest

from ..text import Text

from ..clausesegmenter import ClauseSegmenter

class ClausesTest(unittest.TestCase):

    def test_divide_multi(self):
        segmenter = ClauseSegmenter()
        text = Text('Kõrred, millel on toitunud viljasääse vastsed, jäävad õhukeseks.', clause_segmenter = segmenter)
        clauses = text.divide('words', 'clauses')
        korred, _1, millel, on, toitunud, viljasaase, vastsed, _2, jaavad, ohukeseks, _3 = text.words
        self.assertListEqual([korred, jaavad, ohukeseks, _3], clauses[0])
        self.assertListEqual([_1, millel, on, toitunud, viljasaase, vastsed, _2], clauses[1])
        self.assertEqual(len(clauses), 2)
        # Terminate Java process in order to avoid "OSError: [WinError 6] The handle is invalid"
        # in subsequent Java processing
        segmenter._process.terminate()

    def test_split_by_clauses(self):
        segmenter = ClauseSegmenter()
        text = Text('Kõrred, millel on toitunud viljasääse vastsed, jäävad õhukeseks.', clause_segmenter = segmenter)
        outer = Text('Kõrred jäävad õhukeseks.', clause_segmenter = segmenter).tag_clauses()
        inner = Text(', millel on toitunud väljasääse vastsed,', clause_segmenter = segmenter).tag_clauses()
        outer_split, inner_split = text.split_by('clauses')
        self.assertListEqual(inner.word_spans, inner_split.word_spans)
        self.assertListEqual(outer.word_spans, outer_split.word_spans)
        # Terminate Java process in order to avoid "OSError: [WinError 6] The handle is invalid"
        # in subsequent Java processing
        segmenter._process.terminate()

    def test_ignore_missing_commas_1(self):
        segmenter = ClauseSegmenter( ignore_missing_commas=True )
        text = Text('Pritsimehed leidsid eest lõõmava kapotialusega auto mida läheduses parkinud masinate sohvrid eemale üritasid lükata kuid esialgu see ei õnnestunud sest autol oli käik sees.', clause_segmenter = segmenter)
        clauses = text.divide('words', 'clauses')
        self.assertEqual(len(clauses), 4)
        # Terminate Java process in order to avoid "OSError: [WinError 6] The handle is invalid"
        # in subsequent Java processing
        segmenter._process.terminate()
    
    def test_ignore_missing_commas_2(self):
        segmenter = ClauseSegmenter( ignore_missing_commas=True )
        text = Text('Keegi teine ka siin ju kirjutas et ütles et saab ise asjadele järgi minna aga vastust seepeale ei tulnudki.', clause_segmenter = segmenter)
        clauses = text.divide('words', 'clauses')
        self.assertEqual(len(clauses), 4)
        # Terminate Java process in order to avoid "OSError: [WinError 6] The handle is invalid"
        # in subsequent Java processing
        segmenter._process.terminate()
