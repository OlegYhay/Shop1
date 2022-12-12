from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductListApiView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductRetrieveApiView.as_view(), name='product_retrieve')
]

