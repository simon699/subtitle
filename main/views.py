import json
import os
import threading
import queue
from typing import Dict
import re
import threading
from django.utils import timezone

import userresource.views
from userresource.views import *

from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from userresource.models import *
from main import getExternal
from main import subtitle
from main.models import *
from django.core.files.storage import FileSystemStorage
from login.forms import LoginForm
from django.views.decorators.csrf import csrf_exempt

# 定义一个全局事件
event = threading.Event()

# 创建一个队列用于线程间通信
result_queue = queue.Queue()


def get_index(request):
    if hasattr(request, 'user') and hasattr(request.user, 'userID'):
        userID = request.user.userID

        get_count = getResource.objects.filter(
            userID=userID
        ).aggregate(total_count=Sum('count'))
        exenp_cont = expendResource.objects.filter(
            userID=userID
        ).aggregate(total_count=Sum('count'))

        if exenp_cont['total_count'] == None:
            count = get_count['total_count']
        else:
            count = get_count['total_count'] - exenp_cont['total_count']

        return render(request, 'main.html',
                      {'session_cookie_age': settings.SESSION_COOKIE_AGE,
                       'user_resource': count})

    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form, 'name': 'login'})


@csrf_exempt  # 如果使用了 Django 的 CSRF 保护，需要确保在 AJAX 请求中发送 CSRF token
def get_matermark_subtitle(request):
    if hasattr(request, 'user') and hasattr(request.user, 'userID'):
        if request.method == "POST":
            uploaded_file = request.FILES['file']

            local_file_path = upload_to(request.user.userID, uploaded_file.name)
            if not os.path.exists('uploads/'):
                os.makedirs('uploads/', exist_ok=True)
            # 保存文件到本地
            with open(local_file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # 在这里进行其他处理，例如打印文件路径
            ext = local_file_path.split('/')[-1]
            objectName = f"cx-subtitle-resource/{ext}"

            thread = threading.Thread(target=get_resource_task, args=(request, objectName, local_file_path))
            thread.start()
            thread.join()

            request_data = result_queue.get()

            # print(request_data)

            # request_data = get_resource_task(request, objectName, local_file_path)

            # request_data = {'start': '200', 'data': '{"title": ["比赛终于结束了", "双方打成平局", "这就是足球的魅力", "永不言弃"], "showTitle": "足球之夜，再战无憾", "showDetail": "比赛的最后一刻，所有的努力与汗水都在这一瞬间定格，双方最终1-1平局，正是因为有不放弃的精神，才能成就这足球的精彩。"}'}
            # request_data = {'start': '100', 'error': '网络异常错误'}

            # request_data = {'data': '{\n  "from": "self-written",\n  "title": ["飞书", "让业务先进一步."],\n  "showTitle": "飞书，让业务先进一步。",\n  "showDetail": "一起进入未来，飞书让业务先进一步，迈向成功。"\n}', 'start': '200'}
            try:
                if request_data['start'] == '200':

                    # 提取并解析嵌套的 JSON 字符串
                    data_str = request_data['data']
                    parsed_data = json.loads(data_str)
                    textArr = (parsed_data['title'])
                    showTitle = parsed_data['showTitle']
                    showDetail = parsed_data['showDetail']
                    font = "Bitter-Regular.ttf"

                    sub_image = subtitle.ImageGetText(textArr, local_file_path, font)

                    matermark_image = subtitle.add_watermark(sub_image, font, "水印").convert("RGB")

                    matermark_name = local_file_path.split('/')[-1]
                    matermark_image_name = f'matermark_{matermark_name}'

                    # 构建输出文件的完整路径
                    if not os.path.exists('matermark_image/'):
                        os.makedirs('matermark_image/', exist_ok=True)

                    mater_output_path = os.path.join('matermark_image/', matermark_image_name)

                    # 构建输出文件的完整路径
                    if not os.path.exists('sub_image/'):
                        os.makedirs('sub_image/', exist_ok=True)

                    sub_name = local_file_path.split('/')[-1]
                    sub_image_name = f'sub_{sub_name}'
                    sub_output_path = os.path.join('sub_image/', sub_image_name)

                    # 保存文件到本地
                    matermark_image.save(mater_output_path, format="JPEG")
                    sub_image.save(sub_output_path, format='JPEG')

                    getExternal.put_image_oss(matermark_image_name,mater_output_path)
                    getExternal.put_image_oss(sub_image_name, sub_output_path)
                    data_change( request, f"{os.getenv('BUCKET_URL')}/{ext}", f"{os.getenv('BUCKET_URL')}/{matermark_image_name}",
                        f"{os.getenv('BUCKET_URL')}/{sub_image_name}", showTitle,
                        showDetail)

                    '''
                    thread1 = threading.Thread(target=getExternal.put_image_oss,
                                           args=(matermark_image_name, mater_output_path))
                    thread2 = threading.Thread(target=getExternal.put_image_oss,
                                           args=(sub_image_name, sub_output_path))
                    thread3 = threading.Thread(target=data_change, args=(
                        request, f"{os.getenv('BUCKET_URL')}/{ext}", f"{os.getenv('BUCKET_URL')}/{matermark_image_name}",
                        f"{os.getenv('BUCKET_URL')}/{sub_image_name}", showTitle,
                        showDetail))

                    thread1.start()
                    thread2.start()
                    thread3.start()
                    thread1.join()
                    thread2.join()
                    thread3.join()
                    '''

                    data = {
                        'matermark_image_path': f"{os.getenv('BUCKET_URL')}/{matermark_image_name}",
                        'showTitle': showTitle,
                        'showDetail': showDetail,
                    }

                    delete_image(local_file_path, mater_output_path, sub_output_path)

                    '''
                    # 新开线程，删除保存的本地文件
                    thread1 = threading.Thread(target=delete_image,
                                             args=(local_file_path, mater_output_path, sub_output_path))
                    thread1.start()
                    '''
                else:
                    data = {
                        "error": request_data,
                    }
            except Exception as e:
                print(e)

                data = {
                    "error": request_data,
                }

            return JsonResponse(data)


def get_resource_task(request, objectName, filePath):
    getExternal.put_image_oss(objectName, filePath)
    image_URL = f"{os.getenv('BUCKET_URL')}/{objectName}"
    result = getExternal.get_open_ai(image_URL)
    # 将结果放入队列中
    result_queue.put(result)


def split_string_by_punctuation(input_string):
    # 定义正则表达式模式，匹配 . 。 , ， 四种标点
    pattern = r'[.,。，]'

    # 使用 re.split() 按照指定的模式分割字符串
    segments = re.split(pattern, input_string)

    # 去除空字符串
    segments = [segment for segment in segments if segment]

    return segments


def delete_image(local_file_path, output_path, sub_output_path):
    try:
        # 删除保存的本地文件
        os.remove(local_file_path)
        os.remove(output_path)
        os.remove(sub_output_path)

    except Exception as e:
        print(e)


def data_change(request, imageURL, sub_mak_imageURL, sub_imageURL, subTitle, subDescription):

    sub_data = subtitle_data()
    sub_data.userID = request.user.userID
    sub_data.imageURL = imageURL
    sub_data.sub_mak_imageURL = sub_mak_imageURL
    sub_data.sub_imageURL = sub_imageURL
    sub_data.subTitle = subTitle
    sub_data.subDescription = subDescription
    sub_data.save()


@csrf_exempt  # 如果使用了 Django 的 CSRF 保护，需要确保在 AJAX 请求中发送 CSRF token
def get_subtitle(request):
    if hasattr(request, 'user') and hasattr(request.user, 'userID'):
        if request.method == "POST":
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            get_make_subtitle = body_data['get_make_subtitle']

            try:
                results = subtitle_data.objects.filter(sub_mak_imageURL=get_make_subtitle,
                                                       userID=request.user.userID).values('sub_imageURL')
                # 处理查询结果
                for result in results:
                    data = {
                        'data': result['sub_imageURL']
                    }

                return JsonResponse(data)
            except Exception as e:
                print(e)
                return JsonResponse({'data': None})

@csrf_exempt
def get_user_count(request):
    if hasattr(request, 'user') and hasattr(request.user, 'userID'):

        get_count = getResource.objects.filter(
            userID=request.user.userID
        ).aggregate(total_count=Sum('count'))
        exenp_cont = expendResource.objects.filter(
            userID=request.user.userID
        ).aggregate(total_count=Sum('count'))

        count = get_count['total_count'] - exenp_cont['total_count']

        return JsonResponse({'count': count})


def expend_user_count(request):
    if hasattr(request, 'user') and hasattr(request.user, 'userID'):
        userresource.views.expend_user_resource(request, userID=request.user.userID, expendType='1', count=1)

