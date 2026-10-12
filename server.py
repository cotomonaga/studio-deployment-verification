from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    counter = 0
    def do_GET(self):
        if self.path == '/healthz':
            body = b'{"ok":true}'
            mime = 'application/json'
        else:
            body = ('<!doctype html><html lang="ja"><meta charset="utf-8"><title>Studio deployment verification</title><h1>Studio deployment verification</h1><p>Disposable test application. No business data.</p><form method="post" action="/check"><button>動作を確認</button></form></html>').encode()
            mime = 'text/html; charset=utf-8'
        self.send_response(200); self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_POST(self):
        if self.path != '/check':
            self.send_error(404); return
        type(self).counter += 1
        body = json.dumps({'ok': True, 'operationCount': self.counter}).encode()
        self.send_response(200); self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)

HTTPServer(('0.0.0.0', 8080), Handler).serve_forever()
