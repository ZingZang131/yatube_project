# posts/serializers.py
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.
    Преобразует объекты Post в JSON и обратно.
    """
    
    # Добавляем поле с именем автора для удобства (только для чтения)
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Post
        # Явно перечисляем поля, которые будут в JSON ответе
        # Исключаем id, так как в задании сказано его не обрабатывать
        fields = ('text', 'author', 'author_name', 'pub_date')
        # Поле pub_date только для чтения (устанавливается автоматически)
        read_only_fields = ('pub_date',)