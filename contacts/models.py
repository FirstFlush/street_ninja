from django.db import models
from .enums import ContactMethodEnum


class Contact(models.Model):

    name = models.CharField(max_length=256)
    organization = models.CharField(max_length=256, null=True)
    email = models.EmailField(max_length=256)
    phone = models.CharField(max_length=20)
    contactMethod = models.CharField(choices=ContactMethodEnum.choices)
    msg = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)