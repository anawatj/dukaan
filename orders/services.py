from rest_framework.response import Response
from rest_framework import status

from inventories.models import Product
from orders.models import Order,OrderItem
def create(request):
    data = request.data
    errors = validate(data)
    if len(errors) > 0 :
        return Response({
            "error":','.join(errors)
        },status=status.HTTP_400_BAD_REQUEST)
    result = Order.objects.create(
        mobile_number=  data.get("cart")["mobile_number"],
        first_name = data.get("cart")["first_name"],
        last_name = data.get("cart")["last_name"],
        address = data.get("address"),
        payment_method=data.get("payment_method"),
        credit_card_number=data.get("credit_card_number"),
        credit_card_holder=data.get("credit_card_holder"),
        order_status=Order.OrderStatus.DRAFTED
    )
    result.save()
    items = data.get("cart")["cartItems"]
    for item in items:
        product = Product.objects.filter(id=item["product"]["id"]).first()
        order_item=OrderItem.objects.create(
            order_id=result.id ,
            product_id=product.id,
            qty=item["qty"]
        )
        order_item.save()
    order_items = OrderItem.objects.filter(order__id=result.id)
    return Response({
        "data":{
            "id":result.id,
            "mobile_number":result.mobile_number,
            "address":result.address,
            "first_name":result.first_name,
            "last_name":result.last_name,
            "payment_method":result.payment_method,
            "credit_card_number":result.credit_card_number,
            "credit_card_holder":result.credit_card_holder,
            "orderItems":[
                {
                    "product":[
                        {
                            "id":order_item.product_id,
                            "name":order_item.product.name
                        }
                    ],
                    "qty": order_item.qty

                } for order_item in order_items
            ]
        }
    },
        status=status.HTTP_201_CREATED)

def get_all(request):
    results = Order.objects.all()
    if len(results)==0:
        return Response(
            {
                "error":"Not Found User"
            },status=status.HTTP_404_NOT_FOUND)
    return Response({
        "data":[
            {
                "id":result.id,
                "mobile_number":result.mobile_number,
                "address":result.address,
                "first_name":result.first_name,
                "last_name":result.last_name,
                "payment_method":result.payment_method,
                "credit_card_number":result.credit_card_number,
                "credit_card_holder":result.credit_card_holder
            } for result in results]
    },status=status.HTTP_200_OK)

def put(request,id):
    try:
        result = Order.objects.get(id=id)
    except Order.DoesNotExist:
        result = None
    if not result :
        return Response(
            {
                "error":"Not Found Order"
            },status=status.HTTP_404_NOT_FOUND)


    if not result.order_status==Order.OrderStatus.DRAFTED :
        return Response(
            {
                "error":"This order is issued"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    result.order_status=Order.OrderStatus.CREATED
    result.save()

    return Response({
        "data":{
            "id":result.id,
            "order_status":result.order_status
        }
    },
        status=status.HTTP_200_OK)

def patch(request,id):
    try:
        result = Order.objects.get(id=id)
    except Order.DoesNotExist:
        result = None
    if not result :
        return Response(
            {
                "error":"Not Found Order"
            },status=status.HTTP_404_NOT_FOUND)
    data = request.data
    print(result.order_status)
    if not  result.order_status == Order.OrderStatus.CREATED :
        return Response(
            {
                "error":"This order is issued"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    result.order_status=Order.OrderStatus.SUCCESS
    result.save()
    order_items = OrderItem.objects.filter(order__id=result.id)
    if result.order_status==Order.OrderStatus.SUCCESS:
        for order_item in order_items:
            product = Product.objects.get(id=order_item.product_id)
            if product and order_item.can_order():
                product.qty=product.qty-order_item.qty
                product.save()

    return Response({
        "data":{
            "id":result.id,
            "order_status":result.order_status
        }
    },
        status=status.HTTP_200_OK)

def get_by_id(request,id):
    try:
        result = Order.objects.get(id=id)
    except Order.DoesNotExist:
        result = None
    if not result :
        return Response(
            {
                "error":"Not Found Order"
            },status=status.HTTP_404_NOT_FOUND)
    order_items = OrderItem.objects.filter(order__id=id)
    return Response({
        "data":{
            "id":result.id,
            "mobile_number":result.mobile_number,
            "address":result.address,
            "first_name":result.first_name,
            "last_name":result.last_name,
            "payment_method":result.payment_method,
            "credit_card_number":result.credit_card_number,
            "credit_card_holder":result.credit_card_holder,
            "order_status":result.order_status,
            "orderItems":[
                {
                    "product":[
                        {
                            "id":order_item.product_id,
                            "name":order_item.product.name
                        }
                    ],
                    "qty": order_item.qty

                } for order_item in order_items
            ]
        }
    },
        status=status.HTTP_200_OK)

def delete(request,id):
    try:
        result = Order.objects.get(id=id)
    except Order.DoesNotExist:
        result = None
    if not result :
        return Response(
            {
                "error":"Not Found Order"
            },status=status.HTTP_404_NOT_FOUND)
    OrderItem.objects.filter(order__id=id).delete()
    result.delete()
    return Response({
        "data":"Success"
    },status=status.HTTP_200_OK)

def validate(data):
    errors = list()
    if (not data.get("cart")["mobile_number"]) or data.get("cart")["mobile_number"] == "" :
        errors.append("mobile number is required")
    if (not data.get("cart")["first_name"]) or data.get("cart")["first_name"]=="":
        errors.append("first name is required")
    if (not data.get("cart")["last_name"]) or data.get("cart")["last_name"]== "":
        errors.append("last name is required")
    if (not data.get("address")) or data.get("address")=="":
        errors.append("address is required")
    if (not data.get("payment_method")) or data.get("payment_method")=="":
        errors.append("payment method is required")
    if (not data.get("credit_card_number")) or data.get("credit_card_number")=="":
        errors.append("credit card number is required")
    if (not data.get("credit_card_holder")) or data.get("credit_card_holder")=="":
        errors.append("credit card holder is required")
    return errors