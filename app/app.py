from flask import Flask
from flask_file_watcher import FileWatcher

app = Flask(__name__)

fw = FileWatcher(app)

@app.route("/")
def index():
    # reload_app()
    return "sdfsdf"


if __name__ == "__main__":
    fw.Watch(
        watch=[".", "templates", "static"],
        ignore=["__pycache__"]
    )
    app.run(debug=True)
