from django.contrib import admin
from .models import Product, Category, Order, Customer,Rating

# Register your models here.
admin.site.register(Rating)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Customer)
