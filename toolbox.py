#!/usr/bin/env python3
"""
Portable Toolbox
================
A collection of everyday tools that runs from a USB key.
No installation required - just Python!

Usage:
    python toolbox.py [PORT]

Default port: 8080
Open: http://localhost:8080
"""

import http.server
import socketserver
import sys
from pathlib import Path

PORT = 8080
TOOLBOX_ROOT = Path(__file__).parent

class ToolboxHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve the toolbox and all tools."""

    def do_GET(self):
        path = self.path.strip('/')

        if path == '' or path == 'index.html':
            self.serve_file(TOOLBOX_ROOT / 'index.html')
        elif path in ['timer', 'timer/', 'timer/index.html']:
            self.serve_file(TOOLBOX_ROOT / 'timer' / 'timer.py', as_html=True)
        elif '/' in path:
            parts = path.split('/')
            tool_dir = TOOLBOX_ROOT / parts[0]
            if tool_dir.exists():
                target_file = tool_dir / '/'.join(parts[1:])
                if target_file.exists():
                    self.serve_file(target_file)
                else:
                    self.serve_404()
            else:
                self.serve_404()
        elif path and (TOOLBOX_ROOT / path).exists():
            tool_dir = TOOLBOX_ROOT / path
            if tool_dir.is_dir():
                index_file = tool_dir / 'index.html'
                if index_file.exists():
                    self.serve_file(index_file)
                else:
                    self.send_response(302)
                    self.send_header('Location', f'/{path}/')
                    self.end_headers()
            else:
                self.serve_file(tool_dir)
        else:
            self.serve_404()

    def serve_file(self, file_path, as_html=False):
        if not file_path.exists():
            self.serve_404()
            return

        with open(file_path, 'rb') as f:
            content = f.read()

        if as_html and file_path.suffix == '.py':
            import importlib.util
            spec = importlib.util.spec_from_file_location("tool_module", file_path)
            module = importlib.util.module_from_spec(spec)
            sys.path.insert(0, str(file_path.parent))
            try:
                spec.loader.exec_module(module)
                if hasattr(module, 'TimerHandler'):
                    handler = module.TimerHandler(None, None, None)
                    if hasattr(handler, 'generate_timer_html'):
                        content = handler.generate_timer_html().encode('utf-8')
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html; charset=utf-8')
                        self.send_header('Content-Length', str(len(content)))
                        self.end_headers()
                        self.wfile.write(content)
                        return
            except Exception as e:
                print(f"Error loading module: {e}")
            finally:
                if str(file_path.parent) in sys.path:
                    sys.path.remove(str(file_path.parent))

        content_type = 'text/html' if file_path.suffix in ['.html', '.htm'] else \
                      'text/plain'
        if file_path.suffix == '.py':
            content_type = 'text/plain'

        self.send_response(200)
        self.send_header('Content-type', f'{content_type}; charset=utf-8')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def serve_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>404 - Toolbox</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            margin: 0;
            padding: 20px;
            text-align: center;
        }
        h1 { font-size: 5rem; color: #00d4ff; margin-bottom: 20px; }
        p { font-size: 1.2rem; color: #888; margin-bottom: 30px; }
        a {
            display: inline-block;
            background: linear-gradient(135deg, #00d4ff, #0099cc);
            color: #000;
            padding: 15px 30px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            transition: transform 0.3s;
        }
        a:hover { transform: scale(1.05); }
    </style>
</head>
<body>
    <div>
        <h1>404</h1>
        <p>Page not found in the toolbox</p>
        <a href="/">Return to Toolbox</a>
    </div>
</body>
</html>'''
        self.wfile.write(html.encode('utf-8'))

def run_server(port):
    handler = ToolboxHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"\n{'='*60}")
        print(f"  Toolbox")
        print(f"{'='*60}")
        print(f"\n  Server running at: http://localhost:{port}")
        print(f"  Toolbox root: {TOOLBOX_ROOT}")
        print(f"\n  Available tools:")
        tools = []
        for item in TOOLBOX_ROOT.iterdir():
            if item.is_dir() and not item.name.startswith('_'):
                tools.append(f"    - {item.name}")
        if tools:
            print('\n'.join(tools))
        else:
            print("    No tools found.")
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