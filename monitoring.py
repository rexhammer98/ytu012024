import asyncio
import csv
import gc
from datetime import datetime
import os
from eye_gazing import eye_tracking_generator
from clicked import track_mouse_clicks
from keyboardlog import track_keyboard_presses
from current_app import monitor_app
from noise_level import monitor_noise
from rgb_code import get_mean_rgb
from brightness import track_brightness


def perform_memory_cleanup():
    gc.collect()
    print("Memory cleanup completed.")


perform_memory_cleanup()
def print_and_write_to_csv(buffer, csvfile, brightness, rgb, noise, app_info, mouse_click, keyboard_press, eye_tracking):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    brightness = float(brightness)
    noise = float(noise)

    rgb_values = ",".join(map(str, map(int, rgb)))

    data = [timestamp, mouse_click, keyboard_press, eye_tracking, app_info, noise, rgb_values, brightness]
    ", ".join(map(str, data))

    buffer.append(data)

    if len(buffer) == 120:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(buffer)
        csvfile.flush()
        buffer.clear()
        print("Data written to CSV file.")
        perform_memory_cleanup()

async def run_all_features():
    tasks = [
        track_brightness(),
        get_mean_rgb(),
        monitor_noise(),
        monitor_app(),
        track_mouse_clicks(),
        track_keyboard_presses(),
        eye_tracking_generator()
    ]

    with open('output.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        header = ["timestamp", "mouse_click", "keyboard_press",
        "eye_tracking", "app_info", "noise", "rgb", "brightness"]
        #csv_writer.writerow(header)
        data_buffer = []

        #iteration_count = 0

        while True:
            results = await asyncio.gather(*[asyncio.to_thread(next, task) for task in tasks])
            print_and_write_to_csv(data_buffer, csvfile, *results)
            #iteration_count += 1

            # Check if you want to stop the script by other means
            '''if iteration_count == 10:
                # Send a notification
                send_notification("Script stopped manually. Last cycle completed.")
                break'''


asyncio.run(run_all_features())