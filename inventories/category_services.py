from rest_framework.response import Response
from rest_framework import status
from decimal import *
from stores.models import Store
from inventories.models import Category
def get_by_id(request,id):
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
def get_all(request):
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

def post(request):
    data =request.data
    errors = validate(data,"CREATE")
    if len(errors)>0:
        return Response({
            "error":",".join(errors)
        },status=status.HTTP_400_BAD_REQUEST)

    try:
        store = Store.objects.get(id=data.get("store")["id"])
    except Store.DoesNotExist:
        store=None
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

def put(request,id):
    data =request.data
    errors = validate(data,"UPDATE")
    if len(errors)>0:
        return Response({
            "error":",".join(errors)
        },status=status.HTTP_400_BAD_REQUEST)
    try:
        store = Store.objects.get(id=data.get("store")["id"])
    except Store.DoesNotExist:
        store=None
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


def validate(data,mode):
    errors = list()
    if mode == "CREATE":
        if(not data.get("store")) or (not data.get("store")["id"]):
            errors.append("Store is required")
    if(not data.get("name")) or data.get("name")=="":
        errors.append("Category Name is Required")

    return errors