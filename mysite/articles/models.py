from django.contrib.auth.models import User
from django.db import models


class Articles(models.Model):
    title = models.CharField('Название', max_length=255)
    content = models.TextField('Полный текст')
    photo = models.ImageField('Фото', upload_to='photos/%Y/%m/%d', blank=True)
    time_create = models.DateTimeField('Дата создания', auto_now_add=True)
    acceptance_stage = models.IntegerField("Стадии принятия", default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Потерянная вещь"
        verbose_name_plural = "Потерянные вещь"
        ordering = ['-time_create', 'title']


class Category(models.Model):
    title = models.CharField('Название категории', max_length=50)
    title_single = models.CharField('Название в ед. числе', max_length=50)
    slug = models.SlugField('URL')
    description = models.CharField("Описание", max_length=255)

    def __str__(self):
        return self.title_single

    def get_absolute_url(self):
        return self.slug

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"






