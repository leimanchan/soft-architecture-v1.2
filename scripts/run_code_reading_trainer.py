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

    handler = http.server.SimpleHTTPRequestHandler
    # Change directory once so relative static paths resolve.
    import os
    os.chdir(str(docs_manifesto))

    for port in (8012, 8013, 8014, 8080):
        try:
            with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
                print(f"Serving trainer at http://127.0.0.1:{port}/{index_name}")
                print("Press Ctrl+C to stop.")
                httpd.serve_forever()
        except OSError:
            continue

    print("Could not bind a local port (tried 8012, 8013, 8014, 8080).")
    print("You can open the file directly in a browser:")
    print(docs_manifesto / index_name)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
