from django.contrib import admin
from .models import Posts, Comment


class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'content', 'picture', 'date_add', 'date_upd',
                    'author', 'tags', 'views')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('tags',)
    list_filter = ('author', 'tags')




admin.site.register(Posts, PostsAdmin)
admin.site.register(Comment)
