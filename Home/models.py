from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    email_id = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)