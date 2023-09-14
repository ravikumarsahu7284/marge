from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from blog.serializers import UserSerializer, UserdetailsSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from blog.models import User


# How to ragister a user 
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        res = {}
        first = request.data.get("first_name", None)
        last = request.data.get("last_name", None)
        # print(last,'9999999999')
        email = request.data.get("email", None)
        city = request.data.get("city", None)
        # print(email,'4444444444444')
        password = request.data.get("password", None)

        if first is None:
            res['status'] = False
            res['message'] = "First Name is required"
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        if last is None:
            res['status'] = False
            res['message'] = "Last Name is required"
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        if email is None:
            res['status'] = False
            res['message'] = "Email is required"
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        if city is None:
            res['status'] = False
            res['message'] = "Email is required"
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        

        if password is None:
            res['status'] = False
            res['message'] = "password is required"
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        encrypt_password = make_password(password)
            
        data = request.data
        # try:
        #     data._mutable =True
        # except:
        #     pass
        print(data, 'uuuuuuuuuuuuuu')
        serializer = UserSerializer(data=data, context={"request":request} )
        print(serializer, '9999999999999999')
        # serializer = UserSerializer(data=request.data)
        # try:
        #     data._mutable =True
        # except:
        #     pass
        
        
        if serializer.is_valid():
            user = User.objects.create(email=email, password=password, first_name=first, last_name=last, city=city)
            print(user, 'tttttttttttttttttttttttttttttttttttttt')
            serializer.save(password=encrypt_password)
            # user = User.objects.create_user(email=email, password=password, first_name=first, last_name=last, city=city)
            # print(user, 'tttttttttttttttttttttttttttttttttttttt')
         

        if serializer:
            res['status'] = True
            res['message'] = "Register successfull"
            res['data'] = serializer.data
            print(res['data'], '12222222222222222222222')
            return Response(res, status=status.HTTP_200_OK)
        else:
            res['status'] = False
            res['message'] = "somthing went wrong"
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


# How to login a user 
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        res = {}
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        if username is None:
            res['status'] = False
            res['message'] = "username is required"
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        if password is None:
            res['status'] = False
            res['message'] = "password is required"
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is None:
            res['status'] = False
            res['message'] = "Invalid username & password is required"
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        # print(user,'rrrrrrrrrrrr')
    
        serializer = UserSerializer(user, read_only=True, context={"request":request} )
        # print(serializer,'zzzzzzzzzzzzzzzzzzz')
        
        if serializer:
            res['status'] = True
            res['message'] = "Login successfull"
            res['data'] = serializer.data
            return Response(res, status=status.HTTP_200_OK)
        else:
            res['status'] = False
            res['message'] = "somthing went wrong"
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


# How to see Login user profile details
class ProfileAPiView(APIView):
    # authentication_classes = (IsAuthenticated,)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        res = {}
        try:
            user = User.objects.filter(id=request.user.id).last()
            print(user, 'kkkkkkkkk')
            if user is None:
                res['status'] = False
                res['message'] = "Authentication detail not found!!"
                res['data'] = []
                return Response(res,  status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(user, read_only=True, context={'request': request})
            if serializer:
                res['status'] = True
                res['message'] = 'User detail fetched successfully'
                res['data'] = serializer.data
                return Response(res, status=status.HTTP_200_OK)
            else:
                res['status'] = False
                res['message'] = "User Not Found!!"
                res['data'] = []
                return Response(res,  status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


# How to update a user profile 
class ProfileUpdateAPiView(APIView):
    # authentication_classes = (IsAuthenticated,)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        res = {}

        first_name = request.data.get("first_name", None)
        # print(first_name, 'first nnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
        last_name = request.data.get("last_name", None)
        email = request.data.get("email", None)
        city = request.data.get("city", None)
 
        user = User.objects.get(id=request.user.id)
        # print(user, "user print check")

        if user is None:
            res['status'] = False
            res['message'] = "Authenticate User detail not found!!"
            res['data'] = []
            return Response(res,  status=status.HTTP_404_NOT_FOUND)

        if email:
            res['status'] = False
            res['message'] = "Email is not changeable"
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        data = request.data   

        try:
            data._mutable =True
		
        except:
            pass

        data['username'] = user.username

        data['email'] = user.email

        if first_name is None:
            data['first_name'] = user.first_name

        if last_name is None:
            data['last_name'] = user.last_name
        if city is None:
            data['city'] = user.city

        serializer = UserdetailsSerializer(data=data, instance = user, context={'request': request}) 
        print(serializer, '787887788888888888888888')
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            res['status'] = True
            res['message'] = 'User detail Update successfully'
            res['data'] = serializer.data
            return Response(res, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# How to delete a user 
class DeleteProfileAPiView(APIView):
    # authentication_classes = (IsAuthenticated,)
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = User.objects.get(id=request.user.id)
        # serializer = UserSerializer(user, data=request.data, partial=True) 
        user.delete()
        return Response({'status': True, 'message': 'Profile Delete successfully'}, status=status.HTTP_200_OK)


# Collect all ragister user data in a list
class ProfileListAPiView(APIView):
    # authentication_classes = (IsAuthenticated,)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        res = {}
        try:
            user = User.objects.all()
            print(user, 'kkkkkkkkk')
            if user is None:
                res['status'] = False
                res['message'] = "Authentication detail not found!!"
                res['data'] = []
                return Response(res,  status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(user, read_only=True, many=True, context={'request': request})
            if serializer:
                res['status'] = True
                res['message'] = 'User detail fetched successfully'
                res['data'] = serializer.data
                return Response(res, status=status.HTTP_200_OK)
            else:
                res['status'] = False
                res['message'] = "User Not Found!!"
                res['data'] = []
                return Response(res,  status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

