from django.contrib import admin
from .models import Product, Category, Order, Customer,Rating, OrderItem,ShippingAddress
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Rating)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
