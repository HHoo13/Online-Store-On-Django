import json

from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.test import TestCase

from api.models import Product, Category, Tag, Buyer
from api.serializers import ProductSerializer, CategorySerializer


class ApiSerializerTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', first_name='Ivan', last_name='Petrov', is_staff='t')
        self.user2 = User.objects.create(username='user2', first_name='Dima', last_name='Sidorov')
        self.user3 = User.objects.create(username='user3', first_name='Vadim', last_name='Kuzmin')
        self.category1 = Category.objects.create(category_name='test_category1',
                                                 category_description='category_description_test1')
        self.category2 = Category.objects.create(category_name='test_category2',
                                                 category_description='category_description_test2')
        self.category3 = Category.objects.create(category_name='test_category3',
                                                 category_description='category_description_test3')
        self.tag1 = Tag.objects.create(name='test_tag1')
        self.tag2 = Tag.objects.create(name='test_tag2')
        self.tag3 = Tag.objects.create(name='test_tag3')
        self.product1 = Product.objects.create(title='Product1', description='Product1 description', price=100,
                                               made_in=1, stock=10, category_of_product=self.category1,
                                               tag1=self.tag1, tag2=self.tag2, tag3=self.tag3)
        self.product2 = Product.objects.create(title='Product2', description='Product2 description', price=200,
                                               made_in=1, stock=20, category_of_product=self.category2,
                                               tag1=self.tag3, tag2=self.tag2)
        self.product3 = Product.objects.create(title='Product3', description='Product3 description', price=300,
                                               made_in=1, stock=30, category_of_product=self.category3, tag2=self.tag2)

        self.buyer1 = Buyer.objects.create(User=self.user1, phone_number='992987654321')
        self.buyer2 = Buyer.objects.create(User=self.user2, phone_number='992987654322')
        self.buyer3 = Buyer.objects.create(User=self.user3, phone_number='992987654323')

    def test_serializers(self):
        #  Products
        product = Product.objects.all()
        product_data = ProductSerializer(product, many=True).data
        json_data = json.dumps(product_data)
        product_data1 = [
            {
                "title": "Product1",
                "description": "Product1 description",
                "price": 100.0,
                "made_in": 1,
                "main_picture": None,
                "second_picture": None,
                "third_picture": None,
                "forth_picture": None,
                "fifth_picture": None,
                "first_video": None,
                "second_video": None,
                "stock": 10,
                "category_of_product": self.category1.id,
                "tag1": self.tag1.id,
                "tag2": self.tag2.id,
                "tag3": self.tag3.id,
            },
            {
                "title": "Product2",
                "description": "Product2 description",
                "price": 200.0,
                "made_in": 1,
                "main_picture": None,
                "second_picture": None,
                "third_picture": None,
                "forth_picture": None,
                "fifth_picture": None,
                "first_video": None,
                "second_video": None,
                "stock": 20,
                "category_of_product": self.category2.id,
                "tag1": self.tag3.id,
                "tag2": self.tag2.id,
                "tag3": None
            },
            {
                "title": "Product3",
                "description": "Product3 description",
                "price": 300.0,
                "made_in": 1,
                "main_picture": None,
                "second_picture": None,
                "third_picture": None,
                "forth_picture": None,
                "fifth_picture": None,
                "first_video": None,
                "second_video": None,
                "stock": 30,
                "category_of_product": self.category3.id,
                "tag1": None,
                "tag2": self.tag2.id,
                "tag3": None
            }
        ]

        self.assertEqual(product_data1, json.loads(json_data))


        # Categories
        category = Category.objects.all().annotate(all_products=Count('product__id'))
        category_data = CategorySerializer(category, many=True).data
        json_data = json.dumps(category_data)
        category_data1 = [
            {
                "category_name": "test_category1",
                "category_picture": None,
                "category_description": "category_description_test1",
                "all_products": 1
            },
            {
                "category_name": "test_category3",
                "category_picture": None,
                "category_description": "category_description_test3",
                "all_products": 1
            },
            {
                "category_name": "test_category2",
                "category_picture": None,
                "category_description": "category_description_test2",
                "all_products": 1
            }
        ]
        self.assertEqual(category_data1, json.loads(json_data))
