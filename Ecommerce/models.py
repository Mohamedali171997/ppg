from django.db import models


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
    list_quantity = models.CharField(max_length=2,choices=[
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10')
    ], default='1')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    #todo in future add a field for the product category
    stock = models.PositiveIntegerField()
    is_solde = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    
    # def __str__(self):
    #     return f"Cart Item: {self.product.name} (x{self.quantity})"
    # def total_price(self):
    #     return self.product.price * self.quantity
    
    # def is_in_stock(self):
    #     return self.product.stock >= self.quantity
    
    # def is_on_sale(self):
    #     return self.product.is_solde
    
    # def is_available(self):
    #     return self.product.stock > 0 and not self.product.is_solde
    

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    Customer = models.ForeignKey('Customer', on_delete=models.CASCADE) 
    order_date = models.DateTimeField(auto_now_add=True) 

    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    


    def __str__(self):
        return f"Order {self.id} - {self.cart.id}"
    
    def total_price(self):
        return self.cart.product.price
    
    def is_shipped(self):
        return self.status == 'shipped'
    def is_delivered(self):
        return self.status == 'delivered'
    def is_cancelled(self):
        return self.status == 'cancelled'
    def is_pending(self):
        return self.status == 'pending'
    
    
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=[
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer')
    ], default='credit_card')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

