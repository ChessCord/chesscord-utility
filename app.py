from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "ChessCord Utility is up and running..."


def run_webserver():
    app.run(host="0.0.0.0", port=8080)
