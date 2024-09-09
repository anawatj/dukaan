from django.urls import path
from stores import views

urlpatterns=[
    path('',views.stores),
    path('<int:id>/',views.store)
]