import os
import time
import threading
import pathlib

def watchFile(path):
    # See if file exists, else return and close thread
    if path.is_dir():
        lastSubFiles = os.listdir(path)
        lastModified = os.path.getmtime(path)
        while True:
            time.sleep(2)
            newModified = os.path.getmtime(path)
            if newModified != lastModified:
                newSubFiles = os.listdir(path)
                newFile = list(set(newSubFiles) - set(lastSubFiles))
                if newFile == []:
                    return
                newFilePath = pathlib.Path(os.path.join(path, newFile[0]))
                if newFilePath.suffix != ".swp":
                    print(f"FILE CREATED - {newFilePath}")
                    newFileThread = threading.Thread(target=watchFile, args=(newFilePath,), name=f"fileWatchThread-{newFile}")
                    newFileThread.setDaemon(True)
                    newFileThread.start()
                    lastModified = newModified
                    lastSubFiles = newSubFiles
    else:
        try:
            lastModified = os.path.getmtime(path)
            while True:
                time.sleep(2)
                newModified = os.path.getmtime(path)
                if lastModified != newModified:
                    print(f"FILE MODIFIED - {path}")
                    lastModified = newModified
        except FileNotFoundError:
            print(f"FILE DELETE - {path}")
            return

class FileWatcher():
    def __init__(self, app):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if app:
            self.app = app
            self.cwd = os.getcwd()
            self.files = []

    def Watch(self, watch, ignore=[]):
        watch = list(set(watch))
        ignore = list(set(ignore))
        self.filesToWatch = self.__getFilesToWatch(watch, ignore)
        print("FILES WATCHED:")
        for file in self.filesToWatch:
            print(f"- {file}")
        for file in self.filesToWatch:
            fileWatchThread = threading.Thread(target=watchFile, args=(file,), name=f"fileWatchThread-{file}")
            fileWatchThread.setDaemon(True)
            fileWatchThread.start()

    def __getFilesToWatch(self, watch, ignore):
        filesToWatch = []
        if watch in [[], ["*"], "*", None]:
            filesToWatch = list(pathlib.Path(self.cwd).rglob("*"))
        else:
            cwd = os.getcwd()
            for file in watch:
                file = pathlib.Path(os.path.join(cwd, "app", file))
                if os.path.isfile(file):
                    filesToWatch.append(file)
                else:
                    filesToWatch.append(file)
                    subFiles = [f for f in list(file.rglob("*")) if f.suffix != ".swp"]
                    filesToWatch += subFiles
        ignore += ["flask_file_watcher", "__pycache__", "venv"]
        if ignore in [[], None]:
            pass
        else:
            cwd = os.getcwd()
            for file in ignore:
                file = pathlib.Path(os.path.join(cwd, "app", file))
                if os.path.isfile(file):
                    filesToWatch.remove(file)
                else:
                    filesToWatch.remove(file)
                    for f in list(file.rglob("*")):
                        filesToWatch.remove(f)
        return filesToWatch


