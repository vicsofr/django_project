from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation


class Posts(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    content = RichTextUploadingField(verbose_name='Содержание')
    picture = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, verbose_name='Изображение')
    date_add = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    date_upd = models.DateTimeField(auto_now=True, verbose_name='Отредактировано')
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, editable=False)
    tags = TaggableManager(verbose_name='Теги')
    views = models.IntegerField(default=0, verbose_name='Просмотры', editable=False)
    comments = GenericRelation('comment')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-date_add']

    def get_absolute_url(self):
        return reverse('post_view', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    author_id = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Комментарий')
    parent = models.ForeignKey(
        'self',
        verbose_name='Родительский комментарий',
        blank=True,
        null=True,
        related_name='child_comment',
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    comment_date = models.DateTimeField(auto_now=True, verbose_name='Дата комментария')
    is_child = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return str(self.id)

    @property
    def get_parent(self):
        if not self.parent:
            return ""
        return self.parent
