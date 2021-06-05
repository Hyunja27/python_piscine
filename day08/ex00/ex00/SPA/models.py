from django.db import models
# Create your models here.

class ImageModel(models.Model):
    image = models.ImageField(blank=True)
    title = models.CharField(max_length=40, blank=False)
