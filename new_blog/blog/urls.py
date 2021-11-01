from django.urls import path
from .views import PostsView, PostsDetail, register, user_login, user_logout, CreatePost, TagView, SearchResultsView

urlpatterns = [
    path('', PostsView.as_view(), name='home'),
    path('posts/<int:pk>/', PostsDetail.as_view(), name='post_view'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('add_post/', CreatePost.as_view(), name='add_post'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('tag/<slug:slug>/', TagView.as_view(), name="tag"),
]
