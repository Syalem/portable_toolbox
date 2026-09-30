#!/usr/bin/env python3
"""
Portable Toolbox
================
Static file server for modular tools.
"""

import http.server
import socketserver
import sys
from pathlib import Path

PORT = 8080
TOOLBOX_ROOT = Path(__file__).parent

class ToolboxHandler(http.server.SimpleHTTPRequestHandler):
    """Serve static files from toolbox root."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(TOOLBOX_ROOT), **kwargs)

    def do_GET(self):
        # Redirect root to index.html
        if self.path == '/' or self.path == '/index.html':
            self.path = '/index.html'
        # Redirect tool root to tool's index.html
        elif self.path.endswith('/') or self.path == '/timer':
            self.path = self.path.rstrip('/') + '/index.html'
        super().do_GET()

def run_server(port):
    handler = ToolboxHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"\n{'='*60}")
        print(f"  Toolbox")
        print(f"{'='*60}")
        print(f"\n  Server: http://localhost:{port}")
        print(f"\n  Tools:")
        for item in TOOLBOX_ROOT.iterdir():
            if item.is_dir() and not item.name.startswith('_') and item.name != 'timer':
                print(f"    - {item.name}")
        print(f"    - timer")
        print(f"\n  Press Ctrl+C to stop")
        print(f"\n{'='*60}\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            pass
    run_server(PORT)