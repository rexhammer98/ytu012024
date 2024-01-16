import cv2
import dlib
import time
import gc

def eye_tracking_generator():
    # Load the face and facial landmarks detection models
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Provide the correct path to the model file

    # Define ROIs on the screen
    screen_width, screen_height = 1280, 960  # Adjusted screen dimensions
    roi_left = 0
    roi_top = 0
    roi_right = screen_width
    roi_bottom = screen_height



    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    start_time = time.time()
    interval = 1  # Process every 1 second

    while True:

        def perform_memory_cleanup():
            gc.collect()

        perform_memory_cleanup()

        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = detector(gray)

        on_screen = False  # Initialize the on_screen flag

        for face in faces:
            landmarks = predictor(gray, face)

            # Extract eye coordinates based on multiple landmark points around the eyes
            left_eye_x = sum(landmarks.part(i).x for i in range(36, 42)) // 6
            left_eye_y = sum(landmarks.part(i).y for i in range(36, 42)) // 6
            right_eye_x = sum(landmarks.part(i).x for i in range(42, 48)) // 6
            right_eye_y = sum(landmarks.part(i).y for i in range(42, 48)) // 6

            # Check if the eyes are on the screen
            if roi_left <= left_eye_x <= roi_right and roi_top <= left_eye_y <= roi_bottom and \
                    roi_left <= right_eye_x <= roi_right and roi_top <= right_eye_y <= roi_bottom:
                on_screen = True
                break  # No need to check other faces if one is on the screen

        # Update the message based on whether the eyes are on the screen or not
        if on_screen:
            message = "1"
        else:
            message = "0"

        # Process every 'interval' seconds
        elapsed_time = time.time() - start_time
        if elapsed_time >= interval:
            yield f"{message}"
            start_time = time.time()

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    for output_message in eye_tracking_generator():
        output_message
