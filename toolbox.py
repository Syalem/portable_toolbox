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
        if self.path in ('/', '/index.html'):
            self.path = '/index.html'
        # Redirect tool roots to the tool's index.html, e.g.
        # /timer, /pdf-tools/ or /work_time_calculator -> /<tool>/index.html
        elif self.path.endswith('/'):
            self.path = self.path.rstrip('/') + '/index.html'
        elif '.' not in self.path.rsplit('/', 1)[-1]:
            # No file extension in the last segment: treat it as a tool folder
            if (TOOLBOX_ROOT / self.path.strip('/')).is_dir():
                self.path = self.path + '/index.html'
        super().do_GET()

    def do_POST(self):
        """Dispatch POST save endpoints to the tool that owns them."""
        route = self.path.rstrip('/')
        if route in ('/sauvegarder', '/vacances/sauvegarder'):
            self._handle_vacances_save()
        elif route == '/links/sauvegarder':
            self._handle_links_save()
        else:
            self.send_error(404, "Unknown POST endpoint")

    def _send_json(self, status, payload):
        message = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(message)))
        self.end_headers()
        self.wfile.write(message)

    def _read_json_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(content_length).decode('utf-8'))
        if not isinstance(data, dict):
            raise ValueError("Un objet JSON est attendu")
        return data

    def _handle_vacances_save(self):
        """Save endpoint for the vacances tool (same contract as the old FastAPI app)."""
        try:
            data = self._read_json_body()
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
            self._send_json(400, {'status': 'error', 'detail': str(err)})
            return

        self._send_json(200, {'status': 'success'})

    def _handle_links_save(self):
        """Save endpoint for the links tool: stores the whole list in links/links.json."""
        try:
            data = self._read_json_body()
            if not isinstance(data.get('links'), list):
                raise ValueError("Un objet JSON contenant une liste 'links' est attendu")
            fichier = TOOLBOX_ROOT / 'links' / 'links.json'
            with open(fichier, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except (ValueError, TypeError, OSError) as err:
            self._send_json(400, {'status': 'error', 'detail': str(err)})
            return

        self._send_json(200, {'status': 'success'})

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
        for item in sorted(TOOLBOX_ROOT.iterdir()):
            if item.is_dir() and not item.name.startswith(('_', '.')):
                print(f"    - {item.name}")
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