from django.db import models
from user.models import CustomUser
class Store(models.Model):
    name = models.CharField(max_length=100,unique=True)
    address = models.TextField(null=True)
    seller = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

