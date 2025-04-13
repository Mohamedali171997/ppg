from django.shortcuts import render,redirect
from .models import Product,Rating
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})
def cart(request):
    return render(request, 'cart.html', {})
def orders(request):
    return render(request, 'orders.html', {})
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('home') 
        else:
            messages.error(request, 'Invalid credentials')

            return redirect('login') 
    else:
        return render(request, 'login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, 'Logout successful')
   
    return redirect('home')

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
 
    return render(request, 'product_detail.html', {'product': product})