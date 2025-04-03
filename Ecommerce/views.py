from django.shortcuts import render
from .models import Product,Rating

# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})
def cart(request):
    return render(request, 'cart.html', {})
def orders(request):
    return render(request, 'orders.html', {})