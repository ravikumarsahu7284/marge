# # apivalid/urls.py
from django.urls import path
from .view1.authvalidviews import  UserRegistrationViewSet1, UserCreateListViewSet1, UserloginSerializer1, PostCreateViewSet1, PostUpdateViewSet1, CommentCreateViewSet1, CommentUpdateViewSet1
from .view1.authvalidviews import TagsCreateViewSet1, TagsUpdateViewSet1, ReplyCreateViewSet1, CategoryCreateViewSet1, CategoryUpdateViewSet1


user_list = UserCreateListViewSet1.as_view({'get': 'list', 'post': 'create'})
user_detail = UserRegistrationViewSet1.as_view({'get': 'retrieve', 'put': 'update','delete': 'destroy'})
user_login = UserloginSerializer1.as_view({'patch': 'login', 'get': 'logout'})

post_list = PostCreateViewSet1.as_view({'post': 'create'})  #create new post
post_create = PostUpdateViewSet1.as_view({'get': 'list'}) #only list show
post_detail = PostUpdateViewSet1.as_view({'get': 'retrieve', 'put': 'update','delete': 'destroy'}) #delete, update, post-details, 

comment_create = CommentCreateViewSet1.as_view({'post': 'create'}) #crete comment
comment_list = CommentUpdateViewSet1.as_view({'get': 'list'}) #only list show
comment_update = CommentUpdateViewSet1.as_view({'get': 'retrieve', 'put': 'update','delete': 'destroy'}) #only list show

tags_create = TagsCreateViewSet1.as_view({'post': 'create'}) #crete comment
tags_list = TagsUpdateViewSet1.as_view({'get': 'list'}) #only list show
tags_update = TagsUpdateViewSet1.as_view({'get': 'retrieve', 'put': 'update','delete': 'destroy'}) #only list show

category_create = CategoryCreateViewSet1.as_view({'post': 'create'}) #crete comment
category_list = CategoryUpdateViewSet1.as_view({'get': 'list'}) #only list show
category_update = CategoryUpdateViewSet1.as_view({'get': 'retrieve', 'put': 'update','delete': 'destroy'}) #only list show

# reply_update = ReplyUpdateViewSet1.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}) #update, delete, details
# reply_details = ReplyUpdateViewSet1.as_view({'get': 'list'}) #create reply
reply_create = ReplyCreateViewSet1.as_view({'post': 'create'}) #create reply


urlpatterns = [
	path('users/', user_list, name='user-list'),
	path('users/<int:pk>/', user_detail, name='user-detail'),
	path('login/', user_login, name='login'),
    path('logout/', user_login, name='logout'),

	path('api/posts/', post_list, name='post-list'),
	path('posts/', post_create, name='post-create'),
	path('new/posts/<int:pk>/', post_detail, name='post-detail'),
	
	path('comments/<int:pk>/', comment_create, name='comment-create'),
	path('comments/ftr/<int:pk>/', comment_update, name='comment-create'),
	path('comments-list/', comment_list, name='comment-list'),

	path('api/tags/', tags_create, name='tags-o'), #create tags
	path('tags/ftr/<int:pk>/', tags_update, name='tags-create'), #tags update, delete, details 
	path('tags-list/', tags_list, name='tags-list'), #all tags list

	path('api/category/', category_create, name='category-o'), #create tags
	path('category/ftr/<int:pk>/', category_update, name='category-create'), #tags update, delete, details 
	path('category-list/', category_list, name='category-list'), #all tags list

	# path('reply/ftr/<int:pk>/', reply_update, name='reply-create'), #tags update, delete, details 
	# path('reply-list/', reply_details, name='reply-list'), #all reply list
	path('api/reply/<int:pk>/', reply_create, name='reply-o'), #create reply
	# path('comments/<int:comment_pk>/', ReplyCreateViewSet.as_view({'post': 'create'}), name='reply-create')
]
