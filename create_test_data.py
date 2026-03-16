import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ANTOBAKA.settings')
django.setup()

from posts.models import Post, Group
from django.contrib.auth import get_user_model

User = get_user_model()

# Создаем пользователя Толстого
user, created = User.objects.get_or_create(
    username='tolstoy',
    defaults={
        'first_name': 'Лев',
        'last_name': 'Толстой',
        'email': 'tolstoy@example.com'
    }
)

if created:
    user.set_password('password123')
    user.save()
    print('✅ Создан пользователь: Лев Толстой')

# Удаляем старые группы (чтобы избежать конфликтов)
Group.objects.all().delete()
print('🗑️ Старые группы удалены')

# Создаем группы
group1 = Group.objects.create(
    slug='war-and-peace',
    title='Война и мир',
    description='Обсуждение романа-эпопеи'
)
print('✅ Создана группа: Война и мир')

group2 = Group.objects.create(
    slug='anna-karenina',
    title='Анна Каренина',
    description='Все об Анне Карениной'
)
print('✅ Создана группа: Анна Каренина')

# Создаем посты
posts_data = [
    {
        'text': '3-го июля. Встал в 10, но умылся, оделся, пил кофей, читал письма — все пустые. Писал до 3-х часов. Потом пошел гулять; на дворе жарко, пыльно. Дома застал Горемыкина, который приехал звать меня к себе обедать. Отказался.',
        'pub_date': datetime(1854, 7, 3, 10, 0),
        'group': group1
    },
    {
        'text': '5-го июля. Целый день писал, но немного. Вечером был у Горчакова. Он очень любезен, но я чувствую, что ему со мной скучно. И мне с ним тоже. Зачем эти светские отношения?',
        'pub_date': datetime(1854, 7, 5, 15, 30),
        'group': group1
    },
    {
        'text': '8-го июля. Читал "Histoire de la civilisation en France". Удивительно, как много мы не знаем. Надо больше читать. Вечером играл в шахматы с Волконским - выиграл две партии.',
        'pub_date': datetime(1854, 7, 8, 20, 0),
        'group': group1
    },
    {
        'text': '10-го июля. Получил письмо от брата Николая. Он в горах Кавказа и пишет, что там удивительно хорошо. Завидую ему. Здесь же духота и скука.',
        'pub_date': datetime(1854, 7, 10, 9, 15),
        'group': group1
    },
    {
        'text': '12-го июля. Начал писать новую повесть. Если будет время, может выйти что-то путное. Вечером был у княгини - опять этот пустой светский разговор.',
        'pub_date': datetime(1854, 7, 12, 23, 0),
        'group': group1
    },
    {
        'text': '15-го июля. Сегодня целый день работал - исписал 10 листов. Кажется, получается. Надо больше работать, меньше думать о пустяках.',
        'pub_date': datetime(1854, 7, 15, 8, 0),
        'group': group2
    },
    {
        'text': '18-го июля. Обедал у Муравьева. Много говорили о войне. Все ждут чего-то, а я не жду - просто хочу писать. Вечером читал Руссо.',
        'pub_date': datetime(1854, 7, 18, 19, 30),
        'group': group2
    },
    {
        'text': '20-го июля. Вчера не писал - был болен. Сегодня лучше. Прочел статью о моем последнем рассказе. Хвалят, но я знаю, что можно лучше.',
        'pub_date': datetime(1854, 7, 20, 14, 0),
        'group': group2
    },
    {
        'text': '22-го июля. Ездил в Ясную Поляну. Как хорошо в деревне! Воздух, тишина. Думал о том, чтобы поселиться здесь и писать, писать, писать...',
        'pub_date': datetime(1854, 7, 22, 12, 0),
        'group': group2
    },
    {
        'text': '25-го июля. Опять в Москве. Тоска. Читал корректуру. Ошибок много - надо быть внимательнее. Вечером заходил Аксаков, говорили о славянах.',
        'pub_date': datetime(1854, 7, 25, 22, 0),
        'group': group2
    },
]

# Создаем посты
for post_data in posts_data:
    post = Post.objects.create(
        text=post_data['text'],
        pub_date=post_data['pub_date'],
        author=user,
        group=post_data['group']
    )
    print(f'✅ Создан пост от {post_data["pub_date"].strftime("%d.%m.%Y")}')

print('\n' + '='*40)
print('🎉 ГОТОВО! Тестовые данные загружены')
print('='*40)
print(f'📊 Всего постов: {Post.objects.count()}')
print(f'📊 Групп: {Group.objects.count()}')
print(f'📊 Пользователей: {User.objects.count()}')
print('='*40)