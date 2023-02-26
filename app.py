from flask import Flask

app = Flask(__name__)


@app.get("/")
def get_hello():
    return "Hello Word"


if __name__ == "__main__":
    app.run(debug=True)
