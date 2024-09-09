from rest_framework.permissions import BasePermission

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        print("user_type",request.user.user_type)
        return request.user.user_type=="SELLER"

class IsCustomer(BasePermission):
    def has_permission(self,request,view):
        print("user_type",request.user.user_type)
        return request.user.user_type=="CUSTOMER"