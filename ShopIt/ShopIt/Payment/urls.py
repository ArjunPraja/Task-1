from django.urls import path, include
from .views import pay
urlpatterns = [
  # Include the URLs from the 'accounts' app
    path('',pay,name='pay'),  # Include the URLs from the 'accounts' app
]
