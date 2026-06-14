"""
mock_server/server.py
----------------------
A lightweight mock REST API server for local testing.
Receives detection events and saves annotated images to disk.

Run this in a separate terminal before running main.py:
  python mock_server/server.py

Then set API_ENDPOINT in api/handler.py to:
  http://localhost:5000/api/detections
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import json
import os
import datetime

SAVE_DIR = "mock_server/received_frames"
os.makedirs(SAVE_DIR, exist_ok=True)


class DetectionHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == "/api/detections":
            content_type = self.headers.get("Content-Type", "")
            ctype, pdict = cgi.parse_header(content_type)

            if ctype == "multipart/form-data":
                pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
                fields = cgi.parse_multipart(self.rfile, pdict)

                # ── Extract image ─────────────────────────────────────────────
                image_data = fields.get("image", [None])[0]
                metadata_str = fields.get("metadata", ["{}"])[0]
                metadata = json.loads(metadata_str)

                # ── Save annotated frame to disk ──────────────────────────────
                if image_data:
                    filename = f"{SAVE_DIR}/detection_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
                    with open(filename, "wb") as f:
                        f.write(image_data)
                    print(f"\n[MockServer] Frame saved: {filename}")

                # ── Print metadata ────────────────────────────────────────────
                print(f"[MockServer] Metadata received:")
                print(json.dumps(metadata, indent=2))

                # ── Send 200 OK ───────────────────────────────────────────────
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "received"}).encode())

            else:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress default HTTP logs for cleaner output


if __name__ == "__main__":
    server = HTTPServer(("localhost", 5000), DetectionHandler)
    print("[MockServer] Running at http://localhost:5000")
    print("[MockServer] Waiting for detection events...")
    server.serve_forever()
