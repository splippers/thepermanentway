#!/usr/bin/env python3
"""Small annotation server for a tablet and stylus.

Serves the images in ./images, lets you draw on them in the browser, and saves
the annotated PNG plus the stroke data (in image pixels) to ./annotations.

    python3 server.py [port]

It listens on all interfaces so a tablet on the same network can reach it. A random
token is printed with the URL and is required for everything except the page itself,
so other devices on the network cannot read or write files without it.
"""
import base64, json, mimetypes, os, re, secrets, socket, sys, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs, unquote

ROOT = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(ROOT, 'images')
OUT = os.path.join(ROOT, 'annotations')
TOKEN = os.environ.get('ANNOTATE_TOKEN') or secrets.token_urlsafe(9)
EXT = ('.png', '.jpg', '.jpeg', '.webp')
MAX_BODY = 40 * 1024 * 1024


def safe(name):
    return re.sub(r'[^A-Za-z0-9._-]+', '_', os.path.basename(name)).strip('._') or 'file'


class H(BaseHTTPRequestHandler):
    def log_message(self, fmt, *a):
        sys.stderr.write('%s %s\n' % (self.address_string(), fmt % a))

    def _send(self, code, body, ctype='application/json'):
        if isinstance(body, str):
            body = body.encode()
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def _auth(self, q):
        if secrets.compare_digest(q.get('k', [''])[0], TOKEN):
            return True
        self._send(403, '{"error":"missing or wrong token"}')
        return False

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path in ('/', '/index.html'):
            with open(os.path.join(ROOT, 'index.html'), 'rb') as f:
                return self._send(200, f.read(), 'text/html; charset=utf-8')
        if not self._auth(q):
            return
        if u.path == '/api/images':
            names = sorted(n for n in os.listdir(IMAGES) if n.lower().endswith(EXT))
            return self._send(200, json.dumps(names))
        if u.path == '/api/saved':
            names = sorted(os.listdir(OUT)) if os.path.isdir(OUT) else []
            return self._send(200, json.dumps(names))
        if u.path.startswith('/images/') or u.path.startswith('/annotations/'):
            base = IMAGES if u.path.startswith('/images/') else OUT
            p = os.path.join(base, safe(unquote(u.path.split('/', 2)[2])))
            if os.path.isfile(p):
                with open(p, 'rb') as f:
                    return self._send(200, f.read(), mimetypes.guess_type(p)[0] or 'application/octet-stream')
        self._send(404, '{"error":"not found"}')

    def do_POST(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if not self._auth(q):
            return
        n = int(self.headers.get('Content-Length') or 0)
        if n <= 0 or n > MAX_BODY:
            return self._send(413, '{"error":"bad size"}')
        body = self.rfile.read(n)
        if u.path == '/api/save':
            d = json.loads(body)
            stem = safe(os.path.splitext(d.get('image', 'image'))[0])
            stamp = time.strftime('%Y%m%d-%H%M%S')
            os.makedirs(OUT, exist_ok=True)
            png = d['png'].split(',', 1)[1]
            with open(os.path.join(OUT, f'{stem}-{stamp}.png'), 'wb') as f:
                f.write(base64.b64decode(png))
            meta = {k: d.get(k) for k in ('image', 'note', 'strokes', 'width', 'height')}
            with open(os.path.join(OUT, f'{stem}-{stamp}.json'), 'w') as f:
                json.dump(meta, f)
            return self._send(200, json.dumps({'saved': f'annotations/{stem}-{stamp}.png'}))
        if u.path == '/api/upload':
            name = safe(q.get('name', ['upload.jpg'])[0])
            if not name.lower().endswith(EXT):
                return self._send(400, '{"error":"png, jpg or webp only"}')
            with open(os.path.join(IMAGES, name), 'wb') as f:
                f.write(body)
            return self._send(200, json.dumps({'uploaded': name}))
        self._send(404, '{"error":"not found"}')


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        return s.getsockname()[0]
    except OSError:
        return '127.0.0.1'
    finally:
        s.close()


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8800
    os.makedirs(IMAGES, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    print(f'Annotator: http://{lan_ip()}:{port}/?k={TOKEN}', flush=True)
    ThreadingHTTPServer(('0.0.0.0', port), H).serve_forever()
