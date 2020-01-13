from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from django.contrib import auth
from cart.forms import CartAddProductForm
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from shop.models import Product, Comments
from .forms import CommentForm
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from .serializers import CommentSerializer, ProductDetailSerializer, ProductListSerializer
from rest_framework.response import Response
from core.views import ActionSerializedViewSet


#from django.template import RequestContext
#from django.template.context_processors import csrf

# Страница с товарами

def ProductList(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })
# Страница товара
def ProductDetail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    comments = Comments.objects.filter(comments_product=id)
    cart_product_form = CartAddProductForm()
    form_comments = CommentForm
    #context = {'product': product, 'cart_product_form': cart_product_form}
    #context.update(csrf(request))
    #return render_to_response('shop/detail.html', context)
    return render(request, 'shop/product/detail.html',
                             {'product': product,
                              'comments': comments,
                              'form_comments':form_comments,
                              'cart_product_form': cart_product_form})


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/"

    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)


def addcomment(request, id, slug):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user.username
            comment.comments_product = Product.objects.get(id=id)
            form.save()
    return HttpResponseRedirect('/%s/%s/' % (id, slug))

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()

class ProductViewSet(ActionSerializedViewSet):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()

    action_serializers = {
        'list': ProductListSerializer,
        'retrieve': ProductDetailSerializer,
    }

# class ProductDetailViewSet(viewsets.ModelViewSet):
#     serializer_class = ProductDetailSerializer
#     queryset = Product.objects.all()

