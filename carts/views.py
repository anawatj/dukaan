from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from carts import services

@api_view(["POST"])
@permission_classes([AllowAny])
def carts(request):
    if request.method == "POST":
        return services.add_cart(request)
    else:
        return method_not_allow(request)
def method_not_allow(request):
    return Response(
        {
            "error":"Method Not Allow"
        },
        status=status.HTTP_405_METHOD_NOT_ALLOWED)






