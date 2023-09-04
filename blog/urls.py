from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from .views import edit_profile


urlpatterns = [
    path('', views.post_list, name='post_list'),    
    path('post/<str:slug>/edit/', views.post_edit, name='post_edit'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<str:slug>/', views.post_detail, name='post_detail'),
    path('register/', views.register, name='register'),
    path("login/", views.login_page, name="login"),    
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_user, name='logout'),
    path('post_category/<str:slug>/', views.post_category, name='post_category'),
    path('post_tags/<str:slug>/', views.post_tags, name='post_tags'),
    path('authorfilter/<str:slug>/', views.post_author, name='author_filter'),
    path('postdatefilter/<str:slug>/', views.post_date, name='published_date'),
    path('task/', views.upload_excel, name='task'),
]

