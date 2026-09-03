"""Page-level components — the htpy equivalent of index.html / product_detail.html."""
from datetime import date

from htpy import a, h1, h2, li, p, ul

from components import base_layout, price_tag


def index_page(products: list[dict], today: date | None = None):
    items = [
        li[a(href=f"/products/{product['id']}")[product["name"]], " ", price_tag(product)]
        for product in products
    ] or [li["No products yet."]]

    content = [
        h1["CATALOG"],
        ul(class_="products")[items],
    ]
    return base_layout("Catalog — htpy Demo", content, today)


def product_detail_page(product: dict | None, related: list[dict], today: date | None = None):
    if product is None:
        content = p["Product not found."]
        return base_layout("Not found", content, today)

    related_items = [li[item["name"]] for item in related]
    content = [
        h1[product["name"]],
        price_tag(product),
        h2["Related"] if related_items else "",
        ul[related_items] if related_items else "",
    ]
    return base_layout(product["name"], content, today)


def about_page(team_size: int, founded_year: int, today: date | None = None):
    content = [
        h1["About us"],
        p[f"Founded in {founded_year}, team of {team_size} people."],
    ]
    return base_layout("About", content, today)
