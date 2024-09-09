from django.db import models
from django.core.validators import RegexValidator
from inventories.models import Product
class Cart(models.Model):
    mobile_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile_number = models.CharField(validators=[mobile_regex], max_length=17, blank=True)
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    def __str__(self):
        return self.mobile_number

class CartItem(models.Model):
    qty=models.IntegerField(null=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,parent_link=True)
    def __str__(self):
        return self.product.name+"|"+self.cart.mobile_number
    def can_order(self):
        return self.product.qty>0 and self.product.qty>=self.qty

