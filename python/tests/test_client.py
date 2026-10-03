"""The public client talks HTTP only. No model imports."""
from __future__ import annotations

import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from voxvane import VoxVane, VoxVaneError


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def do_GET(self):
        if self.path == "/v1/voices":
            body = json.dumps({"voices": [{"voice_id": "aria", "name": "VoxVane Aria"}]}).encode()
        else:
            body = json.dumps({"requests": 1, "characters": 5, "audio_seconds": 0.2, "priced": False, "price_version": "unpriced"}).encode()
        self._send(200, "application/json", body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        self.rfile.read(length)
        if "bad" in self.path:
            body = json.dumps({"error": {"code": "voice_not_found", "message": "Unknown voice."}}).encode()
            self._send(404, "application/json", body)
            return
        self._send(200, "audio/L16", b"PCM!")

    def _send(self, status, mime, body):
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)


class ClientTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.client = VoxVane("vv_test_example", base_url=f"http://127.0.0.1:{cls.httpd.server_address[1]}")

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def test_voices_usage_and_audio(self):
        self.assertEqual(self.client.voices()[0]["voice_id"], "aria")
        self.assertEqual(self.client.usage()["characters"], 5)
        self.assertEqual(self.client.text_to_speech("aria", "Hello", output_format="pcm"), b"PCM!")

    def test_errors_do_not_invent_a_model_payload(self):
        with self.assertRaises(VoxVaneError) as caught:
            self.client.text_to_speech("bad", "Hello")
        self.assertEqual(caught.exception.status, 404)
        self.assertEqual(caught.exception.code, "voice_not_found")


if __name__ == "__main__":
    unittest.main()
