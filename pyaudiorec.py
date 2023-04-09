import tkinter as tk
import pyaudio
import wave

class AudioRecorder:
    def __init__(self, master):
        self.master = master
        self.frames = []

        # GUI elements
        self.record_button = tk.Button(master, text="Record", command=self.record, height=2, width=10, font=("Helvetica", 14))
        self.stop_button = tk.Button(master, text="Stop", command=self.stop, state=tk.DISABLED, height=2, width=10, font=("Helvetica", 14))
        self.seconds_entry = tk.Entry(master, font=("Helvetica", 14))
        self.seconds_label = tk.Label(master, text="Seconds to Record:", font=("Helvetica", 14))
        self.seconds_entry.insert(0, "5")
        self.filename_entry = tk.Entry(master, font=("Helvetica", 14))
        self.filename_label = tk.Label(master, text="Output File Name:", font=("Helvetica", 14))
        self.filename_entry.insert(0, "output.wav")
        self.record_button.pack(pady=10)
        self.stop_button.pack(pady=10)
        self.seconds_label.pack(pady=10)
        self.seconds_entry.pack(pady=10)
        self.filename_label.pack(pady=10)
        self.filename_entry.pack(pady=10)

        # Audio parameters
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024

    def record(self):
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.RECORD_SECONDS = int(self.seconds_entry.get())
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                                      rate=self.RATE, input=True,
                                      frames_per_buffer=self.CHUNK,
                                      stream_callback=self.callback)
        self.stream.start_stream()

    def stop(self):
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.save_recording()

    def save_recording(self):
        filename = self.filename_entry.get()
        waveFile = wave.open(filename, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()
        print("Recording saved to " + filename)

    def callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        if len(self.frames) >= int(self.RATE / self.CHUNK * self.RECORD_SECONDS):
            return (in_data, pyaudio.paComplete)
        else:
            return (in_data, pyaudio.paContinue)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Audio Recorder")
    root.geometry("400x400")
    root.configure(bg="black")
    recorder = AudioRecorder(root)
    root.mainloop()
