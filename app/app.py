from flask import Flask
from flask_file_watcher.flask_file_watcher import FileWatcher

app = Flask(__name__)

fw = FileWatcher(app)

@app.route("/")
def index():
    return "sdfsdf"


if __name__ == "__main__":
    fw.Watch(
        watch=[".", "templates", "static"]
    )
    app.run(debug=True)
