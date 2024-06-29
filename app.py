from flask import Flask, request, jsonify
from flask_cors import CORS

from pymongo import MongoClient

from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.environ.get("MONGODB_URI")
db_name = os.environ.get("DB_NAME")
projection = {"_id": 0, "name": 1, "quantity": 1, "price": 1}

client = MongoClient(mongo_uri)
if db_name:
    db = client[db_name]

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})


@app.route("/create", methods=["POST"])
def create():
    product = request.get_json()

    if len(product) < 3:
        return jsonify({"Error": "Please provide all the product details."}), 400

    name = product.get("name")
    price = product.get("price")
    quantity = product.get("quantity")

    db.products.insert_one(
        {"name": name, "price": price, "quantity": quantity})

    return jsonify({"message": f"Inserted product {name}!"}), 201


@app.route("/", methods=["GET"])
def read():
    results = list(db.products.find({}, projection))
    return jsonify(results), 200


@app.route("/search", methods=["POST"])
def search():
    req = request.get_json()
    name = req.get("name")
    if not name:
        return jsonify({"Error": "Please provide the product name."}), 400

    result = list(db.products.find({"name": name}, projection))
    if not result:
        return jsonify({"message": f"Could not find any products named {name}."}), 404

    return jsonify(result), 200


@app.route("/update", methods=["POST"])
def update():
    product_update = request.get_json()

    if not product_update:
        return jsonify({"Error": "Please provide the product name."}), 400

    name = product_update.get("name")
    result = db.products.update_one({"name": name}, {"$set": product_update})

    if result.modified_count == 0:
        return jsonify({"Error": f"Could not find any products named {name}."}), 404

    return jsonify({"message": f"Updated product {name}!"})


@app.route("/delete", methods=["POST"])
def delete():
    name = request.get_json().get("name")
    if not name:
        return jsonify({"Error": "Please provide the product name."}), 400

    result = db.products.delete_one({"name": name})
    if result.deleted_count == 0:
        return jsonify({"message": f"Could not find any products named {name}."}), 404

    return jsonify({"message": f"Deleted product {name}!"})


if __name__ == "__main__":
    app.run(debug=True)
