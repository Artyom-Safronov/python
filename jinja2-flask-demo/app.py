"""Jinja2 demo app (Flask).

Exercises the plugin's DTL/Jinja2 template intelligence:
- render_template() calls with dict context and kwargs context
- {% extends %} / {% include %} chains
- {{ var }} / {{ var|filter }} completion
- a Jinja2 macro import (partials/_macros.html)
"""
from datetime import date
from typing import Optional
from unittest import loader

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "dev-secret-key-not-for-production"

USERS = {"admin": "password123"}


PRODUCTS = [
    {"id": 1, "name": "Keyboard", "price": 49.99, "in_stock": True},
    {"id": 2, "name": "Mouse", "price": 19.99, "in_stock": True},
    {"id": 3, "name": "Monitor", "price": 199.99, "in_stock": False},
]


@app.route("/")
def index():
    
    return render_template(
        "index.html",
        **{
            "title": "Catalog",
            "products": PRODUCTS,
            "today": date.today(),
        },
    )



@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    return render_template(
        "product_detail.html",
        product=product,
        related=[p for p in PRODUCTS if p["id"] != product_id],
    )


@app.route("/about")
def about():
    return render_template("about.html", team_size=5, founded_year=2019)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if USERS.get(username) == password:
            session["username"] = username
            return redirect(url_for("index"))
        error = "Invalid username or password."
    return render_template("login.html", error=error)


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

def sum(a: int, b: int) -> int:
    return "asd"

class User:
    def __init__(self, name: str, phone: Optional[str] = None):
        self.name = name
        self.phone = phone  # Телефон может отсутствовать

user1 = User("Ваня", "+999999999")
user2 = User(123, 123)