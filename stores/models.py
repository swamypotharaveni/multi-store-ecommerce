from django.db import models
from users.models import CustomUser
# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE,related_name="branches"),
    STORE_TYPES = (("main", "Main Store"),("branch", "Branch"),("warehouse", "Warehouse"),)

    store_type = models.CharField(max_length=50, choices=STORE_TYPES)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    updated_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class StoreAddress(models.Model):
    store = models.OneToOneField(Store, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

class StoreSetting(models.Model):
    store = models.OneToOneField(Store, on_delete=models.CASCADE)
    delivery_enabled = models.BooleanField(default=True)
    pickup_enabled = models.BooleanField(default=True)
class StoreDocument(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)
    # file = models.FileField(upload_to="store_docs/")