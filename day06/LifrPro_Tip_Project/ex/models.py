from django.db import models
from django.conf import settings

# class UserData(models.Model):
#     id = models.CharField(max_length=64, null=False, primary_key=True)
#     pw = models.CharField(max_length=64, null=False)
#     created = models.DateTimeField(auto_now_add=True, null=False)
#     updated = models.DateTimeField(auto_now=True, null=False)

#     def __str__(self):
#         return str(self.title)

class TipModel(models.Model):
    content = models.TextField(null=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)