from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    url(r'^(?P<category_slug>[-\w]+)/$', views.ProductList, name='ProductListByCategory'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.ProductDetail, name='ProductDetail'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/addcomment', views.addcomment, name='addcomment'),
    url(r'^$', views.ProductList, name='ProductList'),
]
