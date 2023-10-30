from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from watchdog.observers import Observer
import time


last_trigger_time = time.time()


class FileWatcherHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        global last_trigger_time
        curr_time = time.time()
        if curr_time - last_trigger_time > 1:
            last_trigger_time = curr_time
            # print(f"Event detected: {event.event_type} - Path: {event.src_path}")
            print(event)


class FileWatcher():
    def __init__(self, app=None, files=None):
        if app is not None:
            self.init_app(app, files)

    def init_app(self, app, files):
        self.app = app
        self.files = files
        self.event_handler = FileWatcherHandler()
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path=files, recursive=True)
        self.observer.start()
        print("observser start")

    def run(self):
        while True:
            print("Sleep 1 sec")
            time.sleep(1)

    def stop(self):
        if self.observer.is_alive():
            self.observer.stop()
        self.observer.join()

