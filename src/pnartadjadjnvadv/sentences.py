
from time import time
from Crypto.Hash import SHA256
from Crypto.Random.random import randint
from re import compile
from threading import Lock

from pnartadjadjnvadv.utils import synchronized


WRITE_LOCK = Lock()
NON_LETTERS = compile(r'[^a-z\s]+')
SEPARATORS = compile(r'[-\s]+')
PERIOD = 50000


def hash_sha_256(sentence):
    return SHA256.new(sentence.encode('utf8')).digest()

def key(sentence):
    single_spaced = SEPARATORS.sub(' ', sentence.strip().lower())
    letters_and_spaces = NON_LETTERS.sub('', single_spaced)
    return hash_sha_256(letters_and_spaces)


class Sentences:

    def __init__(self, shuttle, hash=hash_sha_256):
        self._shuttle = shuttle
        self._hash = hash
        (self._previous, self._sentences) = self._read()
        self._calculate_next_epoch()

    def _read(self):
        extended = list(self._shuttle)
        extended.sort(key=lambda ses: ses[0])
        previous = extended[-1] if extended else (None, None)
        extended.append((None, None))
        return previous, \
               {key(sentence): (start, end, sentence)
                for ((start, sentence), (end, _)) in zip(extended, extended[1:])}

    def __contains__(self, item):
        return item in self._sentences

    def __len__(self):
        return len(self._sentences)

    def __getitem__(self, item):
        return self._sentences[item]

    def __reversed__(self):
        '''This is incomplete - it returns only the last key.  It is provided
        so that the current value can be found in server via the OrderedDict
        interface.'''
        yield key(self._previous[1])

    @synchronized(WRITE_LOCK)
    def add(self, sentence):
        k = key(sentence)
        if k in self._sentences: raise ValueError('sentence already exists')
        now = time()
        self._shuttle.append(now, sentence)
        self._sentences[k] = (now, sentence)
        self._previous = (now, sentence)
        self._calculate_next_epoch()

    def _calculate_next_epoch(self):
        if self._previous[0]:
            self._next_epoch = min(time(), self._previous[0] + randint(1, 2 * PERIOD))
        else:
            self._next_epoch = time()

    def next_epoch(self):
        return self._next_epoch

