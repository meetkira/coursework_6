from django.conf import settings
from django.db import models

from users.models import User


class Ad(models.Model):
    title = models.CharField(max_length=100, null=False)
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=1000, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=1000, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.text
