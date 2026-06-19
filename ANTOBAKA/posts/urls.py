from django.urls import path
from . import views

app_name = 'posts'  # <-- ВЕРНУТЬ app_name

urlpatterns = [
    # HTML маршруты
    path('', views.index, name='index'),
    path('groups/', views.groups_all, name='groups_all'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('profile/<str:username>/', views.profile, name='profile'), 
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    
    # API маршруты
    path('api/v1/posts/', views.api_posts, name='api_posts'),
    path('api/v1/posts/<int:pk>/', views.api_posts_detail, name='api_posts_detail'),
]