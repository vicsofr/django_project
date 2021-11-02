from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.views.generic import View, DetailView, CreateView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from taggit.models import Tag
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import create_comment_tree
from django.http import HttpResponseRedirect
from django.db import transaction


class PostsView(View):
    def get(self, request):
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


def base_view(request, pk):
    posts_item = get_object_or_404(Posts, pk=pk)
    obj = Posts.objects.get(id=pk)
    # Переделать счётчик просмотров. Считает лишние при редиректе после отправки комментариев
    obj.views = obj.views + 1
    obj.save()
    request.session['post_id'] = posts_item.pk
    comments = posts_item.comments.all()
    result = create_comment_tree(comments)
    comment_form = CommentForm(request.POST or None)
    return render(request, 'blog/post_view.html', context={
        'comments': result,
        'comment_form': comment_form,
        'posts_item': posts_item
    })


def create_comment(request):
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.author_id = request.user
        new_comment.text = comment_form.cleaned_data['text']
        new_comment.content_type = ContentType.objects.get(model='posts')
        new_comment.object_id = request.session['post_id']
        new_comment.parent = None
        new_comment.is_child = False
        new_comment.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


@transaction.atomic
def create_child_comment(request):
    user_name = request.POST.get('user')
    current_id = request.POST.get('id')
    text = request.POST.get('text')
    user = User.objects.get(username=user_name)
    content_type = ContentType.objects.get(model='posts')
    object_id = request.session['post_id']
    parent = Comment.objects.get(id=int(current_id))
    is_child = False if not parent else True
    Comment.objects.create(
        author_id=user, text=text, content_type=content_type, object_id=object_id,
        parent=parent, is_child=is_child
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class SearchResultsView(View):
    def get(self, request):
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
    def get(self, request, slug):
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
