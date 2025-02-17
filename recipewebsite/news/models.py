from django.db import models
from django.contrib.auth.models import User

class Articles(models.Model):
    title = models.CharField('Название', max_length=50)
    anons = models.CharField('Анонс', max_length=250)
    full_text = models.TextField('Текст статьи')
    date = models.DateTimeField('Дата публикации')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/news/{self.id}'
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class Comment(models.Model):
    article = models.ForeignKey(Articles, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, default="Anonymous")  # Поле для имени
    email = models.EmailField(blank=True, null=True)  # Поле для электронной почты
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.content}"