from AppKit import NSWorkspace
import subprocess
import time
from datetime import datetime
import threading
from urllib.parse import urlparse
import gc



def get_active_app():
    active_app = NSWorkspace.sharedWorkspace().activeApplication()
    return active_app['NSApplicationName']

def get_chrome_tab_info():
    try:
        # Run an AppleScript to get the title and URL of the active tab in Chrome
        script = '''
            tell application "Google Chrome"
                set activeTab to active tab of front window
                set tabTitle to title of activeTab
                set tabURL to URL of activeTab
                return tabURL
            end tell
        '''
        result = subprocess.check_output(['osascript', '-e', script])
        url = result.strip().decode('utf-8')
        parsed_url = urlparse(url)
        main_website_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        return main_website_url
    except subprocess.CalledProcessError:
        return "N/A"

def monitor_app():
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        active_app = get_active_app()

        def perform_memory_cleanup():
            gc.collect()

        perform_memory_cleanup()

        if active_app == "Google Chrome":
            tab_url = get_chrome_tab_info()
            yield f"{active_app} - {tab_url}"
        else:
            yield active_app

        time.sleep(1)

if __name__ == "__main__":
    for info in monitor_app():
        # Do nothing here, just let it run in the background
        pass
