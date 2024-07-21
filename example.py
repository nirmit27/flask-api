# import json
import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app: Flask = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db: SQLAlchemy = SQLAlchemy(app=app)


"""
# One to One mapping

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"Employee({self.id}, '{self.name}', {self.age}, '{self.email}')"
"""

"""
# One to Many mapping

class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # PK
    team = db.Column(db.String(50), nullable=True, unique=True)
    state = db.Column(db.String(50), nullable=True)
    members = db.relationship("Player", backref="team")  # Relationship

    def __repr__(self):
        return f"Team('{self.team}', '{self.state}')"


class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=True)
    nationality = db.Column(db.String(50), nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))  # FK for relationship

    def __repr__(self):
        return f"Player('{self.name}', '{self.nationality}')"
"""

# Many to Many mapping


# Association table
customers_products = db.Table(
    "customers_products",
    db.Column("customer_id", db.Integer, db.ForeignKey("customers.id")),  # FK
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"))  # FK
)


class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    items = db.relationship(
        "Product", backref="buyers", secondary=customers_products)

    def __repr__(self):
        return f"Customer(name='{self.name}, email='{self.email}')"


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price})"


if __name__ == "__main__":
    app.run(debug=True)

    """
    employees: dict[int, dict] = {
        1: {
            "name": "Jim Halpert",
            "age": 26,
            "role": "Sales Representative"
        },
        2: {
            "name": "Pam Beesly",
            "age": 25,
            "role": "Receptionist"
        },
        3: {
            "name": "Michael Scott",
            "age": 40,
            "role": "Regional Manager"
        },
        4: {
            "name": "Dwight Schrute",
            "age": 30,
            "role": "Sales Representative"
        },
        5: {
            "name": "Ryan Howard",
            "age": 35,
            "role": "Regional Manager"
        }
    }

    with open("data.json", 'w') as fp:
        json.dump(employees, fp)

    data: dict[int, dict] = {}
    with open("data.json", 'r') as fp:
        data = json.load(fp)

    for key, value in data.items():
        print(f"{key}) {value['name']}: {value['age']}, {value['role']}")
    """
