from django.shortcuts import render,redirect
from .models import Product, Rating, Order
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm
# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get_or_create(customer=customer, complete=False)[0]
        items = order.orderitem_set.all()
    else:
        # Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0
                 , 'get_shipping_cost': 0, 'get_cart_totalplus_shipping': 0
                 , 'get_estimated_tax': 0, 'get_cart_totalplus_shipping_and_tax': 0
                }

    context = {'items':items, 'order': order}
    return render(request, 'cart.html', context)

def orders(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get_or_create(customer=customer, complete=False)[0]
        items = order.orderitem_set.all()
    else:
        # Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0
                 , 'get_shipping_cost': 0, 'get_cart_totalplus_shipping': 0
                 , 'get_estimated_tax': 0, 'get_cart_totalplus_shipping_and_tax': 0
                }

    context = {'items':items, 'order': order}
    return render(request, 'orders.html', context)
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
def signup(request):
    form = SignUpForm()

    if request.method == 'POST':

        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed')
            return redirect('signup')
    else:
        form = SignUpForm()
    # form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
    