from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', verbose_name='Пользователь',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    id = models.AutoField(primary_key=True)
    feeds = models.ManyToManyField(User, verbose_name='Подписки', blank=True, related_name='post_feeds')
    followers = models.ManyToManyField(User, verbose_name='Подписчики', blank=True, related_name='post_followers')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        url = reverse('post_page', args=[self.author.username, self.pk])
        return url


class PersonalBlog(models.Model):  # Модель хранения данных о публикациях, подписках и подписчиках
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post, verbose_name='Посты', blank=True, related_name='posts')
    feeds = models.ManyToManyField(User, verbose_name='Подписки', blank=True, related_name='feeds')
    followers = models.ManyToManyField(User, verbose_name='Подписчики', blank=True, related_name='followers')
    noted = models.ManyToManyField(Post, blank=True, verbose_name='Прочитано', related_name='noted')

    class Meta:
        verbose_name = 'Блог пользователя'
        verbose_name_plural = 'Блоги пользователей'

    def __str__(self):
        return self.author.username


class UserFollowing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following_posts', verbose_name='Пользователь',
                             on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followed_by', on_delete=models.CASCADE)


class AlreadyRead(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_read', verbose_name='Пользователь',
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='read_id', on_delete=models.CASCADE)
