"""Write one MP3. Requires VOXVANE_API_KEY. Does not load a model."""
import os
from voxvane import VoxVane

client = VoxVane(api_key=os.environ["VOXVANE_API_KEY"])
with open("hello.mp3", "wb") as audio:
    audio.write(client.text_to_speech("aria", "Hello from VoxVane.", output_format="mp3"))
print("wrote hello.mp3")
