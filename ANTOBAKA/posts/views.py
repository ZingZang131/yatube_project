# posts/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Group
from .serializers import PostSerializer

# ==================== HTML VIEWS ====================

def index(request):
    post_list = Post.objects.order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by('-pub_date')
    
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def groups_all(request):
    groups = Group.objects.all()
    context = {
        'groups': groups,
    }
    return render(request, 'posts/groups_all.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author).order_by('-pub_date')
    post_count = post_list.count()
    
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'author': author,
        'page_obj': page_obj,
        'post_count': post_count,
    }
    return render(request, 'posts/profile.html', context)


# ==================== API VIEWS ====================

@api_view(['GET', 'POST'])
def api_posts(request):
    """
    API эндпоинт для работы со списком постов.
    
    GET: возвращает список всех постов в формате JSON
    POST: создает новый пост на основе переданных данных
    """
    if request.method == 'GET':
        # Получаем все посты, сортируем по дате публикации
        posts = Post.objects.all().order_by('-pub_date')
        # Сериализуем queryset в JSON
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Создаем сериализатор с данными из запроса
        serializer = PostSerializer(data=request.data)
        # Проверяем валидность данных
        if serializer.is_valid():
            # Сохраняем новый пост
            # Если автор не указан, но пользователь авторизован - используем его
            if 'author' not in request.data and request.user.is_authenticated:
                serializer.save(author=request.user)
            else:
                serializer.save()
            # Возвращаем созданный объект с кодом 201
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Если данные невалидны - возвращаем ошибки
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_posts_detail(request, pk):
    """
    API эндпоинт для работы с отдельным постом.
    
    GET: возвращает пост по id
    PUT: полностью обновляет пост
    PATCH: частично обновляет пост
    DELETE: удаляет пост
    """
    # Пытаемся найти пост по id
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        # Если пост не найден - возвращаем ошибку 404
        return Response(
            {'error': 'Пост не найден'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        # Сериализуем и возвращаем пост
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        # Для PATCH обновляем частично
        partial = request.method == 'PATCH'
        # Передаем существующий пост и новые данные
        serializer = PostSerializer(post, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Удаляем пост
        post.delete()
        # Возвращаем статус 204 (успешно удалено, без содержимого)
        return Response(status=status.HTTP_204_NO_CONTENT)