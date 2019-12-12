from django.test import TestCase
from shop.urls import *
from shop.models import Product, Category, Comments

class CategorytModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
       Category.objects.create(name='Алмазная вышивка', slug='almaznaya-vyshivka')
       Category.objects.create(name='Картина по номерам', slug='kartina-po-nomeram')

    def test_name_length(self):
        category=Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_slug_length(self):
        category=Category.objects.get(id=1)
        max_length = category._meta.get_field('slug').max_length
        self.assertEquals(max_length, 200)

    def test_name_is_category(self):
        category=Category.objects.get(id=1)
        expected_name = '%s' % (category.name)
        self.assertEquals(expected_name, str(category))

    def test_get_absolute_url(self):
        category=Category.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(category.get_absolute_url(), '/almaznaya-vyshivka/')

    def test_category_filtering(self):
        categories = Category.objects.all()
        self.assertEqual(categories.count(), 2)

class ProducttModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods

       Category.objects.create(name='Картина по номерам', slug='kartina-po-nomeram')
       Product.objects.create(category=Category(id=1), name='Рассвет', slug='rassvet', price=2000, stock=4)
       Product.objects.create(category=Category(id=1), name='Закат', slug='zakat', price=1000, stock=40)
       Product.objects.create(category=Category(id=1), name='Ведьмак', slug='vedmak', price=5000, stock=1)

    def test_name_length(self):
        product=Product.objects.get(id=1)
        max_length = product._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_slug_length(self):
        product=Product.objects.get(id=1)
        max_length = product._meta.get_field('slug').max_length
        self.assertEquals(max_length, 200)

    def test_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')

    def test_category_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('category').verbose_name
        self.assertEquals(field_label, 'Категория')

    def test_price_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('price').verbose_name
        self.assertEquals(field_label, 'Цена')

    def test_stock_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('stock').verbose_name
        self.assertEquals(field_label, 'На складе')

    def test_get_absolute_url(self):
        product=Product.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(product.get_absolute_url(), '/1/rassvet/')

    def test_product_filtering(self):
        products = Product.objects.all()
        self.assertEqual(products.count(), 3)

class CommentsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods

       Category.objects.create(name='Картина по номерам', slug='kartina-po-nomeram')
       Product.objects.create(category=Category(id=1), name='Рассвет', slug='rassvet', price=2000, stock=4)
       Comments.objects.create(comments_text='bla-bla-bla', comments_product=Product(id=1), author='Nobody')

    def test_author_length(self):
        comments=Comments.objects.get(id=1)
        max_length = comments._meta.get_field('author').max_length
        self.assertEquals(max_length, 200)

    def test_comments_text_label(self):
        comments=Comments.objects.get(id=1)
        field_label = comments._meta.get_field('comments_text').verbose_name
        self.assertEquals(field_label, 'Комментарии')

    def test_author_label(self):
        comments=Comments.objects.get(id=1)
        field_label = comments._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'Автор')

    def test_comment_filtering(self):
        comments = Comments.objects.all()
        self.assertEqual(comments.count(), 1)