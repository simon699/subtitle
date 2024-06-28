from django.db import models
import os
from datetime import datetime

def upload_to(userID, filename):
    # 获取文件扩展名
    ext = filename.split('.')[-1]
    # 自定义文件名格式，例如：user_<user_id>_<timestamp>.<ext>
    timestamp = int(datetime.now().timestamp())
    filename = f"user_{userID}_{timestamp}.{ext}"
    # 返回新的文件路径和文件名
    return os.path.join('uploads/', filename)

class subtitle_data(models.Model):
    userID = models.CharField(max_length=100,verbose_name="用户ID")
    imageURL = models.CharField(max_length=100,verbose_name="上传图片地址")
    sub_mak_imageURL = models.CharField(max_length=100,verbose_name="带水印的拼接地址")
    sub_imageURL = models.CharField(max_length=100,verbose_name="无水印的拼接地址")
    subTitle = models.CharField(max_length=200,verbose_name="标题")
    subDescription = models.CharField(max_length=200,verbose_name="描述")

    USERNAME_FIELD = 'userID'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.userID

    class Meta:
        db_table = 'subtitle_data'
        verbose_name = '字幕图片数据'
        verbose_name_plural = verbose_name