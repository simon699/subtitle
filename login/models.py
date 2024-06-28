from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.core.validators import EmailValidator


class UserInfoManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """创建并返回一个普通用户（带有用户名和密码）。"""
        if not username:
            raise ValueError('用户名必须填写')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """创建并返回一个超级用户（带有用户名和密码）。"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class UserInfo(AbstractBaseUser, PermissionsMixin):
    """用户信息模型。"""
    id = models.AutoField(primary_key=True, verbose_name="ID")
    username = models.CharField(verbose_name="用户名", max_length=20, unique=True)
    userID = models.CharField(verbose_name="用户编号", max_length=20, unique=True)
    password = models.CharField(verbose_name="密码", max_length=100)
    phone = models.CharField(verbose_name="手机号", max_length=20)
    email = models.EmailField(verbose_name="电子邮箱", max_length=50, validators=[EmailValidator])
    createDate = models.DateTimeField(verbose_name="注册时间", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="最后登录时间", null=True)
    isFirstPW = models.BooleanField(verbose_name="是否初始密码", default=True)
    uuid = models.CharField(verbose_name="设备信息", max_length=100)

    FROM_TYPE_CHOICES = [
        (1, 'web官网'),
        (2, '类型2'),
        (3, '类型3'),
    ]
    fromType = models.IntegerField(verbose_name="来自信息", choices=FROM_TYPE_CHOICES)
    fromTypeTitle = models.CharField(verbose_name="来自信息详情", max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='userinfo_groups',  # 添加 related_name 参数以避免冲突
        blank=True,
        help_text='用户所属的组。',
        related_query_name='userinfo'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='userinfo_user_permissions',  # 添加 related_name 参数以避免冲突
        blank=True,
        help_text='用户的特定权限。',
        related_query_name='userinfo'
    )

    objects = UserInfoManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'tb_user_info'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['userID']),
        ]