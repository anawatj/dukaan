from django.urls import path
from orders import views

urlpatterns=[
    path('create/',views.create_order),
    path('',views.orders),
    path('<int:id>/',views.order)
]