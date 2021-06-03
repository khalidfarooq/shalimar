# from djongo import models
from cryptography.fernet import Fernet
from django_cryptography.fields import encrypt
from cryptography.fernet import Fernet
from django.db import models

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='static/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)