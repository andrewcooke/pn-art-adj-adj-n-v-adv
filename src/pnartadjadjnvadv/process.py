
from multiprocessing import Queue, Process

from pnartadjadjnvadv.gitfile import GitFile
from pnartadjadjnvadv.sentences import Sentences, key
from pnartadjadjnvadv.server import Server, test_static, TEST_URL
from pnartadjadjnvadv.utils import latest
from pnartadjadjnvadv.words import Words


def run(path, port, static):
    new_sentences = Queue()
    Process(target=sentence_process, args=(path, new_sentences)).start()
    Process(target=server_process, args=(port, static, new_sentences)).start()


def sentence_process(path, new_sentences):
    gf = GitFile(path)
    def write(append, epoch, sentence):
        gf.write(append, epoch, sentence)
        new_sentences.put((epoch, sentence))
    Sentences(Words(), gf.read, write)()


def server_process(port, static, new_sentences):
    def update(sentences):
        while not new_sentences.empty():
            epoch, sentence = new_sentences.get()
            if sentences:
                previous = latest(sentences)
                sentences[previous][1] = epoch
            print('%d: %s' % (epoch, sentence))
            k = key(sentence)
            sentences[k] = [epoch, None, sentence]
        return sentences
    Server(port, static, update=update)()


if __name__ == '__main__':
    test_static()
    run('/tmp/foo', 8080, TEST_URL)

