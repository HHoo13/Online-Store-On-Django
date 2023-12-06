import json

from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Sum, Count
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test.utils import CaptureQueriesContext

from api.models import Product, Category
from api.serializers import ProductSerializer, CategorySerializer



class ProductApiTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', first_name='Ivan', last_name='Petrov', is_staff=True)
        self.user2 = User.objects.create(username='user2', first_name='Dima', last_name='Sidorov', is_staff=False)
        self.user3 = User.objects.create(username='user3', first_name='Vadim', last_name='Kuzmin')
        self.product1 = Product.objects.create(title='Product1', description='Product1 description', price=100,
                                               made_in=1, stock=10)
        self.product2 = Product.objects.create(title='Product2', description='Product2 description', price=200,
                                               made_in=1, stock=20)
        self.product3 = Product.objects.create(title='Product3', description='Product3 description', price=300,
                                               made_in=1, stock=30)
        self.client.force_login(self.user1)

    def test_get(self):
        url = reverse('product-list')  # это имя таблицы в бд
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(3, len(queries))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        product = Product.objects.all()
        product_data = ProductSerializer(product, many=True).data
        self.assertEqual(product_data, response.data)

    def test_get_filter(self):
        url = reverse('product-list')
        response = self.client.get(url, data={'price': 200})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        product = Product.objects.filter(id__in=[self.product2.id, ])
        product_data = ProductSerializer(product, many=True).data
        self.assertEqual(product_data, response.data)

    def test_get_ordering(self):
        url = reverse('product-list')
        response = self.client.get(url, data={'ordering': 'price'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        product = Product.objects.all()
        product_data = ProductSerializer(product, many=True).data
        self.assertEqual(product_data, response.data)

    def test_get_search(self):
        url = reverse('product-list')
        response = self.client.get(url, data={'search': 'Product1'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        product = Product.objects.filter(id__in=[self.product1.id])
        product_data = ProductSerializer(product, many=True).data
        self.assertEqual(product_data, response.data)

    def test_post_is_staff(self):
        self.assertEqual(3, Product.objects.all().count())
        url = reverse('product-list')
        data = {
            "title": "Product4",
            "description": "Product4 description",
            "price": 500.0,
            "made_in": 2,
            'stock': 5
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Product.objects.all().count())

    def test_post_is_not_staff(self):
        self.assertEqual(3, Product.objects.all().count())
        url = reverse('product-list')
        data = {
            "title": "Product4",
            "description": "Product4 description",
            "price": 500.0,
            "made_in": 2,
            'stock': 5
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(3, Product.objects.all().count())

    def test_update_is_staff(self):
        url = reverse('product-detail', args=(self.product1.id,))
        data = {
            "title": "Product1",
            "description": "Product1 description",
            "price": 500,
            "made_in": 1,
            'stock': 10
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.product1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(500, self.product1.price)
        self.assertEqual(3, Product.objects.all().count())

    def test_update_is_not_staff(self):
        url = reverse('product-detail', args=(self.product1.id,))
        data = {
            "title": "Product1",
            "description": "Product1 description",
            "price": 500,
            "made_in": 1,
            'stock': 10
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user3)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.product1.refresh_from_db()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(100, self.product1.price)
        self.assertEqual(3, Product.objects.all().count())

    def test_delete_is_staff(self):
        url = reverse('product-detail', args=(self.product1.id,))
        data = Product.objects.get(id=self.product1.id)
        self.client.force_login(self.user1)
        response = self.client.delete(url, data=data, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Product.objects.all().count())

    def test_delete_is_not_staff(self):
        url = reverse('product-detail', args=(self.product1.id,))
        data = Product.objects.get(id=self.product1.id)
        self.client.force_login(self.user2)
        response = self.client.delete(url, data=data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(3, Product.objects.all().count())



class CategoriesApiTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', first_name='Ivan', last_name='Petrov', is_staff=True)
        self.user2 = User.objects.create(username='user2', first_name='Dima', last_name='Sidorov', is_staff=False)
        self.user3 = User.objects.create(username='user3', first_name='Vadim', last_name='Kuzmin')
        self.category1 = Category.objects.create(category_name='Category1',
                                                 category_description='Category1 description')
        self.category2 = Category.objects.create(category_name='Category2',
                                                 category_description='Category2 description')
        self.category3 = Category.objects.create(category_name='Category3',
                                                 category_description='Category3 description')

    def test_get(self):
        url = reverse('category-list')
        self.client.force_login(self.user2)
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(3, len(queries))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        category = Category.objects.all().annotate(all_products=Count('product__id'))
        category_data = CategorySerializer(category, many=True).data
        self.assertEqual(category_data, response.data)

    def test_get_ordering(self):
        url = reverse('category-list')
        response = self.client.get(url, data={'ordering': 'category_name'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        category = Category.objects.all().annotate(all_products=Count('product__id'))
        category_data = CategorySerializer(category, many=True).data
        self.assertEqual(category_data, response.data)

    def test_post_is_staff(self):
        self.assertEqual(3, Category.objects.all().annotate(all_products=Count('product__id')).count())
        url = reverse('category-list')
        data = {
            "category_name": "Category4",
            "category_description": "Category4 description",
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Category.objects.all().annotate(all_products=Count('product__id')).count())

    def test_post_is_not_staff(self):
        self.assertEqual(3, Category.objects.all().count())
        url = reverse('category-list')
        data = {
            "category_name": "Category4",
            "category_description": "Category4 description",
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user3)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(3, Category.objects.all().annotate(all_products=Count('product__id')).count())

    def test_update_is_staff(self):
        url = reverse('category-detail', args=(self.category1.id,))
        data = {
            "category_name": "Category4",
            "category_description": "Category1 description",
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user1)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.category1.refresh_from_db()
        self.assertEqual('Category4', self.category1.category_name)
        self.assertEqual(3, Category.objects.all().annotate(all_products=Count('product__id')).count())

    def test_update_is_not_staff(self):
        url = reverse('category-detail', args=(self.category1.id,))
        data = {
            "category_name": "Category4",
            "category_description": "Category4 description",
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user3)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.category1.refresh_from_db()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual('Category1', self.category1.category_name)
        self.assertEqual(3, Category.objects.all().annotate(all_products=Count('product__id')).count())

    def test_delete_is_staff(self):
        url = reverse('category-detail', args=(self.category1.id,))
        data = Category.objects.get(id=self.category1.id)
        self.client.force_login(self.user1)
        response = self.client.delete(url, data=data, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Category.objects.all().annotate(all_products=Count('product__id')).count())

    def test_delete_is_not_staff(self):
        url = reverse('category-detail', args=(self.category1.id,))
        data = Category.objects.get(id=self.category1.id)
        self.client.force_login(self.user2)
        response = self.client.delete(url, data=data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(3, Category.objects.all().annotate(all_products=Count('product__id')).count())
