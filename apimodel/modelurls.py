# # apiview/urls.py
from django.urls import path
from .view.authview import  UserRegistrationViewSet, UserCreateListViewSet, UserloginSerializer, PostCreateViewSet, PostUpdateViewSet, CommentCreateViewSet, CommentUpdateViewSet
from .view.authview import TagsCreateViewSet, TagsUpdateViewSet, ReplyCreateViewSet, ReplyUpdateViewSet


# urlpatterns = [
#     # ... other URL patterns ...
#     path('api/reply/', ReplyUpdateViewSet.as_view({'post': 'create'}), name='reply-o'),
#     # path('api/Userupdate/<int:pk>', UserupdateViewSet.as_view({'post': 'update'}), name='user-update'),
#     # path('api/Userdelete/<int:pk>', UserdeleteViewSet.as_view({'post': 'Delete'}), name='user-delete'),
#     # path('api/Post-create/', PostCreateViewSet.as_view({'post': 'create'}), name='Post-create'),
# ]


user_list = UserCreateListViewSet.as_view({'get': 'list', 'post': 'create'})
user_detail = UserRegistrationViewSet.as_view({'get': 'retrieve', 'put': 'update','delete': 'destroy'})
user_login = UserloginSerializer.as_view({'patch': 'login', 'get': 'logout'})

post_list = PostCreateViewSet.as_view({'post': 'create'})  #create new post
post_create = PostUpdateViewSet.as_view({'get': 'list'}) #only list show
post_detail = PostUpdateViewSet.as_view({'get': 'retrieve', 'put': 'update','delete': 'destroy'}) #delete, update, post-details, 


comment_create = CommentCreateViewSet.as_view({'post': 'create'}) #crete comment
comment_list = CommentUpdateViewSet.as_view({'get': 'list'}) #only list show
comment_update = CommentUpdateViewSet.as_view({'get': 'retrieve', 'put': 'update','delete': 'destroy'}) #only list show

tags_create = TagsCreateViewSet.as_view({'post': 'create'}) #crete comment
tags_list = TagsUpdateViewSet.as_view({'get': 'list'}) #only list show
tags_update = TagsUpdateViewSet.as_view({'get': 'retrieve', 'put': 'update','delete': 'destroy'}) #only list show

reply_update = ReplyUpdateViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}) #update, delete, details
reply_details = ReplyUpdateViewSet.as_view({'get': 'list'}) #create reply
reply_create = ReplyCreateViewSet.as_view({'post': 'create'}) #create reply


urlpatterns = [
	path('users/', user_list, name='user-list'),
	path('users/<int:pk>/', user_detail, name='user-detail'),
	path('login/', UserloginSerializer.as_view({'post': 'login'}), name='login'),
    path('logout/', UserloginSerializer.as_view({'post': 'logout'}), name='logout'),

	path('api/posts/', post_list, name='post-list'),
	path('posts/', post_create, name='post-create'),
	path('new/posts/<int:pk>/', post_detail, name='post-detail'),
	
	path('comments/<int:pk>/', comment_create, name='comment-create'),
	path('comments/ftr/<int:pk>/', comment_update, name='comment-create'),
	path('comments-list/', comment_list, name='comment-list'),

	path('api/tags/', tags_create, name='tags-o'), #create tags
	path('tags/ftr/<int:pk>/', tags_update, name='tags-create'), #tags update, delete, details 
	path('tags-list/', tags_list, name='tags-list'), #all tags list

	path('reply/ftr/<int:pk>/', reply_update, name='reply-create'), #tags update, delete, details 
	path('reply-list/', reply_details, name='reply-list'), #all reply list
	path('api/reply/<int:pk>/', reply_create, name='reply-o'), #create reply
	# path('comments/<int:comment_pk>/', ReplyCreateViewSet.as_view({'post': 'create'}), name='reply-create')
]
