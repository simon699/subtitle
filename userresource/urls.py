from django.urls import path
from userresource import views

urlpatterns = [
    path('',views.index),
]