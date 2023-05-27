from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORY_CHOICES =(
    ('sofa', 'Sofa'),
    ('table', 'Tables'),
    ('chair', 'Chairs'),
    ('storage', 'Storages'),
    ('bed', 'Beds'),
    ('desk', 'Desks'),
    ('book', 'Bookcases'),
    ('cup', 'Cupboard'),
)

STATE_CHOICES = (
    ('ALMATY', 'ALMATY OBLYSY'),
    ('ZKO', 'ZKO'),
    ('ATYRAU', 'ATYRAU OBLYSY' ),
    ('MANGYSTAU', 'MANGYSTAU OBLYSY'),
    ('AKTOBE', 'AKTOBE OBLYSY'),
    ('KYZYLORDA', 'KYZYLORDA OBLYSY'),
    ('TURKISTAN', 'TURKISTAN OBLYSY'),
    ('KOSTANAY', 'KOSTANAY OBLYSY'),
    ('SKO', 'SKO'),
    ('AKMOLA', 'AKMOLA OBLYSY'),
    ('KARAGANDY', 'KARAGANDY OBLYSY'),
    ('ULYTAU', 'ULYTAU OBLYSY'),
    ('ZHAMBYL', 'ZHAMBYL OBLYSY'),
    ('PAVLODAR', 'PAVLODAR OBLYSY'),
    ('ABAY', 'ABAY OBLYSY'),
    ('ZHETISU', 'ZHETISU OBLYSY'),
    ('VKO', 'VKO'),
)

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending'),
)

class Products(models.Model):
    title = models.CharField(max_length=50)
    selling_price = models.IntegerField()
    discounted_price = models.IntegerField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    product_image = models.ImageField(null=True, upload_to='media/product')
    file = models.FileField(null=True, upload_to='media/file')
    def __str__(self):
        return self.title

class Customers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField()
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=10)
    def __str__(self):
        return self.name

class Carts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total(self):
        return self.quantity * self.product.discounted_price


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    razorpay_order_id = models.CharField(max_length=50, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=50, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=50, blank=True, null=True)
    paid = models.BooleanField(default=False)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)