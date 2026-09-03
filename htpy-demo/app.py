"""htpy demo app (Flask + htpy — HTML-in-Python, no template files).

Unlike Jinja2/DTL/Mako, there is no string-based mini-language to complete or
navigate: `product_detail_page(product, related)` is a plain Python function
call, so IDE navigation/completion/refactoring on it are already fully served
by PythonCore's own Python PSI support.
"""
from datetime import date

from flask import Flask

from pages import about_page, index_page, product_detail_page

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Keyboard", "price": 49.99, "in_stock": True},
    {"id": 2, "name": "Mouse", "price": 19.99, "in_stock": True},
    {"id": 3, "name": "Monitor", "price": 199.99, "in_stock": False},
]


@app.route("/")
def index():
    return str(index_page(PRODUCTS, today=date.today()))


@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    related = [p for p in PRODUCTS if p["id"] != product_id]
    return str(product_detail_page(product, related, today=date.today()))


@app.route("/about")
def about():
    return str(about_page(team_size=5, founded_year=2019, today=date.today()))


if __name__ == "__main__":
    app.run(debug=True)
