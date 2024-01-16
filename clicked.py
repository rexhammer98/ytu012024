import pygetwindow as gw
from pynput import mouse
import time
import gc

def track_mouse_clicks():
    action_occurred = 0
    prev_window = None


    def on_move(x, y):
        nonlocal action_occurred
        action_occurred = 1

    def on_click(x, y, button, pressed):
        nonlocal action_occurred
        if pressed:
            action_occurred = 1

    while True:
        active_window = gw.getActiveWindow()

        def perform_memory_cleanup():
            gc.collect()

        perform_memory_cleanup()

        if active_window and active_window.title != prev_window:
            # Window changed
            action_occurred = 0
            prev_window = active_window.title

        with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
            time.sleep(1)
            listener.stop()
            yield action_occurred
            action_occurred = 0


if __name__ == "__main__":
    track_mouse_clicks()
