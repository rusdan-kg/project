from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Катерогии'

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)  # связывание с вышестоящим КЛАССом
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    price = models.FloatField(verbose_name='Цена')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    size = models.TextField(null=True, verbose_name='Объем')
    date_end = models.DateField(verbose_name='Срок годности')

    def __str__(self):  # срабатывает когда вызываем объект
        return self.title

class ConfirmCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.code

