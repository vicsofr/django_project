from django import template
from blog.models import Posts
from django.db.models import Count, F
from taggit.models import Tag

register = template.Library()


@register.simple_tag()
def get_tags():
    common_tags = Posts.tags.most_common()[:10]
    return common_tags
