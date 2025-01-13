from django.contrib import admin
from .models import ClothingItem,Cart


class ClothingItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'price', 'photo')
    search_fields = ('name', 'description')
    list_filter = ('gender',)

admin.site.register(ClothingItem, ClothingItemAdmin)
admin.site.register(Cart)
