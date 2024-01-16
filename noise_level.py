import sounddevice as sd
import numpy as np
import time
import gc
import math

def monitor_noise():
    def callback(indata, frames, time, status):
        if status:
            print(status, flush=True)

        # Calculate the sound level in decibels
        rms_value = np.linalg.norm(indata)
        volume_norm = 20 * math.log10(rms_value)

        volume_norm = volume_norm + 35  # Adjust this value as needed

        # Add the sound level to the list
        sound_levels.append(volume_norm)

    # Set the sampling parameters
    duration = 10  # seconds
    sample_rate = 44100  # Hz

    # Initialize variables
    sound_levels = []
    start_time = time.time()

    def perform_memory_cleanup():
        gc.collect()
        print("Memory cleanup completed.")

    perform_memory_cleanup()

    # Start the audio stream
    with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate):
        try:
            while True:
                # Check if one second has passed
                if time.time() - start_time >= 1:
                    # Calculate the mean sound level for the past second
                    mean_level = np.mean(sound_levels)
                    noiselevel = f"{mean_level:.2f}"

                    yield noiselevel
                    # Reset the variables for the next second
                    sound_levels = []
                    start_time = time.time()

        except KeyboardInterrupt:
            pass

# Call the function if the script is run directly
if __name__ == "__main__":
    for noise in monitor_noise():
        print(noise)
