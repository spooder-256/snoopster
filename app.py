from pathlib import Path

from flask import Flask, Response

app = Flask(__name__)
HERE = Path(__file__).parent
PAGE = (HERE / "templates" / "index.html").read_text(encoding="utf-8")
FRAMES = (HERE / "frames.json").read_text(encoding="utf-8")


@app.route("/")
def home():
    return Response(PAGE, mimetype="text/html")


@app.route("/frames.json")
def frames():
    return Response(FRAMES, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)
