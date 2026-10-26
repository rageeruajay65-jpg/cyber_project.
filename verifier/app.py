
from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
import io
import qrcode

# All HTML files are in the same directory as app.py.
app = Flask(__name__, template_folder=".", static_folder=None)

PORT = 5000

# This URL remains identical for all three levels.
QR_TARGET_URL = "https://terrible-spooky-wand-gx4vwg74x756cvxpg-5000.app.github.dev/allow"

LEVEL_CONTENT = {
    "1": "Level 1 content",
    "2": "Level 2 content",
    "3": "Level 3 content",
}

# Shared selection for this single-laptop demonstration.
selected_level = "1"


@app.route("/style.css")
def stylesheet():
    return send_from_directory(app.root_path, "style.css")


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Demonstration login only; no real authentication.
        if not username or not password:
            return render_template(
                "login.html",
                error="Please enter username and password."
            ), 400

        return redirect(url_for("home"))

    return render_template("login.html", error=None)


@app.route("/home")
def home():
    return render_template(
        "home.html",
        selected_level=selected_level
    )


@app.route("/set-level", methods=["POST"])
def set_level():
    global selected_level

    level = request.form.get("level", "1")

    if level not in LEVEL_CONTENT:
        level = "1"

    selected_level = level
    return redirect(url_for("issue"))


@app.route("/issue")
def issue():
    return render_template(
        "issue.html",
        selected_level=selected_level,
        qr_target_url=QR_TARGET_URL
    )


@app.route("/qr.png")
def qr_image():
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4
    )

    qr.add_data(QR_TARGET_URL)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype="image/png")


@app.route("/allow")
def allow():
    return render_template(
        "allow.html",
        level=selected_level,
        content=LEVEL_CONTENT[selected_level]
    )


if __name__ == "__main__":
    print("Laptop browser: http://127.0.0.1:5000")
    print("QR destination:", QR_TARGET_URL)

    app.run(host="0.0.0.0", port=PORT, debug=False)
