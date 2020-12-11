from django.db import models
from user.models import User


# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_active = models.BooleanField(default=True, verbose_name="是否活跃")
    user = models.ForeignKey(User, verbose_name="编辑者")

    class Meta:
        verbose_name = "云笔记"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
