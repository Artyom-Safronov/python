from django import template

register = template.Library()


@register.filter
def usd(value):
    return f"${value:.2f}"


@register.simple_tag
def stock_badge(product):
    return "In stock" if product.in_stock else "Out of stock"
