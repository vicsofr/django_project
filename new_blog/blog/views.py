from django.shortcuts import render
from .models import *


def index(request):
    posts = Posts.objects.all()
    context = {
        'posts': posts,
        'title': 'Все посты',
    }
    return render(request, 'blog/index.html', context)
