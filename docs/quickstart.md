# Quickstart

Base URL: `https://api.voxvane.com`. Text to speech is $0.012 per 1,000 characters.

## Key

```sh
export VOXVANE_API_KEY="your-key-here"
```

Send it as `Authorization: Bearer`. Keep it on a server you control.

## curl

```sh
curl -X POST https://api.voxvane.com/v1/text-to-speech/aria \
  -H "Authorization: Bearer $VOXVANE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello from VoxVane.", "output_format": "mp3"}' \
  --output hello.mp3
```

`output_format` is `mp3` (default), `wav`, `pcm` (16-bit, 24000 Hz, mono), or `mulaw_8000` (8000 Hz mu-law).

Streaming uses the same body on `POST /v1/text-to-speech/aria/stream`.

## Python

From a checkout of this SDK:

```python
import os
from voxvane import VoxVane

client = VoxVane(api_key=os.environ["VOXVANE_API_KEY"])
open("hello.mp3", "wb").write(client.text_to_speech("aria", "Hello from VoxVane."))
```

## JavaScript

```javascript
import { writeFile } from "node:fs/promises";
import { VoxVane } from "voxvane";

const client = new VoxVane({ apiKey: process.env.VOXVANE_API_KEY });
await writeFile("hello.mp3", await client.textToSpeech("aria", "Hello from VoxVane."));
```

## Voices and usage

`GET /v1/voices` lists voice ids, names and languages. `GET /v1/usage` returns characters, audio seconds and `customer_usd`. The price is $0.012 per 1,000 characters (`priced: true`, `price_version` `2026-10-03`).
