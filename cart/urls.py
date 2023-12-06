from django.urls import path, re_path
from cart.views import get_cart, add_to_cart, remove_from_cart

urlpatterns = [
    path('', get_cart, name="get"),
    re_path(r'^add/$', add_to_cart, name="post"),
    re_path(r'^remove/$', remove_from_cart, name="delete"),

]
