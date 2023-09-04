from rest_framework import serializers
from .models import User, Post, Category, Tags, Comment
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
	token = serializers.SerializerMethodField('get_token')
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name', 'email', 'city', 'token')

	def get_token(self, obj):
		token, created = Token.objects.get_or_create(user=obj)
		return token.key

class UserdetailsSerializer(serializers.ModelSerializer):
	token = serializers.SerializerMethodField('get_token')
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name', 'email', 'city', 'token')

	def get_token(self, obj):
		token, created = Token.objects.get_or_create(user=obj)
		return token.key


class CategorySerializer(serializers.ModelSerializer):
	# token = serializers.SerializerMethodField('get_token')
	class Meta:
		model = Category
		fields = ('id','name',)

class TagsSerializer(serializers.ModelSerializer):
	# token = serializers.SerializerMethodField('get_token')
	class Meta:
		model = Tags
		fields = ('id','name',)


class PostSerializer(serializers.ModelSerializer):
	category = CategorySerializer()
	tags = TagsSerializer(many=True)
	post_image = serializers.SerializerMethodField('get_post_image_detail')
	featured_image = serializers.SerializerMethodField('get_featured_image_detail')

	class Meta:
		model = Post
		fields = ('id', 'published_date',  'title', 'text', 'category', 'tags', 'post_image', 'featured_image')

	def get_post_image_detail(self, obj):
		request = self.context.get('request', None)
		url = None
		if request:
			if obj.post_image:
				url = request.build_absolute_uri(obj.post_image.url)
		return url

	def get_featured_image_detail(self, obj):
		request = self.context.get('request', None)
		url = None
		if request:
			if obj.featured_image:
				url = request.build_absolute_uri(obj.featured_image.url)
		return url


class PostdetailsSerializer(serializers.ModelSerializer):

	class Meta:
		model = Post
		fields = ('id', 'published_date',  'title', 'text')


class CommentSerializer(serializers.ModelSerializer):
	reply = serializers.SerializerMethodField('get_reply')

	class Meta:
		model = Comment
		fields = ('id', 'post', 'name', 'created_date', 'email', 'comment', 'reply')

	def get_reply(self, obj):
		replies = Comment.objects.filter(reply=obj.id).all()  
		print(replies, "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
		reply_serializer = CommentSerializer(replies, many=True)
		return reply_serializer.data



# class CommentdetailsSerializer(serializers.ModelSerializer):
# 	reply = serializers.SerializerMethodField('get_reply')

# 	class Meta:
# 		model = Comment
# 		fields = ('id', 'post', 'name', 'created_date', 'email', 'comment', 'reply')

# 	def get_reply(self, obj):
# 		replies = Comment.objects.filter(reply=obj.id)
# 		print(replies, "ppppppppppppppppppppppppppppppp")
# 		reply_serializer = CommentdetailsSerializer(replies, many=True)
# 		print(reply_serializer, "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
# 		return reply_serializer.data


