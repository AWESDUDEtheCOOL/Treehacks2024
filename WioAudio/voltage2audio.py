import numpy as np
import wave

# Sample audio analog voltages (replace this with your actual data)
audio_data = np.array([0.5, 0.7, 0.3, 0.9, 0.2, 0.6])

# Scale the voltages to fit within the range [-32767, 32767] (16-bit signed integer)
scaled_data = np.int16(audio_data * 32767)

# Open a new WAV file
output_file = wave.open("output_audio.wav", "w")

# Set the parameters for the WAV file
output_file.setnchannels(1)  # Mono
output_file.setsampwidth(2)  # 16 bits per sample
output_file.setframerate(44100)  # Sample rate, e.g., CD quality

# Write the audio data to the file
output_file.writeframes(scaled_data.tobytes())

# Close the WAV file
output_file.close()
