
from operator import itemgetter
from time import time, sleep
from Crypto.Hash import SHA256
from Crypto.Random.random import randint
from pnartadjadjnvadv.utils import eprint
from re import compile


NON_LETTERS = compile(r'[^a-z\s]+')
SEPARATORS = compile(r'[-\s]+')
PERIOD = 50000
#PERIOD = 5


def hash_sha_256(sentence):
    return SHA256.new(sentence.encode('utf8')).digest()

def normalize(sentence):
    single_spaced = SEPARATORS.sub(' ', sentence.strip().lower())
    return NON_LETTERS.sub('', single_spaced)

def key(sentence):
    return hash_sha_256(normalize(sentence))


class Sentences:

    def __init__(self, words, read, write):
        self.__words = words
        self.__write = write
        self.__known = set()
        self.__last = None
        data = list(read())
        data.sort(key=itemgetter(0))
        data.append((None, None))
        for (start, sentence), (end, _) in zip(data, data[1:]):
            self.__last = start
            write(False, start, sentence)
            self.__known.add(key(sentence))

    def __calculate_next_epoch(self, epoch):
        if epoch:
            return epoch + randint(1, 2 * PERIOD)
        else:
            return time() # now - special case when empty

    def __wait_until(self, epoch):
        now = time()
        while epoch > now:
            eprint('waiting til %d (%ds)' % (epoch, epoch - now))
            sleep(max(0, epoch - now))
            now = time()
        return int(now)

    def __unique_sentence(self):
        while True:
            sentence = self.__words.sentence()
            k = key(sentence)
            if k not in self.__known:
                self.__known.add(k)
                return sentence

    def __call__(self):
        epoch = self.__last
        while True:
            epoch = self.__wait_until(self.__calculate_next_epoch(epoch))
            self.__write(True, epoch, self.__unique_sentence())
