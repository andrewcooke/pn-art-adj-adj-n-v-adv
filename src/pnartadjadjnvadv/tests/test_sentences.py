
from unittest import TestCase
from collections import OrderedDict

from pnartadjadjnvadv.sentences import Sentences, key, normalize


class TestSentences(TestCase):

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
