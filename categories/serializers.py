from .models import Categories, SubCategories, Brands
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategories
        fields =  '__all__'

class CategorySubCategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(read_only=True)
    class Meta:
        model =  Categories
        fields = ['id', 'name', 'image', 'sub_categories']


class BrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = '__all__'