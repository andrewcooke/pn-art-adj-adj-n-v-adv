
from unittest import TestCase

from pnartadjadjnvadv.sentences import Sentences


class TestSentences(TestCase):

    def test_read(self):
        sentences = Sentences([(1, 'a'), (2, 'b')], hash=lambda x: x)
        assert len(sentences) == 2, sentences._previous
        assert sentences._sentences == {'a': (1, 2, 'a'), 'b': (2, None, 'b')}, sentences._sentences

    def test_empty(self):
        sentences = Sentences([], hash=lambda x: x)
        assert len(sentences) == 0, sentences._sentences

    def test_normalize(self):
        self.assert_normalize('abc', 'abc')
        self.assert_normalize('ABC', 'abc')
        self.assert_normalize(' abc ', 'abc')
        self.assert_normalize('ab c', 'ab c')
        self.assert_normalize('ab  c', 'ab c')
        self.assert_normalize('ab-c', 'ab c')

    def assert_normalize(self, sentence, expected):
        result = Sentences([], hash=lambda x: x)._key(sentence)
        assert result == expected, result