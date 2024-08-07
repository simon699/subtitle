# Generated by Django 5.1a1 on 2024-06-26 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='expendResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.CharField(max_length=100, verbose_name='用户ID')),
                ('expendType', models.IntegerField(verbose_name='消耗方式')),
                ('count', models.IntegerField(verbose_name='消耗数量')),
                ('expendDate', models.DateTimeField(auto_now_add=True, verbose_name='消耗时间')),
            ],
            options={
                'verbose_name': '字幕应用用户消耗点数记录',
                'verbose_name_plural': '字幕应用用户消耗点数记录',
                'db_table': 'sub_expendResource',
            },
        ),
        migrations.CreateModel(
            name='getResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.CharField(max_length=100, verbose_name='用户ID')),
                ('getType', models.IntegerField(verbose_name='获取方式')),
                ('getTitle', models.CharField(max_length=200, verbose_name='获取方式描述')),
                ('count', models.IntegerField(verbose_name='消耗数量')),
                ('getDate', models.DateTimeField(auto_now_add=True, verbose_name='获取时间')),
            ],
            options={
                'verbose_name': '字幕应用用户获得点数记录',
                'verbose_name_plural': '字幕应用用户获得点数记录',
                'db_table': 'sub_getResource',
            },
        ),
    ]
