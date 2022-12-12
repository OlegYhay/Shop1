from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
from shop.models import Product, Category


class TestProduct(APITestCase):
    def setUp(self) -> None:
        category = Category(
            title='Test category',
            slug='test_category',
        )
        category.save()

        product1 = Product(
            title='Тестовый товар 1',
            sku='тест',
            slug='test',
            category=category,
            price=155,
            status='В наличии',
        )
        product1.save()
        self.product = product1

    def test_get_detail_product(self):
        url = reverse('product_retrieve', kwargs={'pk': 1})
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.product.title)

    def test_get_list_products(self):
        url = reverse('product_list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK),
