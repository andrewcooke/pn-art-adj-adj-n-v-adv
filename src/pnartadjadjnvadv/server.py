
from http.server import HTTPServer, BaseHTTPRequestHandler
from pnartadjadjnvadv.sentences import Sentences


class Server(HTTPServer):

    def __init__(self, port, sentences, static, test=False):
        self._sentences = sentences
        self._static = self._build_static(static)
        super().__init__(('0.0.0.0', port), Handler)
        self.serve_forever(poll_interval=0.5 if test else 60)

    def _build_static(self, static):
        return {'about': self._static_page('''
<p>From an <a href="http://rachelbythebay.com/w/2012/08/29/info/">idea</a>
by Rachel Kroll.</p>
<p>A new timestamp is generated approximately every XXX seconds,
posted to <a href="">Twitter</a>,
and archived on <a href="">GitHub</a>.
It is selected from a pool approximately 52 bits in size.</p>
<p>(c) 2013 <a href="http://www.acooke.org">Andrew Cooke</a>.</p>
''',)}

    def _static_page(self, html):
        message = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
</head>
<body>
%s
</body>''' % html
        def render(handler):
            handler.send_response(200)
            handler.send_header('Content-type', 'text-html')
            handler.end_headers()
            handler.wfile.write(message.encode('utf-8'))
        return render


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/'): self.path = self.path[1:]
        print(self.path)
        if self.path in self.server._static:
            self.server._static[self.path](self)
        else:
            try:
                self._lookup(self.server._sentences[self.path])
            except ValueError:
                if self.path:
                    self.not_found()
                else:
                    self.current()

    def _lookup(self, data):
        start, end, sentence = data



if __name__ == '__main__':
    Server(8080, Sentences([]), 'http://www.acooke.org/npxstatic/')
