from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from blog.serializers import PostSerializer, PostdetailsSerializer, CommentSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from blog.models import User, Post, Category, Tags, Comment


class CommentListAPIView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request, id=None):
		res = {}
		try:
			# post = Post.objects.last()
			post = Post.objects.filter(id=id, author=request.user).last()
			print(post, 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
			comments = Comment.objects.filter(post=post).all()
			if post:
				
				comment = comments.first()
				print(comments, 'ddddddddddddddddddddddddddddddddddddd')

				if comment is None:
					res['status'] = False
					res['message'] = "Comments for the post not found"
					res['data'] = []
					return Response(res, status=status.HTTP_404_NOT_FOUND)

				# Assuming your CommentSerializer expects a 'post' field, pass the comment
				# object (not the queryset) to the serializer.
				serializer = CommentSerializer(comment, context={'request': request})
			else:
				comments = Comment.objects.all()
				# For multiple comments, use many=True
				serializer = CommentSerializer(comments, many=True, context={'request': request})

			res['status'] = True
			res['message'] = 'Comments fetched successfully'
			res['data'] = serializer.data
			return Response(res, status=status.HTTP_200_OK)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# How to delete a comment 
class DeletecommentAPiView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        post = Post.objects.get(id=request.user.id)
        # print(user, "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
        # post = Post.objects.get(author=request.user)
        comment = Comment.objects.filter(author=request.user.id).last()
        # print(post, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        comment.delete()
		
        return Response({'status': True, 'message': 'Comment Delete successfully'}, status=status.HTTP_200_OK)








class CommentListAPiView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request, id=None):
		res = {}
		try:
			# post=request.data
			post = Post.objects.filter(id=id, author=request.user).last()
			# post = Post.objects.get(id=request.user.id)
			print(post, 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
			comments = Comment.objects.all()
			# print(comments, 'rrrrrrrrrrrrrrrrrrrrrrr')
			# if id:
			if post:
				comment = comments.filter(post=post).last()
				# print(comments, 'ddddddddddddddddddddddddddddddddddddd')
				if comment is None:
					res['status'] = False
					res['message'] = "Comments for the post not found"
					res['data'] = []
					return Response(res, status=status.HTTP_404_NOT_FOUND)
				serializer = CommentSerializer(comments, context={'request': request})
				res['status'] = True
				res['message'] = 'Comments fetched successfully'
				res['data'] = serializer.data
				return Response(res, status=status.HTTP_200_OK)
			
			serializer = CommentSerializer(comments, many=True, context={'request': request})

			res['status'] = True
			res['message'] = 'Comments fetched successfully'
			res['data'] = serializer.data
			return Response(res, status=status.HTTP_200_OK)

		except Exception as e:
			res['status'] = False
			res['message'] = str(e)
			res['data'] = []
			return Response(res, status=status.HTTP_404_NOT_FOUND)


class CommentDetailsAPiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        res = {}
        try:
            comments = Comment.objects.filter(id=id).last()
			
            if not comments:
                res['status'] = False
                res['message'] = "Comments for the post not found"
                res['data'] = []
                return Response(res, status=status.HTTP_404_NOT_FOUND)
			
            serializer = CommentdetailsSerializer(comments, context={'request': request})

            res['status'] = True
            res['message'] = 'Comments fetched successfully'
            res['data'] = serializer.data
            return Response(res, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            res['status'] = False
            res['message'] = "Post not found"
            res['data'] = []
            return Response(res, status=status.HTTP_404_NOT_FOUND)





class CommentListAPiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        res = {}
        try:
            post_id = Post.objects.last()
            print(post_id, 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
            comments = Comment.objects.all()
            if post_id:
				
                comment = comments.last()
                print(comments, 'ddddddddddddddddddddddddddddddddddddd')
                if comment is None:
                    res['status'] = False
                    res['message'] = "Comments for the post not found"
                    res['data'] = []
                    return Response(res, status=status.HTTP_404_NOT_FOUND)
                serializer = CommentSerializer(comments, context={'request': request})
                res['status'] = True
                res['message'] = 'Comments fetched successfully'
                res['data'] = serializer.data
                return Response(res, status=status.HTTP_200_OK)
			
            serializer = CommentSerializer(comments, many=True, context={'request': request})

            res['status'] = True
            res['message'] = 'Comments fetched successfully'
            res['data'] = serializer.data
            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=status.HTTP_404_NOT_FOUND)