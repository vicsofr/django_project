from django.urls import path
from .views import PostsView, register, user_login, user_logout, CreatePost, TagView, SearchResultsView, \
    create_child_comment, create_comment, base_view

urlpatterns = [
    path('', PostsView.as_view(), name='home'),
    path('posts/<int:pk>/', base_view, name='post_view'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('add_post/', CreatePost.as_view(), name='add_post'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('tag/<slug:slug>/', TagView.as_view(), name="tag"),
    path('create_comment/', create_comment, name='comment_create'),
    path('create_child_comment/', create_child_comment, name='comment_child_create')
]
