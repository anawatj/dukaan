from rest_framework import status
from rest_framework.response import Response
from decimal import *
from functools import reduce
from user.permissions import IsSeller
from user.models import CustomUser
from stores.models import Store
from inventories.models import Product
from carts.models import CartItem,Cart

def add_cart(request):
    data = request.data
    errors= validate(data)
    if len(errors)>0:
        Response({
            "error":",".join(errors)
        },status=status.HTTP_400_BAD_REQUEST)
    try:
        result = Cart.objects.get(mobile_number=data.get("mobile_number"))
    except Cart.DoesNotExist:
        result = None
    if not result :
        c=Cart.objects.create(
            mobile_number=data.get("mobile_number"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name")
        )
        c.save()
    else:
        c = result
    items = data.get("cartItems")
    CartItem.objects.filter(cart__id=c.id).delete()
    for item in items :
        p = Product.objects.get(id=item["product"]["id"])
        if p :
            ci = CartItem.objects.create(
                cart=c,
                product=p,
                qty=item["qty"]
            )
            if ci.can_order():
                ci.save()


    cart_items = CartItem.objects.filter(cart__id=c.id)
    return Response({
        "data":{
            "mobile_number":c.mobile_number,
            "first_name":c.first_name,
            "last_name":c.last_name,
            "cartItems":[{
                "product":{
                    "id":cartItem.product.id,
                    "name":cartItem.product.name
                },
                "qty":cartItem.qty
            }for cartItem in cart_items]
        }
    },status=status.HTTP_200_OK)

def validate(data):
    errors = list()
    if (not data.get("mobile_number")) or data.get("mobile_number") == "" :
        errors.append("mobile number is required")
    if (not data.get("first_name")) or data.get("first_name")=="":
        errors.append("first name is required")
    if (not data.get("last_name")) or data.get("last_name")== "":
        errors.append("last name is required")
    return errors