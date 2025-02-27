import math
import subprocess
import time

# Set the parameters for the sound wave
frequency = 440  # Frequency of the sound wave in Hz (A4 note)
duration = 3  # Duration of the sound wave in seconds
amplitude = 0.5  # Amplitude of the sound wave (normalized)

# Calculate the number of samples per second
samples_per_second = 44100
num_samples = int(duration * samples_per_second)

# Generate and play the sound wave
for i in range(num_samples):
    t = i / samples_per_second
    sample = int(amplitude * math.sin(2 * math.pi * frequency * t))
    subprocess.run(['osascript', '-e', f'beep {sample}'], check=True)

    time.sleep(1 / samples_per_second)  # Adjust the sleep time based on the sample rate

print("Sound wave played successfully.")