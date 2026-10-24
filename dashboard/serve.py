"""Serve the repository root locally so dashboard/index.html can read results/ and src/collect/targets.json.

Usage: python dashboard/serve.py [port]      then open http://localhost:8000/dashboard/
Binds to 127.0.0.1 only. Scaffold: the "run pipeline" action (job queue + worker restricted to the curated
targets in src/collect/targets.json) is future work; see dashboard/README.md.
"""
import functools
import http.server
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
    print(f"Serving {ROOT} at http://localhost:{port}/dashboard/  (Ctrl+C to stop)")
    httpd.serve_forever()
