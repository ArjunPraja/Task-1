from django.db import models
from django.contrib.auth.models import User
from django.db import models

class ClothingItem(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('K', 'Kids'),
    ]
    JAUNERS_CHOICES = [
        ('NEWS_SALES', 'News & Sales'),
        ('CLOTHING', 'Clothing'),
        ('SHOES', 'Shoes'),
        ('ACCESSORIES', 'Accessories'),
        ('BAGS', 'Bags'),
        ('JEWELRY', 'Jewelry'),
        ('BRANDS', 'Brands'),
        ("ALL_WOMEN", "All Women's"),
        ('SUMMER', "Summer Women's"),
        ('POOL_PARTY', "Pool Party"),
        ('STYLISH_DRESSES', 'Stylish Dresses'),
        ('SUMMER_PARTY', 'Summer Party'),
        ('SPORTY', 'Sporty'),
        ('AESTHETICS', 'Aesthetics'),
    ]

    name = models.CharField(max_length=100, verbose_name="Clothing Name")
    description = models.TextField(verbose_name="Description")
    photo = models.ImageField(upload_to='clothing_photos/', verbose_name="Photo")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Gender")
    jauners = models.CharField(max_length=20, choices=JAUNERS_CHOICES, verbose_name="Jauners")
    price = models.IntegerField(verbose_name="Price")  # Fixed here

    def __str__(self):
        return self.name

class Cart(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    is_paid=models.BooleanField(default=False)
    rasor_pay_model_id=models.CharField(max_length=100, null=True, blank=True)
    rasor_pay_payment_id=models.CharField(max_length=100, null=True, blank=True)
    rasor_pay_payment_signature=models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Cart - {self.clothing_item.name}"

    def total_price(self):
        return self.clothing_item.price * self.quantity
    
