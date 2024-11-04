from flask import Flask, send_file

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/pass")
def pass_word():
    image_path = "./Picture1.png"
    return send_file(image_path, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
