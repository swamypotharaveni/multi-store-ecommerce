from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("owner", "Store Owner"),
        ("employee", "Employee"),
        ("customer", "Customer"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)

    def save(self,*args,**kwargs):
        if self.is_superuser:
            self.role == 'admin'
        return super().save(*args,**kwargs)

    def __str__(self):
        return self.username
