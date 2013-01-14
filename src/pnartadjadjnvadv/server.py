
from http.server import HTTPServer, BaseHTTPRequestHandler

from pnartadjadjnvadv.sentences import Sentences, PERIOD
from pnartadjadjnvadv.words import Words


class Server(HTTPServer):

    def __init__(self, port, sentences, static, test=False):
        self.sentences = sentences
        self._static = static
        self.static_content = self._build_static()
        super().__init__(('0.0.0.0', port), Handler)
        self.serve_forever(poll_interval=0.5 if test else 60)

    def _build_static(self):
        return {'about': self._static_page('''
<p>From an <a href="http://rachelbythebay.com/w/2012/08/29/info/">idea</a> by Rachel Kroll.</p>
<p>A new timestamp is generated approximately every {period:d} seconds, posted to
<a href="">Twitter</a>, and archived on
<a href="">GitHub</a>.
It is selected from a pool approximately 52 bits in size.</p>
<p>(c) 2013 <a href="http://www.acooke.org">Andrew Cooke</a>.</p>
''', title='About')}

    def _format(self, body, **kargs):
        substitution = dict(kargs)
        substitution.update(static=self._static, period=PERIOD)
        return ('''<!DOCTYPE html>
<html>
<head>
<title>{title!s}</title>
<link rel="stylesheet" type="text/css" href="{static!s}/style.css">
<script type="text/javascript" src="{static!s}/epoch.js"></script>
</head>
<body>
<p class="links"><a href="./about">about</a> | <a href="./">current</a></p>
%s
</body>''' % body).format(**substitution)

    def _static_page(self, body, **kargs):
        message = self._format(body, **kargs)
        return lambda handler: handler.send(message)


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/'): self.path = self.path[1:]
        print(self.path)
        if self.path in self.server.static_content:
            self.server.static_content[self.path](self)
        else:
            try:
                self._lookup(self.server.sentences[self.path])
            except KeyError:
                if self.path:
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
        self.send(self.server._format('''
<p class="sentence">{sentence!s}</p>
<p class="date"><span class="epoch">{start!s}</span> - <span class="epoch">{end!s}</span></p>
''', start=start, end=end, sentence=sentence, title='Timestamp lookup'))

    def _current(self):
        self.send(self.server._format('''
<p class="sentence"><a href="./{sentence!s}">{sentence!s}</a></p>
''', sentence=self.server.sentences.current_sentence(), title='Current timestamp'))

    def _not_found(self):
        self.send_response_only(404)


if __name__ == '__main__':
    words = Words()
    Server(8080, Sentences([(123456, words.sentence())]), 'file:///home/andrew/project/wordstamp/git/static')
