
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from blog.serializers import PostSerializer, PostdetailsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from blog.models import User, Post, Category, Tags
# from rest_framework.parsers import FileUploadParser


# Collect all post data in a list  // Done
class PostListAPiView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		res = {}
		try:
			post = Post.objects.filter(author=request.user.id).all()
			if post is None:
				res['status'] = False
				res['message'] = "Authentication detail not found!!"
				res['data'] = []
				return Response(res,  status=status.HTTP_404_NOT_FOUND)

			serializer = PostSerializer(post, read_only=True, many=True, context={'request': request})

			if serializer:
				res['status'] = True
				res['message'] = 'User detail fetched successfully'
				res['data'] = serializer.data
				return Response(res, status=status.HTTP_200_OK)
			else:
				res['status'] = False
				res['message'] = "User Not Found!!"
				res['data'] = []
				return Response(serializer.errors,  status=status.HTTP_404_NOT_FOUND)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=status.HTTP_400_BAD_REQUEST)

# How to see post details  // Done
class PostdetailAPiView(APIView):
	# authentication_classes = (IsAuthenticated,)
	permission_classes = [IsAuthenticated]

	def get(self, request):
		res = {}
		try:
			post = Post.objects.filter().last()
			# print(post, 'kkkkkkkkk')
			if post is None:
				res['status'] = False
				res['message'] = "Post detail not found!!"
				res['data'] = []
				return Response(res,  status=status.HTTP_404_NOT_FOUND)

			serializer = PostSerializer(post, read_only=True, context={'request': request})
			
			if serializer:
				res['status'] = True
				res['message'] = 'Post detail fetched successfully'
				res['data'] = serializer.data
				return Response(res, status=status.HTTP_200_OK)
			else:
				res['status'] = False
				res['message'] = "Post Not Found!!"
				res['data'] = []
				return Response(res,  status=status.HTTP_404_NOT_FOUND)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=status.HTTP_400_BAD_REQUEST)

# How to create a new post 
class PostCreateAPiView(APIView):
	permission_classes = [AllowAny]
	# parser_classes = (FileUploadParser,)

	def post(self, request):
		res = {}
		title = request.data.get("title", None)
		text = request.data.get("text", None)
		post_image = request.data.get("image", None)
		featured_image = request.data.get("featured_image", None)
		category_name = request.data.get("category", None)
		tags = request.data.get("tags", [])

		# print(tags, 'fffffffffffffffffffaa')
		if title is None or text is None or category_name is None or not tags:
			res['status'] = False
			res['message'] = "Please provide all required fields"
			res['data'] = []
			return Response(res, status=status.HTTP_400_BAD_REQUEST)

		if post_image is None:
				res['status'] = False
				res['message'] = "post_image not found!!"
				res['data'] = []
				return Response(res,  status=status.HTTP_404_NOT_FOUND)

		if featured_image is None:
				res['status'] = False
				res['message'] = "Featured Image not found!!"
				res['data'] = []
				return Response(res,  status=status.HTTP_404_NOT_FOUND)

		try:
			category = Category.objects.get(name=category_name)
		except Category.DoesNotExist:
			res['status'] = False
			res['message'] = "Invalid category"
			res['data'] = []
			return Response(res, status=status.HTTP_400_BAD_REQUEST)

		tagsss = []
		# print(tagsss, '222222222222222222222222222222222222222')

		for tag_name in tags.split(","):
			# print(tag_name, '8888888888888888888888888888888888')
			
			try:
				tag = Tags.objects.get(name=tag_name.strip())
				tagsss.append(tag)

			except Tags.DoesNotExist:
				res['status'] = False
				res['message'] = "Invalid tag names"
				res['data'] = []
				return Response(res, status=status.HTTP_400_BAD_REQUEST)

		# if invalid_tags is None:
		# 	res['status'] = False
		# 	res['message'] = "Invalid tag names"
		# 	res['data'] = []
		# 	return Response(res, status=status.HTTP_400_BAD_REQUEST)

		data = Post.objects.create(title=title, text=text, category=category, featured_image=featured_image,  post_image=post_image, author=request.user)
		data.tags.set(tagsss)

		serializer = PostSerializer(data, context={"request": request})

		if serializer:
			res['status'] = True
			res['message'] = "Create Post Successful"
			res['data'] = serializer.data
			return Response(res, status=status.HTTP_201_CREATED)
		else:
			res['status'] = False
			res['message'] = "Something went wrong"
			res['data'] = []
			return Response(res, status=status.HTTP_400_BAD_REQUEST)

# How to update post 
class PostUpdateAPiView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request, id=None):
		res = {}
		title = request.data.get("title", None)
		# print(title, 'nnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
		text = request.data.get("text", None)
		category = request.data.get("category", None)
		tags = request.data.get("tags", None)
		postid= request.data.get("id", None)
 
		post = Post.objects.filter(id=postid).last()  #filter post 
		# post = Post.objects.get(author=request.user.id).last()  #filter all post of author
		# post = Post.objects.get(id=postid) #get post with get method
		# print(postid, "55555555555555555555555555555555555555555555555")

		if post is None:
			res['status'] = False
			res['message'] = "Authenticate Post detail not found!!"
			res['data'] = []
			return Response(res,  status=status.HTTP_404_NOT_FOUND)

		if category:
			res['status'] = False
			res['message'] = "Category is not changeable"
			res['data'] = []
			return Response(res, status=status.HTTP_400_BAD_REQUEST)

		if tags:
			res['status'] = False
			res['message'] = "Tags is not changeable"
			res['data'] = []
			return Response(res, status=status.HTTP_400_BAD_REQUEST)

		data = request.data   

		try:
			data._mutable =True
		
		except:
			pass
		# data['text'] = post.text
		# data['title'] = post.title
		data['category'] = post.category

		data['tags'] = post.tags

		# if title is None:
		# 	data['title'] = post.title

		if title is None:
			data['title'] = post.title
		if text is None:
			data['text'] = post.text

		# print(data,"kkkkkkkkkkkkkkkkkkkkk")

		serializer = PostdetailsSerializer(data=data, instance = post, context={'request': request}) 
		# print(serializer, '787887788888888888888888')
		
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			res['status'] = True
			res['message'] = 'Post detail Update successfully'
			res['data'] = serializer.data
			return Response(res, status=status.HTTP_200_OK)

		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                              
# How to delete a post 
class DeletepostAPiView(APIView):
	permission_classes = [IsAuthenticated]

	def delete(self, request):
		user = User.objects.get(id=request.user.id)
		# print(user, "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
		# post = Post.objects.get(author=request.user)
		post = Post.objects.filter(author=request.user.id).last()
		# print(post, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
		post.delete()
		return Response({'status': True, 'message': 'Post Delete successfully'}, status=status.HTTP_200_OK)

