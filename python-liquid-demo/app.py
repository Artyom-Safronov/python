"""python-liquid demo app (Flask + Shopify-style Liquid templates).

Liquid has no {% extends %}/{% block %} inheritance in its core tag set
(unlike Jinja2/DTL/Mako) — composition is done with {% render %} (isolated
scope, explicit params only) or {% include %} (shares the caller's scope).
Every page below assembles itself from partials/nav.liquid and
partials/price_tag.liquid via {% render %}.
"""
from datetime import date

from flask import Flask
from liquid import Environment, FileSystemLoader

app = Flask(__name__)

env = Environment(loader=FileSystemLoader("templates"))

PRODUCTS = [
    {"id": 1, "name": "Keyboard", "price": 49.99, "in_stock": True},
    {"id": 2, "name": "Mouse", "price": 19.99, "in_stock": True},
    {"id": 3, "name": "Monitor", "price": 199.99, "in_stock": False},
]


def render(template_name, **context):
    return env.get_template(template_name).render(**context)


@app.route("/")
def index():
    return render("index.liquid", title="Catalog", products=PRODUCTS, today=date.today())


@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    return render(
        "product_detail.liquid",
        product=product,
        related=[p for p in PRODUCTS if p["id"] != product_id],
    )


@app.route("/about")
def about():
    return render("about.liquid", team_size=5, founded_year=2019)


if __name__ == "__main__":
    app.run(debug=True)
