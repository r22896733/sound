from flask import Flask, request, render_template_string, send_from_directory
import datetime
import os
import json

app = Flask(__name__)

# Path to your sound.wav file
AUDIO_FILE = "sound.wav"

# Path to store logs
LOG_FILE = "client_logs.json"


def load_logs():
    """Load logs from file if exists."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_logs(logs):
    """Save logs to file."""
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)


@app.route("/")
def index():
    logs = load_logs()

    # Collect client details
    log_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent"),
        "method": request.method,
        "url": request.url
    }
    logs.append(log_entry)
    save_logs(logs)

    # Simple HTML page with audio player
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sound Player</title>
    </head>
    <body>
        <h2>Play Sound 🎵</h2>
        <audio controls autoplay>
            <source src="/audio/sound.wav" type="audio/wav">
            Your browser does not support the audio element.
        </audio>
        <p><a href="/logs">View Logs</a></p>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route("/audio/<path:filename>")
def serve_audio(filename):
    return send_from_directory(os.getcwd(), filename)


@app.route("/logs")
def show_logs():
    logs = load_logs()
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Client Logs</title>
    </head>
    <body>
        <h2>Client Logs 📜</h2>
        <table border="1" cellpadding="5">
            <tr>
                <th>Timestamp</th>
                <th>IP Address</th>
                <th>User Agent</th>
                <th>Method</th>
                <th>URL</th>
            </tr>
            {% for log in logs %}
            <tr>
                <td>{{ log.timestamp }}</td>
                <td>{{ log.ip }}</td>
                <td>{{ log.user_agent }}</td>
                <td>{{ log.method }}</td>
                <td>{{ log.url }}</td>
            </tr>
            {% endfor %}
        </table>
        <p><a href="/">Back</a></p>
    </body>
    </html>
    """
    return render_template_string(html, logs=logs)


if __name__ == "__main__":
    if not os.path.exists(AUDIO_FILE):
        print(f"Error: {AUDIO_FILE} not found in current directory.")
    app.run(host="0.0.0.0", port=5000, debug=True)
