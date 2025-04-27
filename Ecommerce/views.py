from django.shortcuts import render,redirect
from .models import Product, Rating, Order, OrderItem, Customer
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm
from django.http import JsonResponse
import json
# Create your views here.

def header1(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get_or_create(customer=customer, complete=False)[0]
        items = order.orderitem_set.all()  # Add parentheses here
        cart_items = order.get_cart_items
    else:
        # Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,
                 'get_shipping_cost': 0, 'get_cart_totalplus_shipping': 0,
                 'get_estimated_tax': 0, 'get_cart_totalplus_shipping_and_tax': 0}
        cart_items = order['get_cart_items']

    context = {'items': items, 'order': order, 'cart_items': cart_items}
    print(context)
    return render(request, 'header.html', context)


def header2(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get_or_create(customer=customer, complete=False)[0]
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        # Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,
                 'get_shipping_cost': 0, 'get_cart_totalplus_shipping': 0,
                 'get_estimated_tax': 0, 'get_cart_totalplus_shipping_and_tax': 0}
        cart_items = order['get_cart_items']

    context = {'items': items, 'order': order, 'cart_items': cart_items}
    print(context)
    return render(request, 'header2.html', context)


def home(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get_or_create(customer=customer, complete=False)[0]
        cart_items = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

    context = {'products': products, 'order': order, 'cart_items': cart_items}
    return render(request, 'home.html', context)


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
    print(context)
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
    print(context)
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
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get_or_create(customer=customer, complete=False)[0]
        cart_items = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

    context = {
        'product': product,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'product_detail.html', context)

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


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)