from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from blog.models import User, Post, Tags, Category, Comment
from blog.serializers import UserSerializer, PostSerializer, CommentSerializer, TagsSerializer, ReplySerializer, CategorySerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout


# User ragister aPI Done
class UserRegistrationViewSet1(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = User.objects.create(email=validated_data['email'],
       username=validated_data['username'],
       password = make_password(validated_data['password']))
        return self.update(request, *args, **kwargs)

    # def patch(self, request, *args, **kwargs):
    #     self.s_password = make_password(self.s_password)
    #     return self.login(request, *args, **kwargs)
        
# User create done 
class UserCreateListViewSet1(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


    def get(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
# Done 
class UserloginSerializer1(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    # not working
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()
        if user is not None and user.check_password(password):
            login(request, user)
            return Response(UserSerializer(user).data)
        else:
            return Response({"error": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)

    # working done
    def logout(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({"message": "Logged out successfully"})
        else:
            return Response({"error": "Not authenticated"}, status=status.HTTP_401_UNAUTH)

# ----------------------------------------------------------------------------------------------Post-----------------------------------


# Done 
class PostCreateViewSet1(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def create(self, request):
        res = {}
        author = request.data.get("author", None)
        title = request.data.get("title", None)
        text = request.data.get("text", None)
        post_image = request.data.get("post_image", None)
        featured_image = request.data.get("featured_image", None)
        category = request.data.get("category")  # Change to category_id

        tags = request.data.get("tags", []).split(",") if "tags" in request.data else []

        data_dict = {
            "author": author, 
            "title": title,
            "text": text,
            "category": category,  
            "featured_image": featured_image,
            "post_image": post_image,
            "tags": tags, 
        }

        serializer = PostSerializer(data=data_dict)

        if serializer.is_valid():
            serializer.save(featured_image=featured_image, post_image=post_image)
            # print(serializer.save(), "xxxxxxxxxxxxxxxxxxxxxx")
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update, Delete, get Done
class PostUpdateViewSet1(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, pk=None):
        post = self.get_object()

        # Update the fields with the new data from the request
        post.author = request.data.get("author", post.author)
        post.title = request.data.get("title", post.title)
        post.text = request.data.get("text", post.text)
        post.post_image = request.data.get("post_image", post.post_image)
        post.featured_image = request.data.get("featured_image", post.featured_image)
        category_id = request.data.get("category")

        if category_id is not None:
            try:
                # Fetch the Category instance based on the provided category_id
                category = Category.objects.get(pk=category_id)
                post.category = category
            except Category.DoesNotExist:
                return Response(data={"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)

        tags = request.data.get("tags", [])

        if tags:
            post.tags.clear()  # Clear existing tags
            for tag_name in tags.split(","):
                try:
                    tag = Tags.objects.get(id=tag_name.strip())
                    post.tags.add(tag)
                except Tags.DoesNotExist:
                    return Response(data={"error": "Tag not found"}, status=status.HTTP_400_BAD_REQUEST)

        post.save()

        serializer = PostSerializer(post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

# ------------------------------------------------------------------------------------------------Category----------------------------------------
# Done 
class CategoryCreateViewSet1(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [AllowAny]


    def get(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class CategoryUpdateViewSet1(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [AllowAny]


    def get(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

# -------------------------------------------------------------------------------------------------Tags----------------------------------------

# Tags create successfully 
class TagsCreateViewSet1(viewsets.ModelViewSet):
    serializer_class = TagsSerializer

    def create(self, request, pk=None):
        res = {}
        post = request.data.get("post", None)
        name = request.data.get("name", None)
        # email = request.data.get("email", None)
        # comment = request.data.get("comment", None)
        # reply = request.data.get("reply", None)

        data_dict = {
            "post": post, 
            "name": name,
            # "email": email,
            # "comment": comment,  
            # "reply": reply,
        }

        serializer = TagsSerializer(data=data_dict)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Tags update successfully 
class TagsUpdateViewSet1(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, pk=None):
        tags = self.get_object()

        # Update the fields with the new data from the request
        # post = request.data.get("post", comment.post)
        tags.name = request.data.get("name", tags.name)
        # comment.created_date = request.data.get("created_date", comment.created_date)
        # comment.email = request.data.get("email", comment.email)
        # comment.comment = request.data.get("comment", comment.comment)
        # comment.reply = request.data.get("reply", comment.reply)
        
        data_dict = {
            # "post": post,  #(use to give post id in postman field)
            "name": tags.name,
            # "email": comment.email,
            # "created_date": comment.created_date,
            # "comment": comment.comment,  
            # "reply": comment.reply,
        }

        tags.save()

        serializer = TagsSerializer(tags)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

# -------------------------------------------------------------------------------------------------Comment-----------------------------------

# Comment create successfully 
class CommentCreateViewSet1(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def create(self, request, pk=None):
        res = {}
        post = request.data.get("post", None)
        name = request.data.get("name", None)
        email = request.data.get("email", None)
        massage = request.data.get("massage", None)
    
        reply = request.data.get("reply", None)

        data_dict = {
            "post": post, 
            "name": name,
            "email": email,
            "massage": massage,  
            "reply": reply,
        }
        serializer = CommentSerializer(data=data_dict)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update, delete, details of single comment with id Done
class CommentUpdateViewSet1(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, pk=None):
        comment = self.get_object()

        # Update the fields with the new data from the request
        # post = request.data.get("post", comment.post)
        comment.name = request.data.get("name", comment.name)
        comment.created_date = request.data.get("created_date", comment.created_date)
        comment.email = request.data.get("email", comment.email)
        comment.massage = request.data.get("massage", comment.massage)
        # comment.reply = request.data.get("reply", comment.reply)

        data_dict = {
            # "post": post,  #(use to give post id in postman field)
            "name": comment.name,
            "email": comment.email,
            "created_date": comment.created_date,
            "massage": comment.massage,  
            # "reply": comment.reply,
        }

        comment.save()

        serializer = CommentSerializer(comment)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

# --------------------------------------------------------------------------------------------------Reply-------------------------------------

        
class ReplyCreateViewSet1(viewsets.ModelViewSet):
    serializer_class = ReplySerializer
    queryset = Comment.objects.filter(reply__isnull=True)
    # serializer_class = CommentSerializer

    def create(self, request, pk=None):
        res = {}
        post = request.data.get("post", None)
        name = request.data.get("name", None)
        email = request.data.get("email", None)
        massage = request.data.get("massage", None)
        reply = request.data.get("reply", None)

        data_dict = {
            "post" : post,
            "name": name,
            "email": email,
            "massage": massage,  
            "reply": pk,
        }

        reply = ReplySerializer(data=data_dict)

        if reply.is_valid():
            reply.save()
            return Response(data=reply.data, status=status.HTTP_201_CREATED)
        else:
            print(reply.errors)
            return Response(data=reply.errors, status=status.HTTP_400_BAD_REQUEST)



# class ReplyUpdateViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentSerializer

#     def create(self, request, pk=None):
#         res = {}
#         massage = request.data.get("massage", None)
#         name = request.data.get("name", None)
#         reply = request.data.get("reply", None)

#         data_dict = {
#             "name": name,
#             "massage": massage,  
#             "reply": reply,
#         }

#         serializer = ReplySerializer(data=data_dict)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             print(serializer.errors)
#             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

