from rest_framework.response import Response
from rest_framework import status
from user.models import CustomUser

def register(request):
    data = request.data
    errors = validate(data,"CREATE")
    if len(errors) > 0 :
        return Response({
            "error":','.join(errors)
        },status=status.HTTP_400_BAD_REQUEST)
    u = CustomUser.objects.create(
        username=data.get('username'),
        email=data.get('email'),
        user_type = CustomUser.Types.CUSTOMER,
        mobile_number=data.get("mobile_number"),
        address=data.get("address"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        is_staff=False
    )
    u.set_password(data.get("password"))
    u.save()
    return Response(
        {"data":
            {
                "username":u.get_username(),
                "email":u.email,
                "mobile_number":u.mobile_number,
                "address":u.address,
                "first_name":u.first_name,
                "last_name":u.last_name}
        },
        status=status.HTTP_201_CREATED)
def get_by_id(request,id):
    try:
        result=CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        result=None

    if not result :
        return Response(
            {
                "error":"Not Found User"
            },status=status.HTTP_404_NOT_FOUND)

    return Response({
        "data":{
            "id":result.id,
            "username":result.get_username(),
            "user_type":result.user_type,
            "email":result.email,
            "mobile_number":result.mobile_number,
            "address":result.address,
            "first_name":result.first_name,
            "last_name":result.last_name}

    },status=status.HTTP_200_OK)
def put(request,id):
    data = request.data
    errors = validate(data,"UPDATE")
    if len(errors) > 0 :
        return Response({
            "error":','.join(errors)
        },status=status.HTTP_400_BAD_REQUEST)
    try:
        result=CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        result=None
    if not result :
        return Response(
            {
                "error":"Not Found User"
            },status=status.HTTP_404_NOT_FOUND)
    result.first_name = data.get("first_name")
    result.last_name= data.get("last_name")
    result.set_password(data.get("password"))
    result.address= data.get("address")
    result.mobile_number=data.get("mobile_number")
    result.save()
    return Response({
        "data":{
            "id":result.id,
            "username":result.username,
            "user_type":result.user_type,
            "email":result.email,
            "mobile_number":result.mobile_number,
            "address":result.address,
            "first_name":result.first_name,
            "last_name":result.last_name}
    },
        status=status.HTTP_200_OK)
def get_all(request):
    results = CustomUser.objects.all()
    if len(results)==0:
        return Response(
            {
                "error":"Not Found User"
            },status=status.HTTP_404_NOT_FOUND)
    return Response({
        "data":[
            {
                "id":result.id,
                "username":result.username,
                "user_type":result.user_type,
                "email":result.email,
                "mobile_number":result.mobile_number,
                "address":result.address,
                "first_name":result.first_name,
                "last_name":result.last_name
            } for result in results]
    },status=status.HTTP_200_OK)

def post(request):
    data = request.data
    errors = validate(data,"CREATE")
    if len(errors) > 0 :
        return Response({
            "error":','.join(errors)
        },status=status.HTTP_400_BAD_REQUEST)
    u = CustomUser.objects.create(
        username=data.get('username'),
        email=data.get('email'),
        user_type = CustomUser.Types.SELLER,
        mobile_number=data.get("mobile_number"),
        address=data.get("address"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        is_staff=False
    )
    u.set_password(data.get("password"))
    u.save()
    return Response({"data":{
        "id":u.id,
        "username":u.get_username(),
        "user_type":u.user_type,
        "email":u.email,
        "mobile_number":u.mobile_number,
        "address":u.address,
        "first_name":u.first_name,
        "last_name":u.last_name}
    },status=status.HTTP_201_CREATED)

def validate(data,mode):
    errors = list()
    if mode=="CREATE":
        if (not data.get("username") ) or data.get("username") == "":
            errors.append("Username is required")
        if (not data.get("email")) or data.get("email")=="":
            errors.append("Email is required")
        if (not data.get("mobile_number")) or data.get("mobile_number")=="":
            return errors.append("mobile_number")
    if (not data.get("password") ) or data.get("password")=="":
        errors.append("Password is required")
    if (not data.get("first_name")) or data.get("first_name")=="":
        return errors.append("First Name is required")
    if (not data.get("last_name")) or data.get("last_name")=="":
        return errors.append("Last Name is required")
    if (not data.get("address")) or data.get("address")=="":
        return errors.append("Address is required")
    return errors