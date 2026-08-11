#!/usr/bin/env python3
"""Serveur statique du site avec en-têtes anti-cache (Cache-Control: no-store).
Lancement : python3 serve.py (port 8080, dossier /root/consulting/site)
"""
import http.server, socketserver, os

os.chdir("/root/consulting/site")

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()
    def log_message(self, fmt, *args):
        pass

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", 8080), NoCacheHandler) as httpd:
    print("serveur anti-cache sur :8080")
    httpd.serve_forever()
