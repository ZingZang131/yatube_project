from django.shortcuts import render
# api/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Post.
    Поддерживает все CRUD операции.
    """
    queryset = Post.objects.all().order_by('-pub_date')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def perform_create(self, serializer):
        # При создании поста автор автоматически берется из request.user
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        # Проверка: только автор может редактировать пост
        if serializer.instance.author != self.request.user:
            raise permissions.PermissionDenied('Изменение чужого контента запрещено!')
        serializer.save()
    
    def perform_destroy(self, instance):
        # Проверка: только автор может удалить пост
        if instance.author != self.request.user:
            raise permissions.PermissionDenied('Удаление чужого контента запрещено!')
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для модели Group.
    Только чтение (GET).
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Comment.
    Поддерживает все CRUD операции.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        # Получаем post_id из URL и возвращаем комментарии только этого поста
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        return Comment.objects.filter(post=post).order_by('created')
    
    def perform_create(self, serializer):
        # Получаем post_id из URL
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        # Создаем комментарий с автором из request.user и привязываем к посту
        serializer.save(author=self.request.user, post=post)
    
    def perform_update(self, serializer):
        # Проверка: только автор может редактировать комментарий
        if serializer.instance.author != self.request.user:
            raise permissions.PermissionDenied('Изменение чужого контента запрещено!')
        serializer.save()
    
    def perform_destroy(self, instance):
        # Проверка: только автор может удалить комментарий
        if instance.author != self.request.user:
            raise permissions.PermissionDenied('Удаление чужого контента запрещено!')
        instance.delete()
