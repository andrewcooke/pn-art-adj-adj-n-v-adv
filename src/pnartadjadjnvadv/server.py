
from urllib.parse import quote, unquote
from collections import OrderedDict
from os import chdir
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from threading import Thread

from pnartadjadjnvadv.sentences import Sentences, PERIOD, key
from pnartadjadjnvadv.utils import latest_dict
from pnartadjadjnvadv.words import Words


class Server(HTTPServer):

    '''
    This displays the information given in the OrderedDict sentences, which
    maps from key(text) to (start, end, text).  The key function is defined
    in the sentences module.

    The entries should be ordered by time, with the latest (end=None) last.

    The ordered dict is modified by the update function (note that to update
    the end time of the 'previous' value it is probably going to need to store
    the tripe as a list, not a tuple).
    '''

    def __init__(self, port, static, sentences=OrderedDict(), update=lambda x: x):
        self.__static = static
        self.sentences = sentences
        self.__update = update
        self.static_content = self._build_static()
        super().__init__(('0.0.0.0', port), Handler)

    def update(self):
        self.sentences = self.__update(self.sentences)

    def __call__(self, test=False):
        self.serve_forever(poll_interval=0.5 if test else 60)

    def _build_static(self):
        return {'about': self.__static_page('''
<p>From an <a href="http://rachelbythebay.com/w/2012/08/29/info/">idea</a> by Rachel Kroll.</p>
<p>A new timestamp is generated every {period:d} seconds (roughly), posted to
<a href="">Twitter</a>, and archived on
<a href="https://github.com/andrewcooke/pn-art-adj-adj-n-v-adv/blob/master/sentences.txt">GitHub</a>.
Sentences are selected from a pool ~50 bits in size.</p>
<p>Dates are displayed in your browser's timezone.</p>
<p>(c) 2013 <a href="http://www.acooke.org">Andrew Cooke</a>.
Source <a href="https://github.com/andrewcooke/pn-art-adj-adj-n-v-adv">available</a> under the AGPL3.</p>
''', title='About')}

    def format(self, body, **kargs):
        substitution = dict(kargs)
        substitution.update(static=self.__static, period=PERIOD)
        return ('''<!DOCTYPE html>
<html>
<head>
<title>{title!s}</title>
<link rel="stylesheet" type="text/css" href="{static!s}/style.css">
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
<script type="text/javascript" src="{static!s}/epoch.js"></script>
</head>
<body>
<p class="links"><a href="./about">about</a> | <a href="./">current</a></p>
%s
</body>''' % body).format(**substitution)

    def __static_page(self, body, **kargs):
        message = self.format(body, **kargs)
        return lambda handler: handler.send(message)


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = unquote(self.path)
        if path.startswith('/'): path = path[1:]
        if path in self.server.static_content:
            self.server.static_content[path](self)
        else:
            self.server.update()
            try:
                self._lookup(self.server.sentences[key(path)])
            except KeyError:
                if path:
                    self._not_found()
                else:
                    self._current()

    def send(self, html):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def _lookup(self, data):
        start, end, sentence = data
        self.send(self.server.format('''
<p class="sentence">{sentence!s}</p>
<p class="date"><span class="epoch">{start!s}</span> &mdash; <span class="epoch">{end!s}</span>.</p>
''', start=start, end=end, sentence=sentence, title='Timestamp lookup'))

    def _current(self):
        start, end, sentence = latest_dict(self.server.sentences)
        if end: self._not_found() # current should have an open endpoint
        self.send(self.server.format('''
<p class="sentence"><a href="./{encoded!s}">{sentence!s}</a></p>
''', sentence=sentence, encoded=quote(sentence), title='Current timestamp'))

    def _not_found(self):
        self.send_response_only(404)


TEST_URL = 'http://localhost:8081'

def test_static():
    chdir('/home/andrew/project/wordstamp/git/static')
    static = HTTPServer(('0.0.0.0', 8081), SimpleHTTPRequestHandler)
    Thread(target=static.serve_forever).start()


if __name__ == '__main__':
    test_static()
    words = Words()
    sentence = words.sentence()
    Server(8080, TEST_URL, OrderedDict([(key(sentence), (123456, None, sentence))]))()
