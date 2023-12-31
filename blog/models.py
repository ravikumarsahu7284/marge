from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from autoslug import AutoSlugField
from django.contrib import admin


class User(AbstractUser):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    phone_number = models.CharField(max_length = 10)
    email = models.EmailField(unique = True)
    city = models.CharField(max_length = 100)
    address = models.CharField(max_length = 100, blank=True, null=True)
    image = models.ImageField(upload_to='images/')    
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.username
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)
    # category_name = models.CharField(max_length=50,unique=True)
    # slug = models.SlugField(unique=True)
    description = models.CharField(max_length=255)
    
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
    featured_image = models.ImageField(upload_to='featured_image/%Y/%m/%d/')
    post_image = models.ImageField(upload_to='post_images/')  # Image field for the post
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
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)  # Allow null if needed
    name = models.CharField(max_length=80) 
    created_date = models.DateTimeField(default=timezone.now)
    email = models.EmailField() 
    massage = models.TextField() 
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True, default=None)
    
    def __str__(self):
        return str(self.name) + ' reply ' + str(self.massage)

    @property
    def children(self):
        return Comment.objects.filter(reply=self).reverse()

    @property
    def is_reply(self):
        if self.reply is None:
            return True
        return False


class Hoteldata(models.Model):
    continent = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    hotelname = models.CharField(max_length=255)
    stars = models.PositiveIntegerField()
    date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_Price = models.DecimalField(max_digits=10, decimal_places=2)

