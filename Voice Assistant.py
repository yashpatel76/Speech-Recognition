import vosk
import pyaudio
import json
import time

model = vosk.Model("E:\Tranning project\College Training\Internship Projects\Speech_Recognition/vosk-model-small-en-us-0.15")

recognizer = vosk.KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
stream.start_stream()

print("Listening...")

last_result = ""
last_time = time.time()

try:
    while True:
        data = stream.read(4096,exception_on_overflow=False)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = json.loads(result).get("text", "")
            current_time = time.time()
            if text.strip():    
                print(f"{text}")
                last_result = text
                last_time = current_time

except KeyboardInterrupt:
    print("Stopped by user")

stream.stop_stream()
stream.close()
p.terminate()
