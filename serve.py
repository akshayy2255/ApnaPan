#!/usr/bin/env python3
"""
ApnaPan — local development server.

    python3 serve.py              → serves this folder on http://localhost:8000
    python3 serve.py 8080         → pick your own port
    python3 serve.py 8080 --no-open

Nicer than `python3 -m http.server` because it:
  • serves index.html for "/" and for any directory
  • shows 404.html for missing pages instead of a bare error
  • sends correct MIME types for .woff2 and .webp
  • sends no-cache headers, so a normal refresh always shows your edits
  • picks the next free port if the one you asked for is taken
  • opens your browser automatically

Nothing here is needed in production — any static host serves these files as-is.
"""
import argparse
import functools
import http.server
import mimetypes
import os
import socket
import socketserver
import sys
import threading
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))

mimetypes.add_type("font/woff2", ".woff2")
mimetypes.add_type("font/woff", ".woff")
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("text/javascript", ".js")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        # Always show the latest build on refresh.
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            page = os.path.join(ROOT, "404.html")
            if os.path.exists(page):
                with open(page, "rb") as f:
                    body = f.read()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                if self.command != "HEAD":
                    self.wfile.write(body)
                return
        super().send_error(code, message, explain)

    def log_message(self, fmt, *args):
        # Quieter than the default: one compact line per request.
        sys.stderr.write("  %s\n" % (fmt % args))


def free_port(start):
    for port in range(start, start + 25):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue
    raise SystemExit("No free port found in range %d-%d" % (start, start + 25))


def main():
    ap = argparse.ArgumentParser(description="Serve the ApnaPan site locally.")
    ap.add_argument("port", nargs="?", type=int, default=8000)
    ap.add_argument("--no-open", action="store_true", help="do not open a browser window")
    args = ap.parse_args()

    if not os.path.exists(os.path.join(ROOT, "index.html")):
        raise SystemExit("index.html not found. Run this from the folder that contains it "
                         "(the apnapan folder), or rebuild with: python3 _build/build.py")

    port = free_port(args.port)
    url = "http://localhost:%d/" % port

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("0.0.0.0", port), Handler) as httpd:
        print("")
        print("  ApnaPan — Real Food · True Care · Live More")
        print("  " + "-" * 58)
        print("  Serving : %s" % ROOT)
        print("  Open    : %s" % url)
        print("  Pages   : index · shop · impact · story · how-it-works · farmers")
        print("            careers · blog · contact · products/ · checkout")
        print("  Stop    : Ctrl + C")
        print("  " + "-" * 58)
        print("  Sample content — read README.md > 'Replace before you go live'")
        print("")
        if not args.no_open:
            threading.Timer(0.6, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Stopped. Bye.\n")


if __name__ == "__main__":
    main()
