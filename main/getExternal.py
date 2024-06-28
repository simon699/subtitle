import os
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from dotenv import load_dotenv
import requests
import json



# 加载 .env 文件中的环境变量
load_dotenv()

def put_image_oss(objectName,localFile):

    auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
    # 填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
    # yourBucketName填写存储空间名称。
    bucket = oss2.Bucket(auth,os.getenv('ENDPOINT'),os.getenv('OSS_BUCKET_NAME'))

    # 上传文件到OSS。
    # yourObjectName由包含文件后缀，不包含Bucket名称组成的Object完整路径，例如abc/efg/123.jpg。
    # yourLocalFile由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
    bucket.put_object_from_file(objectName, localFile)



def get_open_ai(file_path):
    url = os.getenv('OPEN_AI_URL')
    payload = json.dumps({
        "model":"gpt-4o",
        "messages":[{
            "role": "system",
            "content": [{"type": "text",
                    "text": """You are a movie database with a lot of movie quotes. You can also analyze the photos 
                    provided by users and return movie quotes that are suitable for the pictures and moods based on 
                    the photos uploaded by users. If there are no suitable movie quotes, you can create them yourself 
                    and provide titles and texts for social media sharing. Return in format as follows： {
                    "from":"Source, from the movie returns the movie name, self-written, means written by oneself",
                    "title": Divide into segments according to commas and periods to form an array；"showTitle"：Social 
                    media sharing title；"showDetail"：Share content on social media}"""}
            ]},
            {
                "role": "user",
                "content": [{"type": "image_url",
                    "image_url": {
                    "url": file_path
                    }
                 }]
            }]
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {os.getenv('OPEN_AI_KEY')}"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    responseJson = json.loads(response.text)
    try:
        data = responseJson["choices"][0]["message"]["content"]
        return {"start":"200", "data":data}
    except Exception as e:
        return {"start":100,"data":responseJson}


