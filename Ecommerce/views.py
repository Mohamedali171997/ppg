from django.shortcuts import render,redirect
from .models import Product, Rating, Order, OrderItem, Customer
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            # Si le Customer n'existe pas, on le crée
            customer = Customer.objects.create(user=request.user)
    else:
        customer = None

    # Ajoute ici toute logique qui doit se baser sur le `customer`
    cart_items = 0
    order = None

    if customer:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.get_cart_items if order else 0

    context = {
        'products': products,
        'order': order if order else {'get_cart_total': 0, 'get_cart_items': 0},
        'cart_items': cart_items
    }

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

    context = {'items':items, 'order': order,
               'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY}
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
            if user.is_staff or user.is_superuser:
                return redirect('/admin/')  # Redirection vers admin Django
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

@csrf_exempt
def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    print(f"Product ID: {product_id}, Action: {action}")

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity += 1
        order_item.save()
    elif action == 'remove':
        order_item.quantity -= 1
        if order_item.quantity > 0:
            order_item.save()
        else:
            order_item.delete()
    elif action == 'delete':
        # Handle the delete action
        order_item.delete()

    return JsonResponse({'message': 'Item was updated'}, safe=False)



#stripe
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import stripe
import json
from django.conf import settings
from .models import Order
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from .models import Order
import stripe
import json
import traceback

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Utilisateur non connecté'}, status=403)

            customer = request.user.customer

            try:
                order = Order.objects.get(customer=customer, complete=False)
            except Order.DoesNotExist:
                return JsonResponse({'error': 'Commande introuvable'}, status=404)

            total_cents = int(order.get_cart_totalplus_shipping_and_tax * 100)

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': total_cents,
                        'product_data': {
                            'name': 'Commande client',
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:8000/success/',
                cancel_url='http://localhost:8000/cancel/',
            )
            return JsonResponse({'id': checkout_session.id})

        except Exception as e:
            print("Stripe Checkout error:")
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
