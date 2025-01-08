from django.db import models
from django.contrib.auth.models import User
class ClothingItem(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('K', 'Kids'),
    ]

    name = models.CharField(max_length=100, verbose_name="Clothing Name")
    description = models.TextField(verbose_name="Description")
    photo = models.ImageField(upload_to='clothing_photos/', verbose_name="Photo")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Gender")
    price = models.IntegerField(name="price", verbose_name="Price")

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}'s Cart - {self.clothing_item.name}"

    def total_price(self):
        return self.clothing_item.price * self.quantity
