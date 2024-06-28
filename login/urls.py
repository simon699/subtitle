from django.urls import path
from login import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.sign_view, name='signup'),
    path('loginout/',views.logout_user,name='login_out'),
    path('api/sign/', views.sign_user, name='sign_user'),
    path('api/login/', views.login_user, name='login_user'),
    path('api/checkuser/',views.check_user,name='check_user'),
    path('api/user_info/',views.user_info,name='user_info'),

]