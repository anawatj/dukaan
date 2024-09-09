from rest_framework.response import Response
from rest_framework import status
from user.models import CustomUser
from stores.models import Store
def post(request):
    data=request.data
    errors = validate(data,"CREATE")
    if len(errors) > 0 :
        return Response({
            "error":",".join(errors)
        },status=status.HTTP_400_BAD_REQUEST)
    s = Store.objects.create(
        name=data.get("name"),
        address=data.get("address"),
        seller=request.user
    )
    s.save()
    return Response({
        "data":{
            "id":s.id,
            "name":s.name,
            "address":s.address,
            "seller":{
                "id":s.seller.id,
                "first_name":s.seller.first_name,
                "last_name":s.seller.last_name
            }
        }
    },status=status.HTTP_201_CREATED)

def get_all(request):
    results = Store.objects.filter(seller=request.user)
    if len(results)==0:
        return Response(
            {
                "error":"Not Found Store"
            },status=status.HTTP_404_NOT_FOUND)
    return Response({
        "data":[{
            "id":result.id,
            "name":result.name,
            "address":result.address
        }for result in results]
    },status=status.HTTP_200_OK)

def get_by_id(request,id):
    try:
        result = Store.objects.get(id=id,seller=request.user)
    except Store.DoesNotExist:
        result= None
    if not result :
        return Response(
            {
                "error":"Not Found Store"
            },status=status.HTTP_404_NOT_FOUND)
    return Response({
        "data":{
            "id":result.id,
            "name":result.name,
            "address":result.address,
            "seller":{
                "id":result.seller.id,
                "first_name":result.seller.first_name,
                "last_name":result.seller.last_name
            }
        }
    },status=status.HTTP_200_OK)

def put(request,id):
    try:
        result = Store.objects.get(id=id,seller=request.user)
    except Store.DoesNotExist:
        result= None
    if not result :
        return Response(
            {
                "error":"Not Found Store"
            },status=status.HTTP_404_NOT_FOUND)
    data = request.data
    errors = validate(data,"UPDATE")
    if len(errors) > 0 :
        return Response({
            "error":",".join(errors)
        },status=status.HTTP_400_BAD_REQUEST)

    result.address=data.get("address")
    result.save()
    return Response({
        "data":{
            "id":result.id,
            "name":result.name,
            "address":result.address,
            "seller":{
                "id":result.seller.id,
                "first_name":result.seller.first_name,
                "last_name":result.seller.last_name
            }
        }
    },status=status.HTTP_200_OK)
def delete(request,id):
    try:
        result = Store.objects.get(id=id,seller=request.user)
    except Store.DoesNotExist:
        result= None
    if not result :
        return Response(
            {
                "error":"Not Found Store"
            },status=status.HTTP_404_NOT_FOUND)
    result.delete()
    return Response({
        "data":"Success"
    },
        status=status.HTTP_200_OK)



def validate(data,mode):
    errors = list()
    if mode=="CREATE":
        if (not data.get("name")) or data.get("name")=="":
            errors.append("Store name is required")
    if (not data.get("address")) or data.get("address")=="":
        errors.append("Address is required")
    return errors