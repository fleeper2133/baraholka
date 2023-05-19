from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    message = models.CharField('Сообщение', max_length=255, blank=True)
    photo = models.ImageField('Фото', blank=True, upload_to='photos/%Y/%m/%d')
    time_create = models.DateTimeField('Дата создания', auto_now_add=True)
    sender = models.ForeignKey(User, verbose_name="Отправитель", on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(User, verbose_name="Получатель", on_delete=models.CASCADE, related_name="recipient")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['time_create']

    def __str__(self):
        return self.message
