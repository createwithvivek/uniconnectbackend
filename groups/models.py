from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Group(models.Model):
    GROUP_TYPE_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    name = models.CharField(max_length=255)
    description = models.TextField()
    group_type = models.CharField(max_length=20, choices=GROUP_TYPE_CHOICES, default='public')
    category = models.CharField(max_length=100, help_text="Industry/Interest (AI, Fintech, etc.)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

class GroupPost(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
