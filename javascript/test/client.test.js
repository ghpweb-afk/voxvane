import { createServer } from "node:http";
import test from "node:test";
import assert from "node:assert/strict";
import { VoxVane, VoxVaneError } from "../src/client.js";

function listen() {
  const server = createServer((req, res) => {
    if (req.url.startsWith("/v1/voices")) {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ voices: [{ voice_id: "aria", name: "VoxVane Aria" }] }));
      return;
    }
    if (req.url.includes("missing")) {
      res.writeHead(404, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: { code: "voice_not_found", message: "Unknown voice." } }));
      return;
    }
    res.writeHead(200, { "Content-Type": "audio/L16", "Transfer-Encoding": "chunked" });
    res.write("PCM");
    res.end("!");
  });
  return new Promise(resolve => server.listen(0, "127.0.0.1", () => resolve(server)));
}

test("javascript client returns audio and surfaces API errors", async () => {
  const server = await listen();
  const { port } = server.address();
  const client = new VoxVane({ apiKey: "vv_test_example", baseUrl: `http://127.0.0.1:${port}` });
  try {
    assert.equal((await client.voices())[0].name, "VoxVane Aria");
    const audio = await client.textToSpeech("aria", "Hello", { outputFormat: "pcm" });
    assert.equal(Buffer.from(audio).toString(), "PCM!");
    await assert.rejects(client.textToSpeech("missing", "Hello"), (error) => {
      assert.ok(error instanceof VoxVaneError);
      assert.equal(error.code, "voice_not_found");
      return true;
    });
  } finally {
    await new Promise(resolve => server.close(resolve));
  }
});
