import json
import os
from django.utils import timezone
import userresource.views
from login.models import UserInfo
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
# views.py
from django.shortcuts import redirect
from .forms import UserRegistrationForm
from .forms import LoginForm
from django.db import connection
from dotenv import load_dotenv

from django.contrib.auth.decorators import login_required
import random
import string
from django.shortcuts import render, redirect
from userresource.views import *
from userresource.models import getResource


load_dotenv()

def logout_user(request):
    logout(request)
    myform = LoginForm()
    return render(request, 'login.html', {'form_obj': myform, 'name': 'login'})


def login_view(request):
    myform = LoginForm()
    return render(request, 'login.html', {'form_obj': myform, 'name': 'login'})


def sign_view(request):
    myform = UserRegistrationForm()
    return render(request, 'login.html', {'form_obj': myform, 'name': 'sign'})


def sign_user(request):
    if request.method == 'POST':

        sign_form = UserRegistrationForm(request.POST)
        login_form = LoginForm(request.POST)

        if sign_form.is_valid():
            user = sign_form.save(commit=False)
            user.username = sign_form.cleaned_data['sign_username']
            ps = sign_form.cleaned_data['sign_password']
            user.set_password(ps)
            user.fromType = 1
            user.email = sign_form.cleaned_data['sign_email']
            user.fromTypeTitle = "web-官网"
            user.is_active = True
            user.isFirstPW = False
            user.last_login = timezone.localtime(timezone.now())
            user.userID = generate_user_id()
            user.save()
            userresource.views.get_user_resources(request, userID=user.userID, getType='1', getTitle='注册获得',
                                                      count=5, getTime=timezone.now())

            return render(request, 'login.html',
                          {'form_obj': login_form, 'message': '注册成功，请登录', 'name': 'login'})
        else:
            return render(request, 'login.html',
                         {'form_obj': sign_form, 'message': '发生意外，请重试', 'name': 'sign'})


def login_user(request):
    if request.method == 'POST':
        myform = LoginForm(request.POST)
        try:
            if myform.is_valid():
                username = myform.cleaned_data['login_username']
                password = myform.cleaned_data['login_password']
                get_user = authenticate(request, username=username, password=password)

                if get_user is not None:
                    if get_user.is_active:
                        get_user.last_login = timezone.localtime(timezone.now())
                        get_user.save()
                        request.session['login_time'] = timezone.localtime(timezone.now()).isoformat()
                        login(request, get_user)
                        if os.getenv('DAY_GET_RESOURCE'):
                            day_giveaway_user_response(request, get_user.userID)
                        return redirect('mainView')
                    else:
                        return render(request, 'login.html',
                                        {'form_obj': myform, 'message': 'The account is disabled', 'name': 'login'})
                else:
                    return render(request, 'login.html',
                                  {'form_obj': myform, 'message': 'wrong user name or password', 'name': 'login'})
        except Exception as e:
            return render(request, 'login.html',
                          {'form_obj': myform, 'message': 'wrong user name or password', 'name': 'login'})
        else:
            return render(request, 'login.html',
                          {'form_obj': myform, 'message': 'wrong user name or password', 'name': 'login'})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form, 'name': 'login'})


def check_user(request):
    username = request.GET.get('username')
    exists = UserInfo.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})


def generate_user_id():

    existing_ids = UserInfo.objects.values_list('userID', flat=True)

    prefix = 'cx_'
    length = 10
    suffix_length = length - len(prefix)

    while True:
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=suffix_length))
        user_id = prefix + suffix
        if user_id not in existing_ids:
            return user_id


@login_required
def user_info(request):
    user = request.user
    data = {
        'username': user.username,
    }
    return JsonResponse(data)


def day_giveaway_user_response(request, userID):
    # 查询该用户当天是否有赠送过
    today = timezone.now().date()

    sql = '''
            select * from subtitle_db.sub_getResource where DATE(getDate)= %s
            and getType = 2 and userID = %s;
            '''

    count = getResource.objects.raw(sql, (today, userID))

    if len(count) == 0:
        userresource.views.get_user_resources(request, userID=userID, getType='2', getTitle='每日赠送', count=3,
                                                  getTime=timezone.localtime(timezone.now()))

