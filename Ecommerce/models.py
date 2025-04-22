from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal


# Create your models here.
class Rating(models.Model):
    image = models.ImageField(upload_to='ratings/')
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    image = models.ImageField(upload_to='products/')
    name = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)
    rate_star = models.ForeignKey(Rating, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    #todo in future add a field for the product category
    stock = models.PositiveIntegerField()
    is_solde = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name


class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
	

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 
	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 
	@property
	def get_shipping_cost(self):
		return Decimal('6.99')
	@property
	def get_cart_totalplus_shipping(self):
		return self.get_cart_total + self.get_shipping_cost
	@property
	def get_estimated_tax(self):
		return self.get_cart_totalplus_shipping * Decimal('0.1')  
	@property
	def get_cart_totalplus_shipping_and_tax(self):
		return self.get_cart_totalplus_shipping + self.get_estimated_tax

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
    
	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address