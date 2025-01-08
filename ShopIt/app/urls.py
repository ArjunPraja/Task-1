from django.contrib import admin
from django.urls import path, include
from .views import home, clothing_list, add_clothing, view_cart, add_to_cart
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home, name='home'),
    path('add/', add_clothing, name='addcloth'),
    path('clothing_list/', clothing_list, name='clothing_list'),  # For all items
    path('clothing_list/<str:category>/', clothing_list, name='clothing_list_by_category'),
    path('view_cart/', view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)