from flask import Flask, request, render_template_string, send_from_directory
import datetime
import os

app = Flask(__name__)

# Path to your sound.wav file
AUDIO_FILE = "sound.wav"

# In-memory log (could also be written to a database or file)
client_logs = []


@app.route("/")
def index():
    # Log client details
    log_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent"),
        "method": request.method,
        "url": request.url
    }
    client_logs.append(log_entry)

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
    # Serve the audio file
    return send_from_directory(os.getcwd(), filename)


@app.route("/logs")
def show_logs():
    # Display collected client logs
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
    return render_template_string(html, logs=client_logs)


if __name__ == "__main__":
    # Ensure sound.wav exists in the same folder
    if not os.path.exists(AUDIO_FILE):
        print(f"Error: {AUDIO_FILE} not found in current directory.")
    app.run(host="0.0.0.0", port=5000, debug=True)
