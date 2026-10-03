import { writeFile } from "node:fs/promises";
import { VoxVane } from "../../javascript/src/client.js";

const client = new VoxVane({ apiKey: process.env.VOXVANE_API_KEY });
await writeFile("hello.mp3", await client.textToSpeech("aria", "Hello from VoxVane.", { outputFormat: "mp3" }));
console.log("wrote hello.mp3");
