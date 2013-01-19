
from unittest import TestCase
from collections import OrderedDict

from pnartadjadjnvadv.sentences import Sentences, key, normalize


class TestSentences(TestCase):

    def test_read(self):
        sentences = Sentences([(1, 'a'), (2, 'b')])
        assert len(sentences) == 2, sentences._previous
        assert sentences._sentences == OrderedDict([(key('a'), (1, 2, 'a')), (key('b'), (2, None, 'b'))]), sentences._sentences

    def test_empty(self):
        sentences = Sentences([])
        assert len(sentences) == 0, sentences._sentences

    def test_normalize(self):
        self.assert_normalize('abc', 'abc')
        self.assert_normalize('ABC', 'abc')
        self.assert_normalize(' abc ', 'abc')
        self.assert_normalize('ab c', 'ab c')
        self.assert_normalize('ab  c', 'ab c')
        self.assert_normalize('ab-c', 'ab c')

    def assert_normalize(self, sentence, expected):
        result = normalize(sentence)
        assert result == expected, result