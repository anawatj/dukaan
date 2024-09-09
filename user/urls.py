from django.urls import path
from user import views

urlpatterns=[
    path('register/',views.register),
    path('',views.users),
    path('<int:id>/',views.user)
]