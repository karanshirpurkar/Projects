from django.db import models

# Create your models here.
class Register(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    email=models.TextField(max_length=50)
    password=models.TextField(max_length=20)
    date=models.DateTimeField()

class upload(models.Model):
    file=models.FileField(upload_to="data/",default=None)