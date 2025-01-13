from django.contrib import admin
from django.urls import path, include
from .views import home, clothing_list, add_clothing, view_cart, add_to_cart, clothing_list1,Success,update_cart_item,delete_cart_item,paid_cart_items
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home, name='home'),  # Homepage
    path('add/', add_clothing, name='addcloth'),  # Add a clothing item
    path('clothing_list/', clothing_list, name='clothing_list'),  # View all items
    path('clothing_list/<str:category>/', clothing_list, name='clothing_list_by_category'),  # Filter by category
    path('clothing/<str:jauners>/', clothing_list1, name='clothing_list_by_jauners'),  # Filter by jauners
    path('view_cart/', view_cart, name='view_cart'),  # View shopping cart
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),  # Add item to cart
    path('success/', Success, name='success'),  # Add item to cart
   
    # Other URLs in your application
    path('cart/update/', update_cart_item, name='update_cart_item'),
    path('cart/delete/', delete_cart_item, name='delete_cart_item'),
 path('paid_item', paid_cart_items, name='paid_item'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)