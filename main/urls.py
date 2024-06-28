from django.urls import path
from main import views

urlpatterns = [
    path('mainView/', views.get_index, name='mainView'),
    path('mainView/api/get_matermark_subtitle/',views.get_matermark_subtitle,name='get_matermark_subtitle'),
    path('mainView/api/get_subtitle/',views.get_subtitle,name='get_subtitle'),
    path('mainView/api/get_user_count/',views.get_user_count,name='get_user_count'),
    path('mainView/api/expend_user_count/',views.expend_user_count,name='expend_user_count'),
]