from django.db import models


class getResource(models.Model):
    userID = models.CharField(max_length=100,verbose_name="用户ID")
    getType = models.IntegerField(verbose_name="获取方式")
    getTitle = models.CharField(max_length=200,verbose_name="获取方式描述")
    count = models.IntegerField(verbose_name="消耗数量")
    getDate = models.DateTimeField(verbose_name="获取时间",auto_now_add=True)

    def __str__(self):
        return self.userID

    class Meta:
        db_table = 'sub_getResource'
        verbose_name = '字幕应用用户获得点数记录'
        verbose_name_plural = verbose_name


class expendResource(models.Model):
    userID = models.CharField(max_length=100, verbose_name="用户ID")
    expendType = models.IntegerField(verbose_name="消耗方式")
    count = models.IntegerField(verbose_name="消耗数量")
    expendDate = models.DateTimeField(verbose_name="消耗时间", auto_now_add=True)


    def __str__(self):
        return self.userID

    class Meta:
        db_table = 'sub_expendResource'
        verbose_name = '字幕应用用户消耗点数记录'
        verbose_name_plural = verbose_name