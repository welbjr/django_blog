from django.urls import path
from .views import (
    HomeView,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostDeleteView,
    PostUpdateView,
    CommentDeleteView,
    CommentUpdateView,
    comment_create,
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name="post_delete"),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name="post_update"),
    path('posts/new/', PostCreateView.as_view(), name='post_create'),
    path('comments/new/', comment_create, name='comment_create'),
    path('comments/<int:pk>/delete/',
         CommentDeleteView.as_view(), name='comment_delete'),
    path('comments/<int:pk>/update/',
         CommentUpdateView.as_view(), name='comment_update'),
]
