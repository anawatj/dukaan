from django.shortcuts import render
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from decimal import *
from user.permissions import IsSeller
from user.models import CustomUser
from stores.models import Store
from inventories.models import Product,Category
# Create your views here.
@api_view(["GET","POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated,IsSeller])
def products(request):
    if request.method == "GET":
        return get_all_product(request)
    elif request.method=="POST":
        return post_product(request)
    else:
        return method_not_allow(request)

@api_view(["GET","PUT","DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated,IsSeller])
def product(request,id):
    if request.method=="GET":
        return get_by_id_product(request,id)
    elif request.method=="PUT":
        return put_product(request,id)
    elif request.method=="DELETE":
        return delete_product(request,id)
    else:
        return method_not_allow(request)



@api_view(["GET","POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated,IsSeller])
def categories(request):
    if request.method=="GET":
        return get_all_categories(request)
    elif request.method=="POST":
        return post_category(request)
    else:
        return method_not_allow(request)

@api_view(["GET","PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated,IsSeller])
def category(request,id):
    if request.method=="GET":
        return get_by_id_category(request,id)
    elif request.method=="PUT":
        return put_category(request,id)
    else:
        return method_not_allow(request)

def get_by_id_category(request,id):
    try:
        result = Category.objects.get(id=id,seller=request.user)
    except Category.DoesNotExist:
        result = None

    if not result :
        return Response(
            {
                "error":"Not Found Category"
            },status=status.HTTP_404_NOT_FOUND)
    return Response({
        "data":{
            "id":result.id,
            "name":result.name,
            "seller":{
                "id":result.seller.id,
                "first_name":result.seller.first_name,
                "last_name":result.seller.last_name
            },
            "store":{
                "id":result.store.id,
                "name":result.store.name
            }
        }
    },status=status.HTTP_200_OK)
def get_all_categories(request):
    results = Category.objects.filter(seller=request.user)
    if len(results)==0:
        return Response(
            {
                "error":"Not Found Category"
            },status=status.HTTP_404_NOT_FOUND)
    return Response({
        "data":[
            {
                "id":result.id,
                "name":result.name,
                "seller":{
                    "id":result.seller.id,
                    "first_name":result.seller.first_name,
                    "last_name":result.seller.last_name
                },
                "store":{
                    "id":result.store.id ,
                    "name":result.store.name
                }

            } for result in results
        ]
    },status=status.HTTP_200_OK)

def post_category(request):
    data =request.data
    errors = validate_category(data,"CREATE")
    if len(errors)>0:
        return Response({
            "error":",".join(errors)
        },status=status.HTTP_400_BAD_REQUEST)
    store = Store.objects.get(id=data.get("store")["id"])
    if not store :
        return Response(
            {
                "error":"Not Found Store"
            },status=status.HTTP_404_NOT_FOUND)
    c = Category.objects.create(
        name=data.get("name"),
        store=store,
        seller=request.user
    )
    c.save()
    return Response({
        "data":{
            "id":c.id,
            "name":c.name,
            "store":{
                "id":c.store.id,
                "name":c.store.name
            },
            "seller":{
                "id":c.seller.id,
                "first_name":c.seller.first_name,
                "last_name":c.seller.last_name
            }
        }
    },status=status.HTTP_201_CREATED)

def put_category(request,id):
    data =request.data
    errors = validate_category(data,"UPDATE")
    if len(errors)>0:
        return Response({
            "error":",".join(errors)
        },status=status.HTTP_400_BAD_REQUEST)
    store = Store.objects.get(id=data.get("store")["id"])
    if not store :
        return Response(
            {
                "error":"Not Found Store"
            },status=status.HTTP_404_NOT_FOUND)
    try:
        result = Category.objects.get(id=id,seller=request.user)
    except Category.DoesNotExist:
        result = None

    if not result :
        return Response(
            {
                "error":"Not Found Category"
            },status=status.HTTP_404_NOT_FOUND)

    result.name=data.get("name")
    result.save()
    return Response({
        "data":{
            "id":result.id,
            "name":result.name,
            "store":{
                "id":result.store.id,
                "name":result.store.name
            },
            "seller":{
                "id":result.seller.id,
                "first_name":result.seller.first_name,
                "last_name":result.seller.last_name
            }
        }
    },status=status.HTTP_200_OK)
def get_by_id_product(request,id):
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
            "qty":result.qty
        }
    },status=status.HTTP_200_OK)

def get_all_product(request):
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
                "qty":result.qty
            } for result in results
        ]
    },status=status.HTTP_200_OK)
def delete_product(request,id):
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
def put_product(request,id):
    data = request.data
    errors = validate_product(data,"UPDATE")
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

def post_product(request):
    data = request.data
    errors = validate_product(data,"CREATE")
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

def method_not_allow(request):
    return Response(
        {
            "error":"Method Not Allow"
        },
        status=status.HTTP_405_METHOD_NOT_ALLOWED)

def validate_category(data,mode):
    errors = list()
    if mode == "CREATE":
        if(not data.get("store")) or (not data.get("store")["id"]):
            errors.append("Store is required")
    if(not data.get("name")) or data.get("name")=="":
        errors.append("Category Name is Required")

    return errors

def validate_product(data,mode):
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

