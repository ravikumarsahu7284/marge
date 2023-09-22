from rest_framework import viewsets
from blog.models import User, Post, Category, Tags, Comment
from blog.serializers import UserSerializer, PostSerializer, CategorySerializer, TagsSerializer, CommentSerializer,  ReplySerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class TagsViewset(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticated]

class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

class ReplyViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(reply__isnull=False)
    # print(queryset, '65555555555555555555555555555555555')
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]