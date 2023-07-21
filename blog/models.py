from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from autoslug import AutoSlugField
from django.contrib import admin

class User(AbstractUser):
    phone_number = models.CharField(max_length = 10)
    email = models.EmailField(unique = True)
    city = models.CharField(max_length = 100)
    address = models.CharField(max_length = 100, blank=True, null=True)
    image = models.ImageField(upload_to='images/')    

    def __str__(self):
        return self.username
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)
    # category_name = models.CharField(max_length=50,unique=True)
    # slug = models.SlugField(unique=True)
    # description = models.TextField()
    
    def __str__(self):  
        return self.name
      
class Tags(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)
    # description = models.TextField()

    # @staticmethod
    # def post_category(Category_id):
    #     if Category_id :
    #         return Post.objects.filter(post = Category_id)
    #     else :
    #         return Post.objects.filter()

    def __str__(self):
        return self.name
    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    # created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='postimages/', blank=True)
    featured_image = models.ImageField(upload_to='featured_image/%Y/%m/%d/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags)
    slug = AutoSlugField(populate_from='title', unique=True)
    


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model): 
    # sno = models.AutoField(primary_key= True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    name = models.CharField(max_length=80) 
    created_date = models.DateTimeField(default=timezone.now)
    email = models.EmailField() 
    comment = models.TextField() 
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='replies', null=True, blank=True, default=None)
    
    def __str__(self):
        return str(self.name) + ' comment ' + str(self.comment)

    @property
    def children(self):
        return Comment.objects.filter(reply=self).reverse()

    @property
    def is_reply(self):
        if self.reply is None:
            return True
        return False

