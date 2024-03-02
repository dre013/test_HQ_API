from django.db import models
from django.contrib.auth.models import User


class Products(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Создатель продукта")
    name = models.CharField(max_length=255, unique=True, verbose_name="Имя продукта")
    start_date = models.DateTimeField(verbose_name="Дата старта")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    min_users = models.PositiveIntegerField(default=0, verbose_name="Мин. кол-во пользователей")
    max_users = models.PositiveIntegerField(default=0, verbose_name="Макс. кол-во пользователей")

    class Meta:
        db_table = "Product"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
    
    def __str__(self):
        return self.name

class Lessons(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Название урока")
    product = models.ForeignKey(Products, related_name="lessons", on_delete=models.CASCADE, verbose_name="Продукт")
    video_link = models.URLField(verbose_name="Ссылка на видео")

    class Meta:
        db_table = "Lesson"
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
    
    def __str__(self):
        return self.title
    

class Users(models.Model):
    CHOICES = [
        ('Student', 'Студент'),
        ('Client', 'Клиент'),
        ('Teacher', 'Учитель'),
        ('Author', 'Автор')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    type_user = models.CharField(max_length=255, choices=CHOICES, verbose_name="Тип пользователя")
    products = models.ManyToManyField(Products, blank=True, verbose_name="Продукты")

    class Meta:
        db_table = "User"
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"
    
    def __str__(self) -> str:
        return self.user.username


class Groups_members(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя группы")
    user = models.ManyToManyField(User, blank=True, verbose_name="Пользователь")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, default='', verbose_name="Продукт")

    class Meta:
        db_table = "Group"
        verbose_name = "Группу"
        verbose_name_plural = "Группы"
    
    def __str__(self):
        return self.name

