from django.db import models
from stores.models import Store
from user.models import CustomUser
class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    qty = models.IntegerField(null=False)
    sale_price = models.DecimalField(max_digits=13,decimal_places=4)
    image = models.ImageField(upload_to="images",null=True)
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
