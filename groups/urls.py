from django.urls import path
from .views import GroupCreateView, GroupListView, GroupJoinView, GroupPostCreateView

urlpatterns = [
    path('create/', GroupCreateView.as_view(), name='create_group'),
    path('list/', GroupListView.as_view(), name='list_groups'),
    path('join/', GroupJoinView.as_view(), name='join_group'),
    path('post/', GroupPostCreateView.as_view(), name='create_group_post'),
]
