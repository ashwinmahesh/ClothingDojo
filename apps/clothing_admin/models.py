from __future__ import unicode_literals
from django.db import models
import re

class ColorManager(models.Manager):
    def validate(self, postData):
        errors={}
        if(len(postData['color'])==0):
            errors['color']='Color cannot be empty'
        return errors

class ProductManager(models.Manager):
    def validate(self, postData):
        PRICE_REGEX=re.compile(r'^[0-9]*\.[0-9]{2}$')
        errors={}
        if(len(postData['product_name'])==0):
            errors['product_name']='Product name cannot be empty'
        if(len(postData['image_path'])==0):
            errors['image_path']='Image path cannot be empty'
        if not PRICE_REGEX.match(postData['price']):
            errors['price']='Price must be in the format of X.XX'
        if(len(postData['description'])==0):
            errors['description']='Product must have a description'
        # if(len(postData['color'])==0):
        #     errors['color']='Product must have atleast one color'
        return errors

class Product(models.Model):
    name=models.CharField(max_length=255)
    cost=models.DecimalField(max_digits=5, decimal_places=2)
    image_path=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    description=models.TextField(default='')
    # colors=models.ForeignKey(Color, related_name='product')
    objects=ProductManager()

class Color(models.Model):
    name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    product=models.ForeignKey(Product, related_name='colors', null=True)
    # rgb=models.CharField(max_length=14, null=True)

class Location(models.Model):
    name=models.CharField(max_length=255)
    street_address=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    state=models.CharField(max_length=2)
    zip_code=models.CharField(max_length=5)

class Cohort(models.Model):
    name=models.CharField(max_length=255)
    location=models.ForeignKey(Location, related_name='cohorts')
    start_date=models.DateField()

class Batch(models.Model):
    location=models.ForeignKey(Location, related_name='batches')
    status=models.CharField(max_length=50, default='Open')

class BatchItem(models.Model):
    product=models.ForeignKey(Product, related_name='batches')
    batch=models.ForeignKey(Batch, related_name='items')
    size=models.CharField(max_length=3)
    color=models.CharField(max_length=100)
    quantity=models.IntegerField()
    total=models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at=models.DateTimeField(auto_now_add=True)

# Create your models here.
