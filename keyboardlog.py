from pynput import keyboard
import time
import gc
global key_press_status

def track_keyboard_presses():
    last_key_press_time = None

    def log(message):
        print(f"{message}")

    def on_press(key):
        nonlocal last_key_press_time
        last_key_press_time = time.time()

    # Set up the listener
    with keyboard.Listener(on_press=on_press) as listener:
        try:

            def perform_memory_cleanup():
                gc.collect()

            perform_memory_cleanup()

            while True:
                time.sleep(1)
                if last_key_press_time is not None and time.time() - last_key_press_time <= 1:
                    key_press_status = 1
                    yield key_press_status
                else:
                    key_press_status = 0
                    yield key_press_status
                    last_key_press_time = None
        except KeyboardInterrupt:
            listener.stop()

if __name__ == "__main__":
    for key_press in track_keyboard_presses():
        print(f"Keyboard key press detected: {key_press}")