
from os.path import dirname, exists

from brigit import Git, GitException

from pnartadjadjnvadv.sentences import PERIOD
from pnartadjadjnvadv.utils import eprint


class GitFile:

    def __init__(self, path):
        self.__path = path
        self.__new = True
        self.__git = Git(dirname(path))

    def read(self):
        if exists(self.__path):
            with open(self.__path, 'r') as input:
                for line in input:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        epoch, sentence = line.split(' ', 1)
                        yield int(epoch), sentence
                    self.__new = False

    def __header(self):
        with open(self.__path, 'w') as output:
            output.write('''
# each non-comment line contains a unix epoch, followed by a sentence,
# encoded in ascii, and terminated by a newline character (unix style).

# the epoch is the time at which the sentence was created.  obviously there
# may be some delay before it is visible.  sentences 'end' when the next one
# is created.  the gap is typically of order %d seconds, but is not
# guaranteed (there is a random - stochastic - component as well as the
# possibility of service downtimes, etc).

# blank lines and those starting with a # are comments.

''' % PERIOD)

    def __push(self):
        try:
            self.__git.add(self.__path)
            self.__git.commit(self.__path, m='new sentence')
            self.__git.push()
        except GitException as e:
            eprint(e)

    def write(self, append, epoch, sentence):
        if self.__new:
            self.__header()
            self.__push()
            self.__new = False
        if append:
            with open(self.__path, 'a') as output:
                output.write("%d %s\n" % (epoch, sentence))
            self.__push()
