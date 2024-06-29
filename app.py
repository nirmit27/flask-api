from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Hello friend."})


if __name__ == "__main__":
    app.run(debug=True)
