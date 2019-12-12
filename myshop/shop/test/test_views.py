from django.test import TestCase

# Create your tests here.

from shop.models import *
from django.urls import reverse


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