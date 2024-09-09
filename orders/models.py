from django.db import models
from django.core.validators import RegexValidator
from inventories.models import Product
class Order(models.Model):
    mobile_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile_number = models.CharField(validators=[mobile_regex], max_length=17, blank=True)
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    class PaymentMethod(models.TextChoices):
        VISA = "VISA", "Visa"
        MASTERCARD = "MASTERCARD", "MASTERCARD"
    payment_method = models.CharField(
        max_length=20, choices=PaymentMethod.choices,null=True
    )
    credit_card_number = models.CharField(max_length=100)
    credit_card_holder = models.CharField(max_length=200)

    class OrderStatus(models.TextChoices):
        DRAFTED = "DRAFTED","Draft"
        CREATED = "CREATED","Created",
        SUCCESS = "SUCCESS","Success"
    order_status = models.CharField(
        max_length=20, choices=OrderStatus.choices,null=True
    )

    def __str__(self):
        return self.mobile_number

class OrderItem(models.Model):
    qty=models.IntegerField(null=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,parent_link=True)
    def __str__(self):
        return self.product.name+"|"+self.cart.mobile_number

    def can_order(self):
        product = Product.objects.get(id=self.product.id)
        return product.qty>0 and product.qty>=self.qty
