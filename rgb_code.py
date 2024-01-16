import cv2
import numpy as np
import time
import gc

def get_mean_rgb():
    # Open the camera
    cap = cv2.VideoCapture(0)

    # Set the start time
    start_time = time.time()

    try:
        while True:

            def perform_memory_cleanup():
                gc.collect()

            perform_memory_cleanup()

            # Capture frame-by-frame
            ret, frame = cap.read()

            # Calculate the mean values for each channel
            mean_red = np.mean(frame[:, :, 2]).astype(int)
            mean_green = np.mean(frame[:, :, 1]).astype(int)
            mean_blue = np.mean(frame[:, :, 0]).astype(int)

            # Check if one second has passed
            if time.time() - start_time >= 1:
                rgbcode = (mean_red, mean_green, mean_blue)
                yield rgbcode
                start_time = time.time()  # Reset the start time

    except KeyboardInterrupt:
        pass
    # Release the camera
    cap.release()

# Uncomment the line below if you want to use this file as a standalone script
# get_mean_rgb()
