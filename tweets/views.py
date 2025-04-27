from urllib import request, response
from rest_framework import generics, permissions
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer

class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

class LikeCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        post = request.data.get('post') 

        if post:
            post = Post.objects.get(pk=post)
            like, created = Like.objects.get_or_create(user=request.user, post=post)
            if created:
                return response({'status': 'liked'})
            else:
                like.delete()
                return response({'status': 'unliked'})

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RetweetView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        original_post_id = request.data.get('original_post')
        original_post = Post.objects.get(pk=original_post_id)
        new_post = Post.objects.create(
            author=request.user,
            content=original_post.content,
            hashtags=original_post.hashtags,
            original_post=original_post
        )
        serializer = self.get_serializer(new_post)
        return Response(serializer.data)
