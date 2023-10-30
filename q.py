import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
import os

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(folder_to_track):
            src = folder_to_track + "/" + filename
            dest = folder_to_move + "/" + filename
            os.rename(src, dest)

folder_to_track = ""
folder_to_move = ""
observer = Observer()
event_handler = Handler()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except:
    observer.stop()
observer.join()