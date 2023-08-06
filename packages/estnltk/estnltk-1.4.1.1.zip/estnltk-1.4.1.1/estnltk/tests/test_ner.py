# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import unittest
from copy import deepcopy

import estnltk
from ..estner.featureextraction import MorphFeatureExtractor, LocalFeatureExtractor, GazetteerFeatureExtractor, \
    apply_templates
from ..estner.ner import Token
from ..core import as_unicode
from ..text import Text
from ..ner import json_document_to_estner_document, NerTagger


class TestFeatureExtractor(unittest.TestCase):
    def test__apply_templates(self):
        # case 1
        templates = [(('lem', 0),), ]
        t = Token()
        t.word = 'Rahvusvahelistega'
        t.lemma = 'rahvus_vaheline+tega'
        t.morph = '_A_ pl kom'
        t['lem'] = 'rahvusvaheline'
        apply_templates([t], templates)
        self.assertEqual(len(t['F']), 1)
        self.assertTrue('lem[0]=rahvusvaheline' in t['F'])

        # case 2
        t['F'][:] = []
        t['lem'] = ['a', 'b']
        apply_templates([t], templates)
        self.assertEqual(len(t['F']), 2)
        self.assertTrue('lem[0]=a' in t['F'])
        self.assertTrue('lem[0]=b' in t['F'])

        # case 3
        templates = [(('lem', 0), ('lem', 1)), ]
        t['F'][:] = []
        t['lem'] = ['a', 'b']

        t2 = deepcopy(t)
        t2['lem'] = ['c', 'd']

        apply_templates([t, t2], templates)
        self.assertEqual(len(t['F']), 4)
        self.assertTrue('lem[0]|lem[1]=a|c' in t['F'])
        self.assertTrue('lem[0]|lem[1]=a|d' in t['F'])
        self.assertTrue('lem[0]|lem[1]=b|c' in t['F'])
        self.assertTrue('lem[0]|lem[1]=b|d' in t['F'])


class TestGazetteerFeatureExtractor(unittest.TestCase):
    def test(self):
        fex = GazetteerFeatureExtractor(estnltk.estner.settings)

        text = Text(as_unicode('Mr Alexander Graham Bell on tuntud teadlane.'))
        doc = json_document_to_estner_document(text)
        tokens = list(doc.tokens)

        self.assertEqual(len(tokens), 8)

        MorphFeatureExtractor().process(doc)
        LocalFeatureExtractor().process(doc)
        fex.process(doc)

        t = tokens[0]
        self.assertEqual(t.word, 'Mr')
        self.assertTrue('gaz' not in t)

        t = tokens[1]

        self.assertEqual(t.word, 'Alexander')
        self.assertTrue('gaz' in t)
        self.assertTrue('peop' in t['gaz'])

        t = tokens[2]
        self.assertEqual(t.word, 'Graham')
        self.assertTrue('gaz' in t)
        self.assertTrue('peop' in t['gaz'])

        t = tokens[3]
        self.assertEqual(t.word, 'Bell')
        self.assertTrue('gaz' in t)
        self.assertTrue('peop' in t['gaz'])

        t = tokens[4]
        self.assertEqual(t.word, 'on')
        self.assertTrue('gaz' not in t)


class TestMorphFeatureExtractor(unittest.TestCase):
    def test(self):
        fex = MorphFeatureExtractor()

        t = Token()
        t.word = 'Rahvusvahelistega'
        t.lemma = 'rahvus_vaheline+tega'
        t.morph = '_A_ pl kom'
        t.label = 'O'

        fex._process(t)
        self.assertEqual(t['lem'], 'rahvusvaheline')
        self.assertEqual(t['pos'], '_A_')
        self.assertTrue('prop' not in t)
        self.assertEqual(t['pref'], 'rahvus')
        self.assertEqual(t['post'], 'vaheline')
        self.assertTrue('case' not in t)
        self.assertEqual(t['end'], 'tega')
        self.assertTrue('pun' not in t)


class TestLocalFeatureExtractor(unittest.TestCase):
    def test(self):
        t = Token()
        t.word = as_unicode('Lõuna-Eestis')
        t.lemma = as_unicode('Lõuna-Eesti+s')
        t['lem'] = as_unicode('lõuna-eesti')
        t.morph = '_H_ sg in'

        fex = LocalFeatureExtractor()
        fex._process(t)

        self.assertEqual(t['w'], as_unicode('Lõuna-Eestis'))
        self.assertEqual(t['wl'], as_unicode('lõuna-eestis'))
        self.assertEqual(t['shape'], 'ULLLL-ULLLLL')
        self.assertEqual(t['shaped'], 'UL-UL')

        self.assertEqual(t['p1'], 'l')
        self.assertEqual(t['p2'], as_unicode('lõ'))
        self.assertEqual(t['p3'], as_unicode('lõu'))
        self.assertEqual(t['p4'], as_unicode('lõun'))

        self.assertEqual(t['s1'], 'i')
        self.assertEqual(t['s2'], 'ti')
        self.assertEqual(t['s3'], 'sti')
        self.assertEqual(t['s4'], 'esti')

        self.assertTrue('2d' not in t)
        self.assertTrue('up' not in t)

        self.assertTrue('iu' in t)
        self.assertTrue('au' not in t)
        self.assertTrue('al' not in t)
        self.assertTrue('ad' not in t)

        self.assertTrue('cu' in t)
        self.assertTrue('cl' in t)
        self.assertTrue('cd' not in t)
        self.assertTrue('cp' not in t)
        self.assertTrue('cds' in t)
        self.assertTrue('cdt' not in t)
        self.assertTrue('cs' in t)

        self.assertEqual(t['bdash'], as_unicode('lõuna'))
        self.assertEqual(t['adash'], as_unicode('eesti'))

        self.assertEqual(t['len'], '11')


class TestNer(unittest.TestCase):
    def test(self):
        t = Text('Alexander Tkachenko elab Pärnus')
        self.assertEqual(t.named_entities, ['Alexander Tkachenko', as_unicode('Pärnu')])
        self.assertEqual(t.named_entity_labels, ['PER', 'LOC'])
        self.assertEqual(t.named_entity_spans, [(0, 19), (25, 31)])

        t = Text(as_unicode('Tallinn on Eesti pealinn.'))
        self.assertEqual(t.named_entities, ['Tallinn', 'Eesti'])
        self.assertEqual(t.named_entity_labels, ['LOC', 'LOC'])

        t = Text(as_unicode('Eesti piirneb põhjas üle Soome lahe Soome Vabariigiga.'))
        self.assertEqual(t.named_entities, ['Eesti', 'Soome laht', 'Soome Vabariik'])
        self.assertEqual(t.named_entity_labels, ['LOC', 'LOC', 'LOC'])

        t = Text(as_unicode('2006. aastal valiti presidendiks Toomas Hendrik Ilves.'))
        self.assertEqual(t.named_entities, ['Toomas Hendrik Ilves'])
        self.assertEqual(t.named_entity_labels, ['PER'])

        t = Text(as_unicode(
            'Inimestelt saadud vihjed pole veel politseil aidanud leida 43-aastast Kajar Paasi, kes tema naise sõnul Ardus maanteel rööviti.'))
        self.assertEqual(t.named_entities, ['Kajar Paas', 'Ardu'])
        self.assertEqual(t.named_entity_labels, ['PER', 'LOC'])

        t = Text(
            as_unicode('Tuhanded Šotimaa kodud on lääneranniku piirkondi tabanud „ilmapommi“-tormi tõttu elektrita'))
        self.assertEqual(t.named_entities, [as_unicode('Šotimaa')])
        self.assertEqual(t.named_entity_labels, ['LOC'])

        t = Text(as_unicode('Elion AS ja EMT on Eesti suurimad ettevõted.'))
        self.assertEqual(t.named_entities, ['Elion AS', 'EMT', 'Eesti'])
        self.assertEqual(t.named_entity_labels, ['ORG', 'ORG', 'LOC'])
