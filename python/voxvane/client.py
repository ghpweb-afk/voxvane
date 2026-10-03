"""HTTP client for the VoxVane text-to-speech API.

This module does not load a model. Point base_url at the hosted API.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from urllib.parse import quote


class VoxVaneError(Exception):
    def __init__(self, status: int, code: str, message: str):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message


class VoxVane:
    def __init__(self, api_key: str, base_url: str = "https://api.voxvane.com", timeout: float = 60):
        if not api_key:
            raise ValueError("api_key is required")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def voices(self) -> list[dict]:
        return self._json("GET", "/v1/voices")["voices"]

    def usage(self) -> dict:
        return self._json("GET", "/v1/usage")

    def text_to_speech(self, voice_id: str, text: str, output_format: str = "mp3") -> bytes:
        return b"".join(self.stream(voice_id, text, output_format=output_format))

    def stream(self, voice_id: str, text: str, output_format: str = "mp3"):
        path = f"/v1/text-to-speech/{quote(voice_id, safe='')}/stream"
        yield from self._chunks("POST", path, {"text": text, "output_format": output_format})

    def _json(self, method: str, path: str) -> dict:
        body = b"".join(self._chunks(method, path, None))
        return json.loads(body.decode())

    def _chunks(self, method: str, path: str, payload):
        data = None if payload is None else json.dumps(payload).encode()
        request = urllib.request.Request(
            self.base_url + path,
            data=data,
            method=method,
            headers={"Authorization": f"Bearer {self.api_key}", "Accept": "*/*", **({"Content-Type": "application/json"} if data else {})},
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                while True:
                    chunk = response.read(1024)
                    if not chunk:
                        break
                    yield chunk
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode()
            try:
                parsed = json.loads(raw)["error"]
                raise VoxVaneError(exc.code, parsed.get("code", "error"), parsed.get("message", raw)) from None
            except (json.JSONDecodeError, KeyError, TypeError):
                raise VoxVaneError(exc.code, "error", raw or exc.reason) from None
