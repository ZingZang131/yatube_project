from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    # Добавляем поле group (связь с группой)
    group = models.ForeignKey(
        'Group',  # Ссылка на модель Group
        on_delete=models.CASCADE,  # При удалении группы удаляются все посты группы
        blank=True,  # Может быть пустым
        null=True    # Разрешено NULL в БД
    )


class Group(models.Model):
    title = models.CharField(max_length=200)  # Название группы
    slug = models.SlugField(unique=True)      # Уникальный адрес для URL
    description = models.TextField()          # Описание группы

    def __str__(self):
        return self.title  # При печати будет выводиться название группы
