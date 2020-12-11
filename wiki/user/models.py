from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30, verbose_name="用户名", unique=True)
    password = models.CharField(max_length=32, verbose_name="密码")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_active = models.BooleanField(default=True, verbose_name="是否活跃")

    class Meta:
        verbose_name = "用户名"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
