#!/usr/bin/env python3
"""Run a local static server for the code reading trainer."""

from __future__ import annotations

import http.server
import socketserver
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    docs_manifesto = root / "docs" / "manifesto"
    index_name = "code-reading-trainer.html"
    if not (docs_manifesto / index_name).exists():
        print(f"Missing {docs_manifesto / index_name}")
        return 1

    port = 8012
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        print(f"Serving trainer at http://127.0.0.1:{port}/{index_name}")
        print("Press Ctrl+C to stop.")
        # Change directory once so relative static paths resolve.
        import os
        os.chdir(str(docs_manifesto))
        httpd.serve_forever()


if __name__ == "__main__":
    raise SystemExit(main())
