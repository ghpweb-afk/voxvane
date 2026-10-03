/**
 * HTTP client for the VoxVane text-to-speech API.
 * It sends JSON and reads audio. It does not load a model.
 */

export class VoxVaneError extends Error {
  constructor(status, code, message) {
    super(message);
    this.name = "VoxVaneError";
    this.status = status;
    this.code = code;
  }
}

export class VoxVane {
  constructor({ apiKey, baseUrl = "https://api.voxvane.com", fetchImpl = globalThis.fetch, timeoutMs = 60000 } = {}) {
    if (!apiKey) throw new Error("apiKey is required");
    this.apiKey = apiKey;
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.fetchImpl = fetchImpl;
    this.timeoutMs = timeoutMs;
  }

  async voices() {
    return (await this.#json("GET", "/v1/voices")).voices;
  }

  async usage() {
    return this.#json("GET", "/v1/usage");
  }

  async textToSpeech(voiceId, text, { outputFormat = "mp3" } = {}) {
    const chunks = [];
    for await (const chunk of this.stream(voiceId, text, { outputFormat })) chunks.push(chunk);
    return concat(chunks);
  }

  async *stream(voiceId, text, { outputFormat = "mp3" } = {}) {
    const response = await this.#send("POST", `/v1/text-to-speech/${encodeURIComponent(voiceId)}/stream`, { text, output_format: outputFormat });
    if (!response.body) {
      yield new Uint8Array(await response.arrayBuffer());
      return;
    }
    const reader = response.body.getReader();
    while (true) {
      const { done, value } = await reader.read();
      if (done) return;
      if (value?.byteLength) yield value;
    }
  }

  async #json(method, path) {
    const response = await this.#send(method, path);
    return response.json();
  }

  async #send(method, path, body) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);
    try {
      const response = await this.fetchImpl(this.baseUrl + path, {
        method,
        headers: {
          Authorization: `Bearer ${this.apiKey}`,
          ...(body ? { "Content-Type": "application/json" } : {}),
        },
        body: body ? JSON.stringify(body) : undefined,
        signal: controller.signal,
      });
      if (!response.ok) {
        let code = "error", message = response.statusText;
        try {
          const payload = await response.json();
          code = payload.error?.code || code;
          message = payload.error?.message || message;
        } catch { /* non-JSON error body */ }
        throw new VoxVaneError(response.status, code, message);
      }
      return response;
    } finally {
      clearTimeout(timer);
    }
  }
}

function concat(chunks) {
  const length = chunks.reduce((sum, chunk) => sum + chunk.byteLength, 0);
  const out = new Uint8Array(length);
  let offset = 0;
  for (const chunk of chunks) {
    out.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return out;
}
