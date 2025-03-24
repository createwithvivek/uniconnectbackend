from django.urls import path
from .views import PostCreateView, PostListView, LikeCreateView, CommentCreateView, RetweetView

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('list/', PostListView.as_view(), name='list_posts'),
    path('like/', LikeCreateView.as_view(), name='like_post'),
    path('comment/', CommentCreateView.as_view(), name='comment_post'),
    path('retweet/', RetweetView.as_view(), name='retweet_post'),
]
