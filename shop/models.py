from django.contrib.auth.models import User
from django.db import models

class CategoryShop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS = (
        ('Disponible', 'Disponible'),
        ('Agotado', 'Agotado')
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    image = models.ImageField(upload_to='items/', null=True)
    category = models.ForeignKey(CategoryShop, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=100, null=True, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.nam} ({self.product.name})"


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

