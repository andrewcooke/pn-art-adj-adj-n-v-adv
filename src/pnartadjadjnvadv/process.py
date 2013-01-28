
from multiprocessing import Queue, Process
from time import sleep

from pnartadjadjnvadv.gitfile import GitFile
from pnartadjadjnvadv.sentences import Sentences, key
from pnartadjadjnvadv.server import Server, repeat_text
from pnartadjadjnvadv.tweet import Tweet
from pnartadjadjnvadv.utils import latest, eprint
from pnartadjadjnvadv.words import Words


def run(path, twitter, port, static):
    new_sentences = Queue()
    targets = (sentence_process, server_process)
    args = ((path, twitter, new_sentences), (port, static, new_sentences))
    processes = ([None], [None])  # mutable 'pointers'
    while True:
        for target, arg, process in zip(targets, args, processes):
            if not process[0] or not process[0].is_alive():
                eprint('Starting %s' % target)
                process[0] = Process(target=target, args=arg)
                process[0].start()
        sleep(1)


def sentence_process(path, twitter, new_sentences):
    gf = GitFile(path)
    tw = Tweet(twitter)
    def write(append, epoch, sentence):
        gf.write(append, epoch, sentence)
        tw.write(append, epoch, sentence)
        new_sentences.put((epoch, sentence))
    Sentences(Words(), gf.read, write)()


def server_process(port, static, new_sentences):
    def update(texts, sentences):
        while not new_sentences.empty():
            epoch, sentence = new_sentences.get()
            if sentences:
                previous = latest(sentences)
                sentences[previous][1] = epoch  # mutate end
            eprint('%d: %s' % (epoch, sentence))
            sentences[key(sentence)] = [epoch, None, sentence]  # mutable end
            texts = None # flag to reset below
        if not texts: texts = repeat_text(sentences)
        return texts, sentences
    Server(port, static, update=update)()


if __name__ == '__main__':
#    test_static()
#    run('/tmp/sentences.txt', None, 8080, TEST_URL)
    run('/home/acooke/webapps/colorlessgreen/sentences.txt',
        '/home/acooke/twitter', 17492, 'http://acooke.org/cg/static')

