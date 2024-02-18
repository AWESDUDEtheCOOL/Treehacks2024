from customtkinter import *


import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write
import tkinter as tk
from threading import Thread
import numpy as np
import queue
import os
from transformers import pipeline

transcriber = pipeline(model="openai/whisper-base")

fs = 44100  # Sample rate

AUDIO_FILENAME = "audiooutput.wav"
TEXT_FILENAME = "audiooutput.txt"

if os.path.exists(AUDIO_FILENAME):
    os.remove(AUDIO_FILENAME)
if os.path.exists(TEXT_FILENAME):
    os.remove(TEXT_FILENAME)


def transcribe(filename=AUDIO_FILENAME):
    result = transcriber(filename)

    text = result["text"].strip()
    with open(TEXT_FILENAME, "w") as f:
        f.write(text)

    return text


class Recorder:
    def __init__(self, master):
        self.master = master
        self.master.title = "Transcribe your thoughts"
        self.master.config(bg="skyblue")

        self.recording = False
        self.q = queue.Queue()

        self.start_button = tk.Button(
            master, text="Start Recording", command=self.start_recording
        )
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(
            master,
            text="Stop Recording",
            command=self.stop_recording,
            state=tk.DISABLED,
        )
        self.stop_button.pack(pady=10)

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        self.q.put(indata.copy())

    def start_recording(self):
        print("Starting recording...")
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.record_thread = Thread(target=self.record)
        self.record_thread.start()

    def stop_recording(self):
        self.recording = False
        print("Stopping recording.")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        print(transcribe())

    def record(self):
        with sf.SoundFile(
            AUDIO_FILENAME,
            mode="x",
            samplerate=fs,
            channels=1,
        ) as file:
            with sd.InputStream(samplerate=fs, channels=1, callback=self.callback):
                while self.recording:
                    file.write(self.q.get())

    def save_recording(self, filename):
        write(filename, fs, self.audio_data)


if __name__ == "__main__":
    root = tk.Tk()
    app = Recorder(root)
    root.mainloop()
