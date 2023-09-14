# Create DRF Api with modelview Set / Viewset 
from rest_framework import serializers
from .models import User, Post, Category, Tags, Comment
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
import re

class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField('get_token')
    class Meta:
        model = User
        fields = ('id', 'image', 'username', 'first_name', 'last_name', 'email', 'city', 'password', 'token')
        extra_kwargs = {
            'image': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'city': {'required': True},
            "password": {"write_only": True}
        }

    # def validate_username(self, value):
    #     username = value
    #     print(username, "ususususuusuususususuususususuu")
    #     username_exists = User.objects.filter(username=username)
    #     if username_exists.exists():
    #         raise serializers.ValidationError("username is not update")
    #     return value

    def validate_email(self, value):
        email = value
        email_exists = User.objects.filter(email=email) #check if email is not exist 
        accepted_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']
        username = self.initial_data.get('username', '')  # Use initial_data to access input data
        _, domain = email.split('@')
        if email_exists.exists():
            raise serializers.ValidationError("Email is taken")
        elif domain.lower() not in accepted_domains:
            raise serializers.ValidationError("PLEASE ENTER VALID EMAIL ADDRESS")
        return value

    def create(self, validated_data):
        # Hash the password before saving
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Update user fields and hash the password if provided
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance  
        
    def validate_username(self, value):
        # Custom username validation logic
        if len(value) < 5:  #check that input value leath is valid or not
            raise serializers.ValidationError("Username must be at least 5 characters long.")

        if not value.isalpha():  #use to check that input value has only alfabates value or not
            raise serializers.ValidationError("Username must contain only alphabetic characters.")

        if not value[0].isupper():
            raise serializers.ValidationError("Username must start with a capital letter.")

        user = self.instance  # Get the current user instance if available (None during creation)
        if user and user.username != value:
            raise serializers.ValidationError("You cannot update the username.")

        # if not value.islower():
        #     raise serializers.ValidationError("Usernames should be in Lower")

        # if not value.isupper():
        #     raise serializers.ValidationError("Usernames should be in Upper")

        # if not re.search(r'[a-zA-Z]', value):  #check that username have one alfabat charector or not
        #     raise serializers.ValidationError("Username must contain at least one alphabet character.")

        # if not re.search(r'[0-9]', value):  #check that username have one alfabat charector or not
        #     raise serializers.ValidationError("Password denied: must contain a number between 0 and 9")

        # if not re.search(r'[!, @, #, $, %, &, (, ), -, _, [, ], {, }, ;, :, ", ., /, <, >, ?]', value):  #check that username have one alfabat charector or not
        #     raise serializers.ValidationError("Password denied: must contain a special character")

        return value

    def validate_first_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("First name must be at least 3 characters long.")

        if not value.isalpha():  #use to check that input value has only alfabates value or not
            raise serializers.ValidationError("Username must contain only alphabetic characters.")
        return value

    def validate_last_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("First name must be at least 3 characters long.")

        if not value.isalpha():  #use to check that input value has only alfabates value or not
            raise serializers.ValidationError("Username must contain only alphabetic characters.")
        return value

    def validate_password(self, value):
        # Check that the password contains at least one alphabet character
        if not re.search(r'[a-zA-Z]', value):
            raise serializers.ValidationError("Password must contain at least one alphabet character.")

        # Check that the password contains at least one digit
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one digit (0-9).")

        # Check that the password contains at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")

        return value

   
        
    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class UserdetailsSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField('get_token')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'city', 'token')
        read_only_fields = ['id']

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class PostSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()
    # tags = TagsSerializer(many=True)
    post_image = serializers.SerializerMethodField('get_post_image_detail')
    # print(post_image, "yyyyyyyyyyyyyyyyyyyyyyyyyyyy")
    featured_image = serializers.SerializerMethodField('get_featured_image_detail')
    # print(featured_image, "mmmmmmmmmmmmmmmmmmmmmmmmm")

    class Meta:
        model = Post
        fields = ('id',  'title', 'text', 'category', 'tags', 'post_image', 'featured_image', 'author')
        # extra_kwargs = {
        #     'published_date': {'required': False},
        #     'title': {'required': False},
        #     'text': {'required': False},
        #     'category': {'required': False},
        #     'tags': {'required': False},
        #     'post_image': {'required': False},
        #     'featured_image': {'required': False},
        #     'author': {'required': False},
        # }

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

    def validate_title(self, value):
        if len(value) < 5 or len(value) > 56:
            raise serializers.ValidationError("Post Title must be at 5 to 56 characters long.")
        return value
        
        # if len(value) > 56:
        # 	raise serializers.ValidationError("Post Title must be at 5 to 56 characters long.")

    # def validate_title(self, value):
    #     if len(value) < 5 or len(value) > 56:
    #         raise serializers.ValidationError("Tags Name must be at 3 to 9 characters long.")
    #     return value

class PostdetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'published_date',  'title', 'text')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name',)
    
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Category Name must be at 3 to 9 characters long.")

        if not value.isalpha():  #use to check that input value has only alfabates value or not
            raise serializers.ValidationError("Category Name must contain only alphabetic characters.")
        return value
    

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id','name',)

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Tags Name must be at 3 to 9 characters long.")

        if not value.isalpha():  #use to check that input value has only alfabates value or not
            raise serializers.ValidationError("Tags Name must contain only alphabetic characters.")
        return value


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'post', 'name', 'created_date', 'email', 'massage')
        extra_kwargs = {
            'post': {'required': False},
            'name': {'required': False},
            'created_date': {'required': False},
            'email': {'required': False},
            'massage': {'required': False},
            'reply': {'required': False},
        }

    def validate_email(self, value):
        email = value
        email_exists = User.objects.filter(email=email) #check if email is not exist 
        accepted_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']
        username = self.initial_data.get('username', '')  # Use initial_data to access input data
        _, domain = email.split('@')
        if email_exists.exists():
            raise serializers.ValidationError("Email is taken")
        elif domain.lower() not in accepted_domains:
            raise serializers.ValidationError("PLEASE ENTER VALID EMAIL ADDRESS")
        return value

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 3 characters long.")

        if not value.isalpha():  #use to check that input value has only alfabates value or not
            raise serializers.ValidationError("Username must contain only alphabetic characters.")
        return value

   


    # def get_reply(self, obj):
    #     replies = Comment.objects.filter(reply=obj.id).all()  
    #     # print(replies, "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    #     reply_serializer = CommentSerializer(replies, many=True)
    #     return reply_serializer.data


class ReplySerializer(serializers.ModelSerializer):
    all_reply = serializers.SerializerMethodField('get_reply')
    # reply = Comment.objects.filter(reply=none, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'name', 'created_date', 'massage', 'email', 'all_reply','reply' )

    def get_reply(self, obj):
        if obj.id:
            replies = Comment.objects.filter(reply=obj.id)
            # print(replies, "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            reply_serializer = CommentSerializer(replies, many=True, read_only=True)
            # reply = Comment.objects.filter(reply=None, read_only=True)
            # print(reply, "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            return reply_serializer.data
        else:
            return none
        







# class CommentChildSerializer(serializers.ModelSerializer):
#     # comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(),source='comment.id')
#     reply_id = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False)
#     # print(comment_id, 'hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
#     # author = SerializerMethodField()
#     class Meta:
#         model = Comment
#         fields = ('id','name', 'email', 'comment', 'reply_id')

#     def get_author(self, obj):
#         return obj.author.username

#     def create(self, validated_data):
#         subject = Comment.objects.create(comment=validated_data['comment']['id'], content=validated_data['comment'])
#         print(subject, "ppppppppppppppppppppppppppppp")

# class CommentSerializer(serializers.ModelSerializer):
#     reply_count = Comment()
#     # author = SerializerMethodField()
#     reply = CommentChildSerializer()
#     class Meta:
#         model = Comment
#         fields = ('id','name', 'email', 'comment', 'reply')

#     def get_reply_count(self, obj):
#         if obj.is_comment:
#             return obj.children().count()
#         return 0

#     def get_author(self, obj):
#         return obj.author.username

#     def get_reply(self, obj):
#         if obj.is_comment:
#             return CommentChildSerializer(obj.children(), many=True).data
#         return None