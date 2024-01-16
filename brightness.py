import cv2
import time
from datetime import datetime
import gc

def track_brightness(camera_index=0):
    # Open the camera
    cap = cv2.VideoCapture(camera_index)

    brightness_values = []
    start_time = time.time()

    while True:

        # Variables for calculating average brightness per second
        def perform_memory_cleanup():
            gc.collect()

        perform_memory_cleanup()
        # Capture a frame
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate the mean pixel intensity (brightness)
        brightness = int(gray_frame.mean())

        # Store the brightness value
        brightness_values.append(brightness)

        # Check if one second has passed
        try:
            if time.time() - start_time >= 1.0:
                # Calculate average brightness for the last second
                average_brightness = sum(brightness_values) / len(brightness_values)

                # Print the average brightness with two decimals
                brightness = (f'{average_brightness:.2f}')
                yield brightness

                # Reset variables for the next second
                brightness_values = []
                start_time = time.time()

        except KeyboardInterrupt:
            pass

    # Release the camera
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    track_brightness()
