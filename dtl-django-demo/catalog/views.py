"""DTL demo views.

Exercises the plugin's DTL template intelligence:
- render() calls with dict context and kwargs context
- {% extends %} / {% include %} chains resolved against TEMPLATES[0]['DIRS']
  and <app>/templates/<app>/ (APP_DIRS)
- {% load %} of a custom templatetags module (catalog_extras)
- {% url %} reverse lookups
"""
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

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
    # dict-literal context (Django's render() has no **kwargs context, unlike Flask)
    return render(request, "catalog/product_detail.html", {"product": product})


def about(request):
    return render(request, "catalog/about.html", {"team_size": 5, "founded_year": 2019})


def login_view(request):
    next_url = request.GET.get("next") or request.POST.get("next") or ""
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url or "catalog:product_list")
        error = "Invalid username or password."
    return render(request, "catalog/login.html", {"error": error, "next": next_url})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("catalog:product_list")
