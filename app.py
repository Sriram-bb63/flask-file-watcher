from flask import Flask, render_template, jsonify
import os
import time
import threading

app = Flask(__name__)

def file_monitor():
    print(" * Static files monitor: True")
    filename = "static/styles/styles.css"
    last_modified = os.path.getmtime(filename)
    while True:
        current_modified = os.path.getmtime(filename)
        if current_modified != last_modified:
            print("Change detected (Why is this printing twice)")
            last_modified = current_modified
            global css_change_count
            css_change_count = css_change_count + 1
        time.sleep(1)

@app.route("/")
def index():
    return render_template("index.html") + "<h1>Hello world</h1>"

@app.route("/css-refresher")
def css_refresher():
    return jsonify({
        "css_change_count": css_change_count
    })

if __name__ == "__main__":
    try:
        css_change_count = 0
        file_monitor_thread = threading.Thread(target=file_monitor, daemon=True)
        file_monitor_thread.start()
        app.run(debug=True)
    except KeyboardInterrupt:
        file_monitor_thread.join()