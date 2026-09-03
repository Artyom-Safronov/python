"""django-cotton demo views.

Templates compose <c-product-card>, <c-price-tag>, <c-button> components
(templates/cotton/*.html) that compile to native DTL tags — so the plugin's
existing DTL context-var / render() intelligence should keep working, plus a
new surface: <c-xxx> tag names <-> cotton/xxx.html file resolution and
<c-vars>/slot/:attr completion inside those component templates.
"""
from django.shortcuts import get_object_or_404, render

from .models import Product


def product_list(request):
    products = Product.objects.select_related("category").all()
    return render(
        request,
        "catalog/product_list.html",
        {
            "products": products,
            "query": request.GET.get("q", ""),
        },
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "catalog/product_detail.html", {"product": product})


def about(request):
    return render(request, "catalog/about.html", {"team_size": 5, "founded_year": 2019})
