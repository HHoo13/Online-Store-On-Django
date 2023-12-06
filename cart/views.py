from rest_framework.decorators import api_view

from cart.cart import Cart
from django.shortcuts import render

from api.models import Product

@api_view(["POST"])
def add_to_cart(request, product_id, quantity):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.add(product, product.unit_price, quantity)
@api_view(["DELETE"])
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
@api_view(["GET"])
def get_cart(request):
    # cart = Cart(request)
    # totalprice=cart.summary()
    return render(request, 'cart/base.html', {'cart': Cart(request)})




