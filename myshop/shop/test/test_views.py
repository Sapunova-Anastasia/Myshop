import json

from shop.models import *
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..serializers import ProductDetailSerializer, ProductListSerializer

User = get_user_model()
# initialize the APIClient app
client = Client()

class ProductListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_products = 26
        Category.objects.create(name='Картина по номерам', slug='kartina-po-nomeram')
        for products_num in range(number_of_products):
            Product.objects.create(category=Category(id=1), name='Продукт %s' % products_num, slug='product-%s' % products_num, price=2000, stock=4)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/kartina-po-nomeram/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('shop:ProductListByCategory', args=['kartina-po-nomeram']))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('shop:ProductListByCategory', args=['kartina-po-nomeram']))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'shop/product/list.html')

    def test_view_url_exists_at_desired_location_product(self):
        resp = self.client.get('/8/product-7/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_exists_at_desired_location_product_404(self):
        resp = self.client.get('/28/product-27/')
        self.assertEqual(resp.status_code, 404)

    def test_view_url_accessible_by_name_product(self):
        resp = self.client.get(reverse('shop:ProductDetail', args=[8, 'product-7']))
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name_product_404(self):
        resp = self.client.get(reverse('shop:ProductDetail', args=[13, 'product-7']))
        self.assertEqual(resp.status_code, 404)

    def test_view_uses_correct_template_product(self):
        resp = self.client.get(reverse('shop:ProductDetail', args=[8, 'product-7']))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'shop/product/detail.html')

class GetAllProductsTest(TestCase):
    """ Test module for GET all posts API """
    def setUp(self):
        Category.objects.create(name='Картина по номерам', slug='kartina-po-nomeram')
        Product.objects.create(category=Category(id=1), name='Рассвет', slug='rassvet', price=2000, stock=4)
        Product.objects.create(category=Category(id=1), name='Закат', slug='zakat', price=1000, stock=40)
        Product.objects.create(category=Category(id=1), name='Ведьмак', slug='vedmak', price=5000, stock=1)

    def test_get_all_products(self):
        # get API response
        response = self.client.get('/api/products/')
        # get data from db
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSingleProductTest(TestCase):
    """ Test module for GET single post API """
    def setUp(self):
        Category.objects.create(name='Картина по номерам', slug='kartina-po-nomeram')
        Product.objects.create(category=Category(id=1), name='Рассвет', slug='rassvet', price=2000, stock=4)

    def test_get_valid_single_product(self):
        response = self.client.get('/api/products/1/')
        product = Product.objects.get(pk=1)
        serializer = ProductDetailSerializer(product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_product(self):
        response = self.client.get('/api/products/2/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateNewProductTest(TestCase):
    """ Test module for POST a new post API """
    def setUp(self):
        Category.objects.create(name='Картина по номерам', slug='kartina-po-nomeram')
        self.valid_payload = {
                                'category': 1,
                                'name': 'gfjhgjhgj',
                                 'slug': 'gfjhgjhgj',
                                 'description': 'bla',
                                 'price': 1,
                                 'stock': 1,
                            }
        self.invalid_payload = {
            'category': 'Картина по номерам',
            'description': 'Корабль на море',
            'price': 1000,
            'stock': 4,
        }

    def test_create_valid_single_post(self):
        response = client.post('/api/products/',
                               data=json.dumps(self.valid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_single_post(self):
        response = client.post('/api/products/',
                               data=json.dumps(self.invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSingleProductTest(TestCase):
    """ Test module for updating an existing post record """
    def setUp(self):
        Category.objects.create(name='Картина по номерам', slug='kartina-po-nomeram')
        Product.objects.create(category=Category(id=1), name='Ведьмак', slug='vedmak', price=5000, stock=1)

        self.valid_payload = {
                                'category': 1,
                                'name': 'Ведьмак',
                                 'slug': 'vedmak',
                                 'description': 'bla',
                                 'price': 3000,
                                 'stock': 5,
                            }
        self.invalid_payload = {
                                'category': 1,
                                'name': 'Ведьмак',
                                 'slug': 'vedmak',
                                 'description': 'bla',
                                 'price': 3000,
                                 'stock': None,
                                }

    def test_valid_update_product(self):
        response = client.put('/api/products/1/',
                              data=json.dumps(self.valid_payload),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_product(self):
        response = client.put('/api/products/1/',
                              data=json.dumps(self.invalid_payload),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteSingleProductTest(TestCase):
    """ Test module for deleting an existing post record """
    def setUp(self):
        Category.objects.create(name='Картина по номерам', slug='kartina-po-nomeram')
        Product.objects.create(category=Category(id=1), name='Ведьмак', slug='vedmak', price=5000, stock=1)

    def test_valid_delete_product(self):
        response = client.delete('/api/products/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_product(self):
        response = client.delete('/api/products/2/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)