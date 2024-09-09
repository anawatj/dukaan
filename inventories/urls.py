from django.urls import path
from inventories import views

urlpatterns=[
    path('products/',views.products),
    path('products/<int:id>/',views.product)
    #path('<int:id>/',views.store)
]