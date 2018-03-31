from django.contrib import admin

# Register your models here.
from Product.models import Product, Transaction, Review

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Transaction)