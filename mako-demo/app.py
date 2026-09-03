"""Mako demo app (Flask + Mako, Mako used directly — not via Flask's Jinja loader).

Exercises Mako templating:
- <%inherit file="..."/> template inheritance
- <%include file="..."/> partials
- <%def> local functions (Mako's equivalent of Jinja macros)
- ${ expr } / ${ expr | filter } interpolation
- % for / % if control blocks
"""
from datetime import date
from pathlib import Path

from flask import Flask
from mako.lookup import TemplateLookup

app = Flask(__name__)

TEMPLATE_DIR = Path(__file__).parent / "templates"
lookup = TemplateLookup(directories=[str(TEMPLATE_DIR)], input_encoding="utf-8")

PRODUCTS = [
    {"id": 1, "name": "Keyboard", "price": 49.99, "in_stock": True},
    {"id": 2, "name": "Mouse", "price": 19.99, "in_stock": True},
    {"id": 3, "name": "Monitor", "price": 199.99, "in_stock": False},
]


def render(template_name, **context):
    return lookup.get_template(template_name).render(**context)


@app.route("/")
def index():
    return render("index.mako", page_title="Catalog", products=PRODUCTS, today=date.today())


@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    return render(
        "product_detail.mako",
        product=product,
        related=[p for p in PRODUCTS if p["id"] != product_id],
    )


@app.route("/about")
def about():
    return render("about.mako", team_size=5, founded_year=2019)


if __name__ == "__main__":
    app.run(debug=True)
