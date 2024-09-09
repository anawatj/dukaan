from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from user.permissions import IsSeller

from inventories import product_services
from inventories import category_services

# Create your views here.
@api_view(["GET","POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated,IsSeller])
def products(request):
    if request.method == "GET":
        return product_services.get_all(request)
    elif request.method=="POST":
        return product_services.post(request)
    else:
        return method_not_allow(request)

@api_view(["GET","PUT","DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated,IsSeller])
def product(request,id):
    if request.method=="GET":
        return product_services.get_by_id(request,id)
    elif request.method=="PUT":
        return product_services.put(request,id)
    elif request.method=="DELETE":
        return product_services.delete(request,id)
    else:
        return method_not_allow(request)



@api_view(["GET","POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated,IsSeller])
def categories(request):
    if request.method=="GET":
        return category_services.get_all(request)
    elif request.method=="POST":
        return category_services.post(request)
    else:
        return method_not_allow(request)

@api_view(["GET","PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated,IsSeller])
def category(request,id):
    if request.method=="GET":
        return category_services.get_by_id(request,id)
    elif request.method=="PUT":
        return category_services.put(request,id)
    else:
        return method_not_allow(request)


def method_not_allow(request):
    return Response(
        {
            "error":"Method Not Allow"
        },
        status=status.HTTP_405_METHOD_NOT_ALLOWED)




