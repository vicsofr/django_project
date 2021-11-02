from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostsViewSet, TagDetailView, TagView, Top10TagView, \
    RegisterView, ProfileView, LogoutView, CommentView, AllCommentView

router = DefaultRouter()
router.register('posts', PostsViewSet, basename='posts')

urlpatterns = [
    path("", include(router.urls)),
    path("tags/", TagView.as_view()),
    path("tags/top", Top10TagView.as_view()),
    path("tags/<slug:tag_slug>/", TagDetailView.as_view()),
    path('register/', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('logout/', LogoutView.as_view()),
    path("comments/", AllCommentView.as_view()),
    path("comments/<slug:post_slug>/", CommentView.as_view()),
]
