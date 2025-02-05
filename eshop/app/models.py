from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models


class Product(models.Model):
    pro_id = models.TextField()  # Product ID
    name = models.TextField()  # Product name
    price = models.IntegerField()  # Product price
    ofr_price = models.IntegerField()  # Offer price
    img = models.FileField()  # Product image
    dis = models.TextField()  # Product description
    ram = models.CharField(max_length=50, blank=True, null=True)  # RAM size (e.g., "8GB", "16GB")
    storage = models.CharField(max_length=50, blank=True, null=True)  # Storage size (e.g., "128GB", "256GB")

    def __str__(self):
        return self.name


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)


class Buy(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.IntegerField()
    date=models.DateField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ram = models.CharField(max_length=50, null=True, blank=True)
    storage = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"