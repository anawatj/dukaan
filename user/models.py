from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
class CustomUser(AbstractUser):
    class Types(models.TextChoices):
        SELLER = "SELLER", "Seller"
        CUSTOMER = "CUSTOMER", "Customer"
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile_number = models.CharField(validators=[mobile_regex], max_length=17, blank=True)
    user_type = models.CharField(
        max_length=20, choices=Types.choices, default=Types.SELLER
    )
    address = models.TextField(null=True)
