from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from . import views
from .views import CommentViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register(r'comments', CommentViewSet, basename='CommentViewSet')
router.register(r'products', ProductViewSet, basename='ProductViewSet')

urlpatterns = [
    # path('', include(router.urls)),
    path('api/', include(router.urls)),
    url(r'^(?P<category_slug>[-\w]+)/$', views.ProductList, name='ProductListByCategory'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.ProductDetail, name='ProductDetail'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/addcomment', views.addcomment, name='addcomment'),
    url(r'^$', views.ProductList, name='ProductList'),
]
