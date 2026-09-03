"""Reusable htpy components.

htpy has no template files or string templates at all: markup is plain Python
function calls returning composable Element trees. This is the paradigm the
plugin's PSI-based approach handles "for free" (ordinary Python navigation,
completion, refactoring already work) — there is no {% %}/{{ }} mini-language
to parse, no render()->file resolution, no context-variable inference.
"""
from datetime import date

from htpy import a, body, footer, h1, h2, head, html, li, main, meta, nav, p, span, title, ul


def nav_bar():
    return nav[
        a(href="/")["Catalog"],
        " ",
        a(href="/about")["About"],
    ]


def site_footer(today: date | None = None):
    year = today.year if today else 2026
    return footer[p[f"© {year} htpy Demo"]]


def price_tag(product: dict):
    css_class = "in-stock" if product["in_stock"] else "out-of-stock"
    return span(class_=f"price {css_class}")[f"{product['price']:.2f} USD"]


def base_layout(page_title: str, content, today: date | None = None):
    return html(lang="en")[
        head[
            meta(charset="UTF-8"),
            title[page_title],
        ],
        body[
            nav_bar(),
            main[content],
            site_footer(today),
        ],
    ]
