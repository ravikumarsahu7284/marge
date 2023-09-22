from django.urls import path, include
from rest_framework import routers
from .view.auth import UserViewset, PostViewset, CategoryViewset, TagsViewset, CommentViewset, ReplyViewset

router = routers.DefaultRouter()
router.register(r'user', UserViewset)
router.register(r'post', PostViewset)
router.register(r'category', CategoryViewset)
router.register(r'tags', TagsViewset)
router.register(r'comment', CommentViewset)
router.register(r'reply', ReplyViewset)

urlpatterns = [
    path('', include(router.urls)),
]

