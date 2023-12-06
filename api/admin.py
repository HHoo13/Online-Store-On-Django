from django.contrib import admin
from api.models import Banner, Product, Buyer, Review, Tag, Category, Orders

admin.site.register([Product, Banner, Buyer, Review, Tag, Category, Orders])
