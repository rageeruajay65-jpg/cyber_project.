from flask import Flask, redirect, render_template, request, send_file
import io
import os
import socket
import qrcode

app = Flask(__name__, template_folder=".", static_folder=None)

PORT = 5000

def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()

LAPTOP_IP = os.environ.get("LAPTOP_IP", get_local_ip())
QR_TARGET_URL = f"http://{LAPTOP_IP}:{PORT}/allow"

LEVEL_CONTENT = {
    "1": "Level 1 content",
    "2": "Level 2 content",
    "3": "Level 3 content"
}

selected_level = "1"


@app.route("/")
def index():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username and password:
            return redirect("/home")

        return "Username and password are required.", 400

    return render_template("login.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/set-level", methods=["POST"])
def set_level():
    global selected_level

    level = request.form.get("level", "1")

    if level not in LEVEL_CONTENT:
        return "Invalid level", 400

    selected_level = level
    return redirect("/issue")


@app.route("/issue")
def issue():
    return render_template("issue.html")


@app.route("/qr.png")
def qr_image():
    qr = qrcode.make(QR_TARGET_URL)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype="image/png")


@app.route("/allow")
def allow():
    return render_template(
        "allow.html",
        level=selected_level,
        content=LEVEL_CONTENT[selected_level]
    )


@app.route("/style.css")
def stylesheet():
    return send_file("style.css", mimetype="text/css")


@app.route("/assets/<path:filename>")
def assets(filename):
    from flask import send_from_directory
    return send_from_directory("assets", filename)


if __name__ == "__main__":
    print("Open on laptop: http://127.0.0.1:5000")
    print("QR destination:", QR_TARGET_URL)
    app.run(host="0.0.0.0", port=PORT, debug=False)
