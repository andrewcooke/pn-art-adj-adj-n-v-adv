
from unittest import TestCase

from pnartadjadjnvadv.sentences import Sentences


class TestSentences(TestCase):

    def test_read(self):
        sentences = Sentences([(1, 'a'), (2, 'b')], hash=lambda x: x)
        assert len(sentences) == 2, sentences._previous
        assert sentences._sentences == {'a': (1, 2, 'a'), 'b': (2, 0, 'b')}, sentences._sentences

    def test_empty(self):
        sentences = Sentences([], hash=lambda x: x)
        assert len(sentences) == 0, sentences._sentences

