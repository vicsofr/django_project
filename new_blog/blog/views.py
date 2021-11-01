from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.views.generic import View, ListView, DetailView, CreateView
from django.contrib.auth import login, logout
from django.contrib import messages
from taggit.models import Tag
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin


class PostsView(View):
    def get(self, request, *args, **kwargs):
        posts = Posts.objects.all()
        paginator = Paginator(posts, 6)
        title = 'Главная'
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'blog/index.html', context={
            'page_obj': page_obj,
            'title': title,
            'pages': paginator.num_pages
        })


class PostsDetail(DetailView):
    model = Posts
    template_name = 'blog/post_view.html'
    context_object_name = 'posts_item'

    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj


class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        results = ""
        if query:
            results = Posts.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        paginator = Paginator(results, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/search.html', context={
            'title': 'Поиск',
            'page_obj': page_obj,
            'count': paginator.count,
            'pages': paginator.num_pages,
            'query': query
        })


class TagView(View):
    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Posts.objects.filter(tags=tag)
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/post_by_tag.html', context={
            'title': f'#ТЕГ {tag}',
            'page_obj': page_obj,
            'pages': paginator.num_pages
        })


class CreatePost(LoginRequiredMixin, CreateView):
    form_class = PostsForm
    template_name = 'blog/add_post.html'
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы вошли в систему!')
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'blog/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


