# Api/urls.py
from django.urls import path
from .Views.auth import LoginView, RegisterView, ProfileAPiView, ProfileUpdateAPiView, DeleteProfileAPiView, ProfileListAPiView
from .Views.blog import PostListAPiView, PostdetailAPiView, PostCreateAPiView, PostUpdateAPiView, DeletepostAPiView
from .Views.comment import CommentListAPIView
# from .View.authwithmodel import 


urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('loginpage/', LoginView.as_view(), name='loginpage'),
    path('profilepage/', ProfileAPiView.as_view(), name='profilepage'),
    path('profileupdatepage/', ProfileUpdateAPiView.as_view(), name='profileupdatepage'),
    path('profileDelete/', DeleteProfileAPiView.as_view(), name='profileDelete'),
    path('profileList/', ProfileListAPiView.as_view(), name='profileList'),
    path('postlist/', PostListAPiView.as_view(), name='postlist'),
    path('postdetail/', PostdetailAPiView.as_view(), name='postdetail'),
    path('postcreate/', PostCreateAPiView.as_view(), name='postcreate'),
    path('postupdate/', PostUpdateAPiView.as_view(), name='postupdate'),
    path('postdelete/', DeletepostAPiView.as_view(), name='postdelete'),
    path('commentdetails/<int:id>/', CommentListAPIView.as_view(), name='commentdetails'),
    path('commentlist/', CommentListAPIView.as_view(), name='commentlist'),
]
