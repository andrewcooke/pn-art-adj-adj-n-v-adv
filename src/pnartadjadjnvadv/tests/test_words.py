
from unittest import TestCase

from pnartadjadjnvadv.words import Words


class WordsTest(TestCase):

    def test_reading(self):
        words = Words(None)
        assert words._words, 'no words'
        assert len(words._words) == 6, len(words._words)
        assert 'happy' in words._words[1]

    def test_sentence(self):
        words = Words(None)
        sentence = words._new_sentence()
        assert sentence
        print(sentence)