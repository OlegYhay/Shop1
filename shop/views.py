from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveAPIView, ListAPIView
from shop.models import Product
from shop.serializers import SerializerProduct


class ProductRetrieveApiView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = SerializerProduct


class ProductListApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = SerializerProduct
    # Необходимые фильтры по заданию
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status']
    search_fields = ['sku', 'title']
