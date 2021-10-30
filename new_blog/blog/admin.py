from django.contrib import admin
from .models import Posts


class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'content', 'picture', 'date_add', 'date_upd',
                    'author', 'tags', 'views')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('tags',)
    list_filter = ('author', 'tags')

    # def get_photo(self, obj):
    #     if obj.photo:
    #         return mark_safe(f'<img src="{obj.photo.url}" width="75">')
    #     else:
    #         return '¯\_(ツ)_/¯'
    #
    # get_photo.short_description = 'Photo'


admin.site.register(Posts, PostsAdmin)
