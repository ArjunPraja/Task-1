from django.contrib import admin
from .models import ClothingItem

class ClothingItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'price', 'photo')
    search_fields = ('name', 'description')
    list_filter = ('gender',)

admin.site.register(ClothingItem, ClothingItemAdmin)
