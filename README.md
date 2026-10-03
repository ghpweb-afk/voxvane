# VoxVane public SDK

This folder is the public text-to-speech SDK. It calls `https://api.voxvane.com` and returns audio bytes.

What is here:

| Path | What it is |
|---|---|
| `openapi/openapi.json` | The HTTP contract. The voxvane.com API reference is generated from this file. |
| `python/` | `voxvane.VoxVane`, stdlib only. |
| `javascript/` | `VoxVane` for Node 22, `fetch` only. |
| `docs/quickstart.md` | Install-later quickstart. |
| `examples/` | One Python script and one JavaScript script. |

The clients send JSON and receive audio bytes. They do not contain a model, a voice file, a pronunciation table, or a text normalizer. The hosted service that renders audio lives in the private `services/tts-api` tree, not in this folder.

```sh
# from this folder
PYTHONPATH=python python3 examples/python/hello.py
node examples/javascript/hello.mjs
```

Both examples expect `VOXVANE_API_KEY`. The clients are not on PyPI or npm yet. Text to speech is $0.012 per 1,000 characters.
