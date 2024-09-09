from rest_framework.response import Response
from rest_framework import status
from decimal import *
from stores.models import Store
from inventories.models import Product,Category
def get_by_id(request,id):
    try:
        result = Product.objects.get(id=id,seller=request.user)
    except Product.DoesNotExist:
        result = None
    if not result :
        return Response(
            {
                "error":"Not Found Product"
            },status=status.HTTP_404_NOT_FOUND)
    return Response({
        "data":{
            "id":result.id,
            "name":result.name,
            "category":{
                "id":result.category.id,
                "name":result.category.name
            },
            "seller":{
                "id":result.seller.id,
                "first_name":result.seller.first_name,
                "last_name":result.seller.last_name
            },
            "description":result.description,
            "qty":result.qty,
            "sale_price":result.sale_price
        }
    },status=status.HTTP_200_OK)

def get_all(request):
    results = Product.objects.filter(seller=request.user)
    if len(results)==0:
        return Response(
            {
                "error":"Not Found Product"
            },status=status.HTTP_404_NOT_FOUND)
    return Response({
        "data":[
            {
                "id":result.id,
                "name":result.name,
                "category":{
                    "id":result.category.id,
                    "name":result.category.name
                },
                "seller":{
                    "id":result.seller.id,
                    "first_name":result.seller.first_name,
                    "last_name":result.seller.last_name
                },
                "description":result.description,
                "qty":result.qty,
                "sale_price":result.sale_price
            } for result in results
        ]
    },status=status.HTTP_200_OK)
def delete(request,id):
    try:
        result = Product.objects.get(id=id,seller=request.user)
    except Product.DoesNotExist:
        result = None
    if not result :
        return Response(
            {
                "error":"Not Found Product"
            },status=status.HTTP_404_NOT_FOUND)
    result.delete()
    return Response({
        "data":"Success"
    },status=status.HTTP_200_OK)
def put(request,id):
    data = request.data
    errors = validate(data,"UPDATE")
    if len(errors)>0:
        return Response({
            "error":",".join(errors)
        },status=status.HTTP_400_BAD_REQUEST)


    try:
        result = Product.objects.get(id=id,seller=request.user)
    except Product.DoesNotExist:
        result = None
    if not result :
        return Response(
            {
                "error":"Not Found Product"
            },status=status.HTTP_404_NOT_FOUND)

    result.description = data.get("description")
    result.qty= data.get("qty")
    result.sale_price = Decimal(data.get("sale_price"))
    result.name = data.get("name")
    result.save()
    return Response({
        "data":{
            "id":result.id,
            "name":result.name,
            "qty":result.qty,
            "sale_price":result.sale_price,
            "description":result.description,
            "store":{
                "id":result.store.id,
                "name":result.store.name
            },
            "category":{
                "id":result.category.id,
                "name":result.category.name
            },
            "seller":{
                "id":result.seller.id,
                "first_name":result.seller.first_name,
                "last_name":result.seller.last_name
            }
        }
    },status=status.HTTP_200_OK)

def post(request):
    data = request.data
    errors = validate(data,"CREATE")
    if len(errors)>0:
        return Response({
            "error":",".join(errors)
        },status=status.HTTP_400_BAD_REQUEST)
    try:
        store = Store.objects.get(id=data.get("store")["id"],seller=request.user)
    except Store.DoesNotExist:
        store = None
    if not store:
        return Response({
            "error":"Store is not found"
        },status=status.HTTP_400_BAD_REQUEST)
    try:
        category = Category.objects.get(name=data.get("category")["name"],seller=request.user)
    except Category.DoesNotExist:
        category = None
    if not category :
        c=Category.objects.create(name=data.get("category")["name"],store=store,seller=request.user)
        c.save()
    else:
        c = category

    p = Product.objects.create(
        name=data.get("name"),
        category=c,
        store=store,
        seller=request.user,
        qty=data.get("qty"),
        sale_price = Decimal(data.get("sale_price")),
        description = data.get("description")
    )
    p.save()
    return Response({
        "data":{
            "id":p.id,
            "name":p.name,
            "qty":p.qty,
            "sale_price":p.sale_price,
            "description":p.description,
            "store":{
                "id":p.store.id,
                "name":p.store.name
            },
            "category":{
                "id":p.category.id,
                "name":p.category.name
            },
            "seller":{
                "id":p.seller.id,
                "first_name":p.seller.first_name,
                "last_name":p.seller.last_name
            }
        }
    },status=status.HTTP_201_CREATED)


def validate(data,mode):
    errors = list()
    if mode == "CREATE":
        if not data.get("category"):
            errors.append("Category is required")
        if not data.get("store"):
            errors.append("store is required")

    if (not data.get("name")) or data.get("name")=="":
        errors.append("Product Name is required")
    if not data.get("qty"):
        errors.append("Qty is required")
    if not data.get("sale_price"):
        errors.append("Sale Price is required")
    return errors
