
from time import time
from Crypto.Hash import SHA256
from re import compile
from threading import Lock

from pnartadjadjnvadv.utils import synchronized


WRITE_LOCK = Lock()
NON_LETTERS = compile(r'[^a-z]+')
PERIOD = 50000
PERIOD_ERROR = 10000


def hash_sha_256(sentence):
    return SHA256.new(sentence.encode('utf8')).digest()


class Sentences:

    def __init__(self, shuttle, hash=hash_sha_256):
        self._shuttle = shuttle
        self._hash = hash
        (self._previous, self._sentences) = self._read()

    def _read(self):
        extended = list(self._shuttle)
        extended.sort(key=lambda ses: ses[0])
        previous = extended[-1] if extended else (None, None)
        extended.append((None, None))
        return previous, \
               {self._key(sentence): (start, end, sentence)
                for ((start, sentence), (end, _)) in zip(extended, extended[1:])}

    def _key(self, sentence):
        return self._hash(NON_LETTERS.sub('', sentence.lower()))

    def __contains__(self, item):
        return self._key(item) in self._sentences

    def __len__(self):
        return len(self._sentences)

    def __getitem__(self, item):
        return self._sentences[self._key(item)]

    @synchronized(WRITE_LOCK)
    def add(self, sentence):
        key = self._key(sentence)
        if key in self._sentences: raise ValueError('sentence already exists')
        now = time()
        self._shuttle.append(now, sentence)
        self._sentences[key] = (now, sentence)
        self._previous = (now, sentence)

    def current_sentence(self):
        return self._previous[1]
