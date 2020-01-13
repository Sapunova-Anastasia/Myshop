from .models import Comments, Product
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('id', 'comments_text', 'comments_product', 'author')

class ProductDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'slug', 'image', 'description', 'price', 'stock', 'available', 'created', 'updated', 'comments', 'comments_count')

class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'slug', 'description', 'price', 'stock')
