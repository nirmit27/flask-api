from flask import Flask, request, jsonify
from flask_cors import CORS

from pymongo import MongoClient

from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.environ.get("MONGODB_URI")
db_name = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
if db_name:
    db = client[db_name]

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})


@app.route("/", methods=["GET"])
def index():
    projection = {"_id": 0, "name": 1, "quantity": 1, "price": 1}
    result = list(db.products.find({}, projection))
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
