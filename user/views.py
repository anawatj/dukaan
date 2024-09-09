from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status
from user import services
from user.models import CustomUser
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    if request.method=="POST":
        return services.register(request)
    else:
        return method_not_allow(request)

@api_view(["GET","POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated,IsAdminUser])
def users(request):
    if request.method=="GET":
        return services.get_all(request)
    elif request.method=="POST":
        return services.post(request)
    else:
        return method_not_allow(request)

@api_view(["GET","PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated,IsAdminUser])
def user(request,id):
    if request.method=="GET":
        return services.get_by_id(request,id)
    elif request.method=="PUT":
        return services.put(request,id)
    else:
        return services.method_not_allow(request)


def method_not_allow(request):
    return Response(
        {
            "error":"Method Not Allow"
        },
        status=status.HTTP_405_METHOD_NOT_ALLOWED)