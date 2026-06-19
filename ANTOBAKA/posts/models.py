from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey(
        Group, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name='posts'  # ЭТО КЛЮЧЕВОЕ! Без этого нет связи
    )
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.text[:15]
    
    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'