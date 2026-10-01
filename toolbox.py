#!/usr/bin/env python3
"""
Portable Toolbox
================
Static file server for modular tools.
"""

import http.server
import json
import socketserver
import sys
from datetime import datetime
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

    def do_POST(self):
        """Save endpoint for the vacances tool (same contract as the old FastAPI app)."""
        if self.path.rstrip('/') not in ('/sauvegarder', '/vacances/sauvegarder'):
            self.send_error(404, "Unknown POST endpoint")
            return
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            if not isinstance(data, dict):
                raise ValueError("Un objet JSON est attendu")
            annee = str(data.get('annee', datetime.now().year))
            donnees_annee = {k: v for k, v in data.items() if k != 'annee'}

            fichier = TOOLBOX_ROOT / 'vacances' / 'vacances.json'
            toutes_vacances = {}
            if fichier.exists():
                with open(fichier, 'r', encoding='utf-8') as f:
                    toutes_vacances = json.load(f)
                # Migration: ancien format (une seule année) -> format par année
                if isinstance(toutes_vacances, dict) and 'annee' in toutes_vacances:
                    ancienne_annee = str(toutes_vacances.pop('annee'))
                    toutes_vacances = {ancienne_annee: toutes_vacances}

            toutes_vacances[annee] = donnees_annee
            with open(fichier, 'w', encoding='utf-8') as f:
                json.dump(toutes_vacances, f, indent=4, ensure_ascii=False)
        except (ValueError, TypeError, OSError) as err:
            message = json.dumps({'status': 'error', 'detail': str(err)}).encode('utf-8')
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(message)))
            self.end_headers()
            self.wfile.write(message)
            return

        reponse = b'{"status": "success"}'
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(reponse)))
        self.end_headers()
        self.wfile.write(reponse)

class ToolboxServer(socketserver.TCPServer):
    """TCPServer that fails fast when the port is already taken.

    SO_REUSEADDR is deliberately NOT enabled on Windows: there it would
    allow a second server to bind onto a port that is already in use
    instead of raising an error.
    """
    allow_reuse_address = (sys.platform != 'win32')

def run_server(port, explicit_port=False):
    try:
        httpd = ToolboxServer(("", port), ToolboxHandler)
    except OSError as err:
        if explicit_port:
            print(f"\n  Error: port {port} is already in use. ({err})")
            print(f"\n  Stop the program using it, or run on another port, e.g.:")
            print(f"    python toolbox.py {port + 1}")
            sys.exit(1)
        # Default port busy: automatically start on the next free port.
        httpd = None
        for candidate in range(port + 1, port + 11):
            try:
                httpd = ToolboxServer(("", candidate), ToolboxHandler)
                break
            except OSError:
                continue
        if httpd is None:
            print(f"\n  Error: port {port} is already in use and no free port")
            print(f"  was found in the range {port + 1}-{port + 10}.")
            sys.exit(1)
        print(f"  Note: port {port} is already in use - using port {candidate} instead.\n")
        port = candidate

    with httpd:
        print(f"\n{'='*60}")
        print(f"  Toolbox")
        print(f"{'='*60}")
        print(f"\n  Server: http://localhost:{port}")
        print(f"\n  Tools:")
        for item in TOOLBOX_ROOT.iterdir():
            if item.is_dir() and not item.name.startswith(('_', '.')) and item.name != 'timer':
                print(f"    - {item.name}")
        print(f"    - timer")
        print(f"\n  Press Ctrl+C to stop")
        print(f"\n{'='*60}\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")

if __name__ == '__main__':
    explicit_port = False
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
            explicit_port = True
        except ValueError:
            pass
    run_server(PORT, explicit_port)