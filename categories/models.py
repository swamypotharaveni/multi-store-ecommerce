from django.db import models
from django.utils.text import slugify
# Create your models here.

class Categories (models.Model):
    name = models.CharField(max_length=600)
    description = models.TextField()
    image = models.ImageField(upload_to='images/categories/' , )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class SubCategories (models.Model):
    name = models.CharField(max_length=600)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE,  related_name='subcategory')
    image = models.ImageField(upload_to='images/subcategories/' , )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Brands (models.Model):
    name = models.CharField(max_length=600)

    def __str__(self):
        return self.name
    

