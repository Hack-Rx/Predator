from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)

class Food(models.Model):
    uploader = models.ForeignKey(profile, on_delete=models.CASCADE)



