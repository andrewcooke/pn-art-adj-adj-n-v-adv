#!/usr/bin/env python

from Crypto.Random.random import choice
from os.path import dirname, join
from pkg_resources import resource_stream

from pnartadjadjnvadv.utils import to_list, tmap


class Words:

    def __init__(self):
        self._read_words()

    def _read_words(self):
        self._words = tmap(self._read,
            ['names', 'adjectives', 'colours', 'animals', 'verbs', 'adverbs'])

    def sentence(self):
        line = "%s the %s %s %s %s %s." % tmap(choice, self._words)
        return line[0].upper() + line[1:]

    @to_list
    def _read(self, name):
        try:
            for line in resource_stream('__main__', 'distinct-%s' % name):
                yield line.strip()
        except IOError:
            with open(join(dirname(dirname(dirname(__file__))), 'distinct-%s' % name)) as input:
                for line in input:
                    yield line.strip()


if __name__ == '__main__':
    print(Words().sentence())
